import os

def is_valid_filepath(working_directory: str, file_path: str) -> tuple[bool, str]:
    working_directory_abs_path = os.path.abspath(working_directory)
    file_path_abs_path = os.path.join(working_directory_abs_path, file_path)
    if os.path.commonpath([working_directory_abs_path, file_path_abs_path]) != working_directory_abs_path:
        return (False, f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(file_path_abs_path):
        return (False, f'Error: File not found or is not a regular file: "{file_path}"')
    return (True, f'{file_path_abs_path}')
