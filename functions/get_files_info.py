# functions/get_files_info.py
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    try:
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
            return f'Error: {e}'

    try:
        lines = ["Result for current directory:"]
        for file in os.listdir(target_dir):
            file_path = '/'.join([target_dir, file])
            lines.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        return '\n'.join(lines)
    except Exception as e:
        return f'Error: {e}'
