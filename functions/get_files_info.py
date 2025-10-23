import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):

	working_directory_abs = os.path.abspath(working_directory)
	

	path = os.path.join(working_directory, directory)

	directory_abs = os.path.abspath(path)

	print(f"Result for '{path}' directory")

	if directory_abs.startswith(working_directory_abs) == False:
		return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')


	if os.path.isdir(path) == False:
		return(f'Error: "{path}" is not a directory')

	try:

		contents_dir = os.listdir(path)

		for x in contents_dir:
			x_path = os.path.join(path,x)
			if os.path.isdir(x_path) == True:
				print(f"- {x}: file_size={os.path.getsize(x_path)} bytes, is_dir=True")

			else:
				print(f"- {x}: file_size={os.path.getsize(x_path)} bytes, is_dir=False")


	except Exception as e:
		return f"Error: {e}"




