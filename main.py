import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import SYS_PROMPT as system_prompt 
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function


max_iters = 20


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


if len(sys.argv) > 2 and sys.argv[2]!= "--verbose":
	print("prompt not in quotes :)\n Eg. uv run main.py '[prompt]' --verbose(optional)")
	sys.exit(2)

if len(sys.argv) == 1:
	print("no prompt provided")
	sys.exit(1)

user_prompt = sys.argv[1]

ai_model = "gemini-2.0-flash-001"


if len(sys.argv)>2:
	verbose = True
else:
	verbose = False


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]





def generate_content(ai_model, messages, verbose):

	for i in range(0, max_iters):
		response = client.models.generate_content(
			model = ai_model, contents = messages,
		    config=types.GenerateContentConfig(
	    	tools=[available_functions], system_instruction=system_prompt)
		)

		if verbose == True:
				print(f"""User prompt: {user_prompt} \n
					Prompt tokens: {response.usage_metadata.prompt_token_count}
					Response tokens: {response.usage_metadata.candidates_token_count}
					""")

		if response.candidates:
			for candidate in response.candidates:
				if candidate is None or candidate.content is None:
					continue
				messages.append(candidate.content)


		if response.function_calls:
			for function_call_part in response.function_calls:
				result = call_function(function_call_part, verbose)
				messages.append(result)

		else:
			print(response.text)
			return




	



generate_content(ai_model, messages, verbose)
