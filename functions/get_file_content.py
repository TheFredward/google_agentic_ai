import os

from google.genai import types

from config import MAX_CHARS


def get_file_content(working_dir, file_path):
    try:
        abs_working_dir = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside permitted working directory.'
        if not os.path.isfile(target_dir):
            return f"Error: File not found or is not a regular file: {file_path}"
        with open(target_dir) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content
    except Exception as e:
        return f"Error: Exception occured: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the specified file, truncated at 10,000 chars",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file to read from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
