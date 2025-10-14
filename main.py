import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types




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


	response = client.models.generate_content(
		model = ai_model, contents = messages, 
	)

	if verbose == True:
		print(f"""User prompt: {user_prompt} \n
			Prompt tokens: {response.usage_metadata.prompt_token_count}
			Response tokens: {response.usage_metadata.candidates_token_count}
			""")
	else:
		print(response.text)



generate_content(ai_model, messages, verbose)
