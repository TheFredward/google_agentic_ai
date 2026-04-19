import os
import subprocess

from google.genai import types


def run_python_file(working_dir, file_path, args=None):
    abs_working_path = os.path.abspath(working_dir)
    abs_file_path = os.path.normpath(os.path.join(abs_working_path, file_path))
    if os.path.commonpath([abs_working_path, abs_file_path]) != abs_working_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error "{file_path}" is not a Python file'
    command = ["python", abs_file_path]
    if args is not None:
        command.extend(args)
    program_status = subprocess.run(command, text=True, timeout=30, capture_output=True)
    if program_status.returncode != 0:
        output_string = f"Process exited with code {program_status}"
    if program_status.stderr is None and program_status.stdout is None:
        output_string = "No outpout produced"
    else:
        output_string = (
            f"STDOUT: {program_status.stdout}\nSTDERR: {program_status.stderr}"
        )
    return output_string


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python script with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file to read from, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items={"type": types.Type.STRING},
                description="Optional args that can be passed to the program",
            ),
        },
        required=["file_path"],
    ),
)
