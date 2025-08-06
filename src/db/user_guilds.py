from exception.MBBException import MBBException
from db.guilds import get_guild, add_guild

supabase = None
def _check_supabase_initialized():
    if supabase is None:
        raise MBBException("Database not initialized", "Please initialize the database before using this function.")

def init_db(client):
    global supabase
    supabase = client

def link_user_to_guild(discord_id, guild_id):
    _check_supabase_initialized()
    if not discord_id or not guild_id:
        raise MBBException("Invalid input", "Discord ID and Guild ID must be provided.")
    if get_guild(guild_id) is None:
        add_guild(guild_id)
    supabase.table("user_guilds").insert({"discord_id": discord_id, "guild_id": guild_id}).execute()


def unlink_user_from_guild(discord_id, guild_id):
    _check_supabase_initialized()
    if not discord_id or not guild_id:
        raise MBBException("Invalid input", "Discord ID and Guild ID must be provided.")
    
    supabase.table("user_guilds").delete().eq("discord_id", discord_id).eq("guild_id", guild_id).execute()
    


def get_users_in_guild(guild_id):
    _check_supabase_initialized()
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")

    response = supabase.table("user_guilds").select("discord_id, users(musicboard_token)").eq("guild_id", guild_id).execute()
    if not response.data:
        return []
    return [{"discord_id": row['discord_id'], "musicboard_token": row['users']['musicboard_token']} for row in response.data]
    
    


def get_guilds_of_user(discord_id):
    _check_supabase_initialized()
    if not discord_id:
        raise MBBException("Invalid Discord ID", "The provided Discord ID is invalid.")
    
    response = supabase.table("user_guilds").select("guild_id").eq("discord_id", discord_id).execute()
    if not response.data:
        return []
    
    return [row['guild_id'] for row in response.data]
    


def is_linked(discord_id, guild_id):
    _check_supabase_initialized()
    if not discord_id or not guild_id:
        raise MBBException("Invalid input", "Discord ID and Guild ID must be provided.")
    
    response = supabase.table("user_guilds").select("*").eq("discord_id", discord_id).eq("guild_id", guild_id).execute()
    if response.data:
        return True
    return False

def remove_all_users(guild_id):
    _check_supabase_initialized()
    if not guild_id:
        raise MBBException("Invalid guild ID", "The provided guild ID is invalid.")
    
    supabase.table("user_guilds").delete().eq("guild_id", guild_id).execute()
