import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    # We wrap everything in a try except block so we always return a string, even when there is an error when calling one of the os functions.
    try:
        abs_working_dir = os.path.abspath((working_directory))
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = (
            os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command: list[str] = ["python", abs_file_path]
        if args:
            command.extend(args)
        process: subprocess.CompletedProcess = subprocess.run(
            command, cwd=abs_working_dir, text=True, capture_output=True, timeout=30
        )
        output: list[str] = []
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            output.append("No output produced")
        else:
            output.append(f"STDOUT:\n{process.stdout}")
            output.append(f"STDERR:\n{process.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
