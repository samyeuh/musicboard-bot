import sqlite3
from exception.MBBException import MBBException
import os

DB_PATH = "src/db/data/profiles.db"

def init_db():
    os.makedirs("src/db/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            guild_id TEXT,
            discord_id TEXT,
            musicboard_id TEXT NOT NULL,
            access_token TEXT NOT NULL,
            PRIMARY KEY (guild_id, discord_id)
        )
    """)
    
    conn.commit()
    conn.close()

def link_profile(guild_id: int, discord_id: int, musicboard_id: str, access_token: str):
    """ link your discord profile and your musicboard account to the database! """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO profiles (guild_id, discord_id, musicboard_id, access_token)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(guild_id, discord_id) DO UPDATE SET 
            musicboard_id = excluded.musicboard_id,
            access_token = excluded.access_token
    """, (str(guild_id), str(discord_id), musicboard_id, access_token))
    
    conn.commit()
    conn.close()

def get_profile(guild_id: int, discord_id: int):
    """ get your profile (musicboard_id + token) """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT musicboard_id, access_token
        FROM profiles
        WHERE guild_id = ? AND discord_id = ?
    """, (str(guild_id), str(discord_id)))
    result = cursor.fetchone()
    conn.close()
    return result if result else MBBException("error get profile!", "error during trying to get your profile :/")

def get_all_profiles_for_guild(guild_id: int):
    """ get all profiles of your discord server """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT discord_id, musicboard_id, access_token
        FROM profiles
        WHERE guild_id = ?
    """, (str(guild_id),))
    
    results = cursor.fetchall()
    conn.close()
    return results if results else MBBException("error get all profiles for guild!", "error during trying to get all profiles :/")
