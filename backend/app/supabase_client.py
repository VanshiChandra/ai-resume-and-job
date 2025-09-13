from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("Supabase URL or service role key not configured in env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
