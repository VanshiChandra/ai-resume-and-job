import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PORT = int(os.getenv("PORT", 8000))
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
