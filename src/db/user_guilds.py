import sqlite3
import os

DB_PATH = "src/db/data/user_guilds.db"

def init_db():
    os.makedirs("src/db/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_guilds (
            discord_id TEXT,
            guild_id TEXT,
            PRIMARY KEY (discord_id, guild_id)
        )
    """)

    conn.commit()
    conn.close()

def link_user_to_guild(discord_id, guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO user_guilds (discord_id, guild_id)
        VALUES (?, ?)
    """, (discord_id, guild_id))

    conn.commit()
    conn.close()


def unlink_user_from_guild(discord_id, guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_guilds
        WHERE discord_id = ? AND guild_id = ?
    """, (discord_id, guild_id))

    conn.commit()
    conn.close()


def get_users_in_guild(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT discord_id FROM user_guilds
        WHERE guild_id = ?
    """, (guild_id,))

    res = cursor.fetchall()
    conn.close()

    return [row[0] for row in res]


def get_guilds_of_user(discord_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT guild_id FROM user_guilds
        WHERE discord_id = ?
    """, (discord_id,))

    res = cursor.fetchall()
    conn.close()

    return [row[0] for row in res]

def is_linked(discord_id, guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 1 FROM user_guilds
        WHERE discord_id = ? AND guild_id = ?
    """, (discord_id, guild_id))
    
    res = cursor.fetchone()
    conn.close()
    return res is not None

def remove_all_users(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        """
            DELETE FROM user_guilds WHERE guild_id = ?
        """, (guild_id,)
    )
    
    conn.commit()
    conn.close()
