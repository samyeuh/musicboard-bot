import sqlite3
from exception.MBBException import MBBException
import os

DB_PATH = str(os.getenv("DB"))

def init_db():
    os.makedirs("src/db/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id TEXT PRIMARY KEY,
            default_language TEXT DEFAULT 'EN'
        )
    """)
    
    conn.commit()
    conn.close()

def add_guild(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO guilds (guild_id) VALUES (?)", (guild_id,))
    
    conn.commit()
    conn.close()

def get_guid_language(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
    
    res = cursor.fetchone()
    conn.close()
    
    return res[1] if res else None

def remove_guild(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM guilds WHERE guild_id = ?", (guild_id,))
    
    conn.commit()
    conn.close()
    
def get_nb_guild():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM guilds")
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count

def change_language(guild_id, language):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE guilds SET default_language = ? WHERE guild_id = ?", (language, guild_id))
    
    conn.commit()
    conn.close()