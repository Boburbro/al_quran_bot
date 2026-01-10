import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OAuth2 credentials from environment
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Quran API token URL
TOKEN_URL = "https://oauth2.quran.foundation/oauth2/token"
