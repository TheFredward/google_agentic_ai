import os

from google.genai import types


def write_file(working_dir, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to specified file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that needs to be written into the specified file in file_path",
            ),
        },
        required=["file_path", "content"],
    ),
)
