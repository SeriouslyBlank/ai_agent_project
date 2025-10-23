import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description = "Runs the python file, relative to the working directory. Must be located within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run the file from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



def run_python_file(working_directory, file_path, args=[]):

	working_directory_abs = os.path.abspath(working_directory)
	

	path = os.path.join(working_directory, file_path)

	file_abs = os.path.abspath(path)

	print(f"Result for file - {file_path} args - {args}")

	if file_abs.startswith(working_directory_abs) == False:
		return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

	if os.path.exists(file_abs) == False:
		return(f'Error: File "{file_path}" not found.')

	if file_path.endswith('.py') == False:
		return(f'Error: "{file_path}" is not a Python file.')

	try:
		
		sub = subprocess.run(args = ["python", file_abs], capture_output= True, timeout = 30, cwd = working_directory_abs, check = True)

		if sub.returncode != 0:
			return(f"STDOUT: {sub.stdout} \n STDERR: {sub.stderr} \n Process exited with code {sub.returncode}")
		elif not sub.stdout.strip():
			print(sub)
			return("No output produced")
		else:
			return(f"STDOUT: {sub.stdout} \n STDERR: {sub.stderr}")

	except Exception as e:
		return(f"Error: executing Python file: {e} - exception")






