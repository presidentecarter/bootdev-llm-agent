import os
from functions.func_utils import is_valid_filepath

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try: 
        # checking existence
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.join(working_directory_abs_path, file_path)
        if os.path.commonpath([working_directory_abs_path, file_path_abs_path]) != working_directory_abs_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(file_path_abs_path), exist_ok=True)

        with open(file_path_abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
