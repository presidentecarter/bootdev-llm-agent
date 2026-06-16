import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from call_function import call_function
from prompts import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


def process_response(response, args):
    if not response.usage_metadata:
        raise RuntimeError("No LLM response received")
    if args.verbose:
        print(f"User prompt: {response.prompt_feedback}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []
    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call)

            if not function_call_result.parts:
                raise Exception(f"function call {call.name} returned empty .parts")
            if not function_call_result.parts[0].function_response:
                raise Exception(f"function call {call.name} contained response of None")
            if not function_call_result.parts[0].function_response.response:
                raise Exception(f"function call {call.name} had no response")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    return function_results

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("no GEMINI_API_KEY found")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_run_python_file, schema_write_file, schema_get_file_content]
    )

    config=types.GenerateContentConfig(tools=[available_functions],
                                       system_instruction=system_prompt,
                                       temperature=0)

    for _ in range(20):
        response = client.models.generate_content(
            contents=messages,
            model='gemini-2.5-flash',
            config=config
        )

        if response.candidates:
            for c in response.candidates:
                if c.content:
                    messages.append(c.content)

        function_results = process_response(response, args)

        if function_results:
            messages.append(types.Content(role="user", parts=function_results))
        else: 
            exit(0)
    
    print("maximum number of iterations reached")
    exit(1)

if __name__ == "__main__":
    main()
