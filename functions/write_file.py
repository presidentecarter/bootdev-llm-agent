import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file_path from a specific working directory, given certain content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="relative file path from working directory to write a file to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into file",
            ),
        },
    ),
)

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
