import os
from dotenv import load_dotenv
import goodfire

# Load .env file
load_dotenv()

# Get values from .env
api_key = os.getenv("GOODFIRE_API_KEY")

client = goodfire.Client(api_key=api_key)
# Instantiate a model variant.
variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")

for token in client.chat.completions.create(
    [{"role": "user", "content": "Hi, how are you?"}],
    model=variant,
    stream=True,
    max_completion_tokens=100,
):
	print(token.choices[0].delta.content, end="")
