import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
        if os.path.commonpath([working_directory_abs_path, file_path_abs_path]) != working_directory_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs_path]

        if args:
            command.extend(args)

        print(f"\nRunning {file_path}")
        res = subprocess.run(command, text=True, capture_output=True, cwd=working_directory_abs_path, timeout=30)

        output_string = ""
        if res.returncode != 0:
            output_string += f"Process exited with code {res.returncode}"
        if not (res.stderr or res.stdout):
            output_string += "no output produced"
        else:
            output_string += "STDOUT:" + res.stdout + '\n'
            output_string += "STDERR:" + res.stderr
        return output_string
    except Exception as e:
        return f'Error: executing Python file: {e}'
