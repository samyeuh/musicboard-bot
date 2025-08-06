from exception import MBBException

supabase = None
def _check_supabase_initialized():
    if supabase is None:
        raise MBBException("Database not initialized", "Please initialize the database before using this function.")

def init_db(client):
    global supabase
    supabase = client

def add_user(discord_id, musicboard_id, musicboard_token, language):
    _check_supabase_initialized()
    if not discord_id or not musicboard_id or not musicboard_token:
        raise MBBException("Invalid input", "Discord ID, Musicboard ID, and token must be provided.")
    
    supabase.table("users").insert({
        "discord_id": discord_id,
        "musicboard_id": musicboard_id,
        "musicboard_token": musicboard_token,
        "language": language
    }).execute()
    
def get_user(discord_id):
    _check_supabase_initialized()
    if not discord_id:
        raise MBBException("Invalid Discord ID", "The provided Discord ID is invalid.")
    
    user = supabase.table("users").select("*").eq("discord_id", discord_id).execute()
    if user.data:
        return user.data[0]
   
def delete_user(discord_id):
    _check_supabase_initialized()
    if not discord_id:
        raise MBBException("Invalid Discord ID", "The provided Discord ID is invalid.")
    
    supabase.table("users").delete().eq("discord_id", discord_id).execute()

