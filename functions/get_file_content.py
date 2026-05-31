# functions/get_file_content.py
from functions.func_utils import is_valid_filepath

MAX_CHARACTERS=10000

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
