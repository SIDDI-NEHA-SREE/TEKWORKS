# src/config.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client
 
load_dotenv()  # loads .env from project root
 
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
 
def get_supabase() -> Client:
    """
    Return a supabase client. Raises RuntimeError if config missing.
    """
    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment (.env)")
    return create_client(supabase_url, supabase_key)