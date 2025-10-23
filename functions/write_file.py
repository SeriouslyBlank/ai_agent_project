import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description = "Overwrites or Writes the file, relative to the working directory. Must be located within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write the file, relative to the working directory.",

            ),
            "content": types.Schema(
            	type=types.Type.STRING,
            	description="The content that will be written to the file",)
        },
    ),
)



def write_file(working_directory, file_path, content):

	working_directory_abs = os.path.abspath(working_directory)
	

	path = os.path.join(working_directory, file_path)

	file_abs = os.path.abspath(path)
	print(f"Result for '{path}' file")

	if file_abs.startswith(working_directory_abs) == False:
		return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

	try :

		output = 0
		dir_name = os.path.dirname(file_abs)

		if os.path.exists(dir_name) == True:
			with open(file_abs, "w") as f:
				f.write(content)
				output = 1
		else:
			os.makedirs(dir_name)
			with open(file_abs, "w") as f:
				f.write(content)
				output = 1

		if output == 1:
			return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
		else:
			return(f"Didn't work")


	except Exception as e:
		return(f"Error: exception - {e}")



