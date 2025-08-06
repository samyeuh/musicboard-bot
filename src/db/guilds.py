from exception.MBBException import MBBException

supabase = None
def _check_supabase_initialized():
    if supabase is None:
        raise MBBException("Database not initialized", "Please initialize the database before using this function.")
    
def init_db(client):
    global supabase
    supabase = client

def add_guild(guild_id):
    _check_supabase_initialized()
    
    supabase.table("guilds").insert({"guild_id": guild_id}).execute()
    
def get_guild(guild_id):
    _check_supabase_initialized()
    
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")
    
    response = supabase.table("guilds").select("*").eq("guild_id", guild_id).execute()
    if not response.data:
        return None
    
    return response.data[0]

def get_guid_language(guild_id):
    _check_supabase_initialized()
    
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")
    
    res = supabase.table("guilds").select("default_language").eq("guild_id", guild_id).execute()
    if res.data:
        return res.data[0]['default_language']

def remove_guild(guild_id):
    _check_supabase_initialized()
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")
    
    supabase.table("guilds").delete().eq("guild_id", guild_id).execute()
    
def get_nb_guild():
    _check_supabase_initialized()
    
    response = supabase.table("guilds").select("id", count="exact").limit(1).execute()
    return response.count if response.count is not None else 0

def change_language(guild_id, language):
    _check_supabase_initialized()
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")
    if not language:
        raise MBBException("Invalid language", "The provided language is invalid.")
    
    supabase.table("guilds").update({"default_language": language}).eq("guild_id", guild_id).execute()