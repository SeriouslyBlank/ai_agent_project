import os




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




