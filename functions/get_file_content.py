
import os
from config import CH_LIMIT
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description = "Retrieves the contents of a specified file within the working directory, ensuring access is limited to files inside it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to retrieve the contents from, relative to the working directory. If not provided, retrieve files in the working directory itself.",
            ),
        },
    ),
)




def get_file_content(working_directory, file_path):
	working_directory_abs = os.path.abspath(working_directory)
	

	path = os.path.join(working_directory, file_path)

	directory_abs = os.path.abspath(path)

	print(f"Result for '{path}' file")

	if directory_abs.startswith(working_directory_abs) == False:
		return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

	if os.path.isfile(path) == False:
		return(f'Error: File not found or is not a regular file: "{file_path}"')

	try:
		with open(path, "r") as f:
			file_content_string = f.read(CH_LIMIT)

		if len(file_content_string) >= CH_LIMIT:
			return(f"{file_content_string} \n[...File '{file_path}' truncated at 10000 characters]")
		else:
			return(file_content_string)

	except Exception as e:
		return(f"Error: exception - {e}")

