import sqlite3
from exception.MBBException import MBBException
import os

DB_PATH = "data/profiles.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            guild_id TEXT,
            discord_id TEXT,
            musicboard_username TEXT NOT NULL,
            PRIMARY KEY (guild_id, discord_id)
        )
    """)
    
    conn.commit()
    conn.close()
    
def link_profile(guild_id: int, discord_id: int, username: str):
    """ link your discord profile and your musicboard account to the database! """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO profiles (guild_id, discord_id, musicboard_username)
        VALUES (?, ?, ?)
        ON CONFLICT(guild_id, discord_id) DO UPDATE SET musicboard_username = excluded.musicboard_username
    """, (str(guild_id), str(discord_id), username))
    conn.commit()
    conn.close()
    
def get_profile(guild_id: int, discord_id: int):
    """ get your profile """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT musicboard_username
        FROM profiles
        WHERE guild_id = ? AND discord_id = ?
    """, (str(guild_id), str(discord_id)))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else MBBException("error get profil!", f"error during trying to get your profile :/")

def get_all_profiles_for_guild(guild_id: int):
    """ get all profiles of yout discord server """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT discord_id, musicboard_username
        FROM profiles
        WHERE guild_id = ?
    """, (str(guild_id),))
    results = cursor.fetchall()
    conn.close()
    return results
    