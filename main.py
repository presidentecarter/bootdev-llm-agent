import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info

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
        function_declarations=[schema_get_files_info]
    )

    config=types.GenerateContentConfig(tools=[available_functions],
                                       system_instruction=system_prompt,
                                       temperature=0)

    response = client.models.generate_content(
        contents=messages,
        model='gemini-3.5-flash',
        config=config
    )

    if not response.usage_metadata:
        raise RuntimeError("No LLM response received")
    if args.verbose:
        print(f"User prompt: {response.prompt_feedback}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    print(response.text)

if __name__ == "__main__":
    main()
