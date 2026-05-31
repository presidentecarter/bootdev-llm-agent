# functions/get_file_content.py
import os

MAX_CHARACTERS=10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.join(working_directory_abs_path, file_path)
        if os.path.commonpath([working_directory_abs_path, file_path_abs_path]) != working_directory_abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
