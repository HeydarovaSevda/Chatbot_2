import os
from dotenv import load_dotenv
load_dotenv("OPENAI_API_KEY.env")
API_KEY=os.getenv("OPENAI_API_KEY")
assert API_KEY, "API KEY not found, please, check your API file"