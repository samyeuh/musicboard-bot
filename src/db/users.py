import sqlite3
import os

DB_PATH = str(os.getenv("DB"))

def init_db():
    os.makedirs("src/db/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            discord_id TEXT PRIMARY KEY,
            musicboard_id TEXT NOT NULL,
            musicboard_token TEXT NOT NULL,
            language TEXT DEFAULT 'EN'
        )
    """)

    conn.commit()
    conn.close()

def add_user(discord_id, musicboard_id, musicboard_token, language):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO users (discord_id, musicboard_id, musicboard_token, language) VALUES (?, ?, ?, ?)", 
        (discord_id, musicboard_id, musicboard_token, language)
    )
    
    conn.commit()
    conn.close()
    
def get_user(discord_id):
    conn = sqlite3.connect(DB_PATH)
    
    cursor = conn.cursor()
    cursor.execute(
        "SELECT musicboard_id, musicboard_token, language FROM users WHERE discord_id = ?", 
        (discord_id,)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    return user if user else None
   
def delete_user(discord_id):
    conn = sqlite3.connect(DB_PATH)
    
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE discord_id = ?", 
        (discord_id,)
    )
    
    conn.commit()
    conn.close()

