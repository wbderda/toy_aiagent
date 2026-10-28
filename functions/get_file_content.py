import os
from config import MAX_CHAR_READ_LIMIT


def get_file_content(working_directory: str, file_path: str) -> str:
    # We wrap everything in a try except block so we always return a string, even when there is an error when calling one of the os functions.
    try:
        abs_path = os.path.abspath((working_directory))
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as file:
            file_content_string = file.read(MAX_CHAR_READ_LIMIT)
            # Check if file was larger than MAX_CHAR_READ_LIMIT
            if file.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHAR_READ_LIMIT} characters]'
        return file_content_string
    except Exception as e:
        return f'Error: reading file "{file_path}" {e}'
