# functions/get_file_content.py

from google.genai import types
from functions.func_utils import is_valid_filepath

MAX_CHARACTERS=10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="read a file at the given filepath inside a specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative to working directory, the file path which is the target to read from",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        ok, result = is_valid_filepath(working_directory, file_path)

        if not ok:
            return result

        with open(result, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
