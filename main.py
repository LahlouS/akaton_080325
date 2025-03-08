import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get values from .env
api_key = os.getenv("GOODFIRE_API_KEY")

# Print to verify (remove this in production)
print(f"API Key: {api_key}")
