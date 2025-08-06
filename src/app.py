import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from db import users, user_guilds, guilds
from supabase import Client, create_client
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")

intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix='mb.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
        for cmd in synced:
            print(f"- {cmd.name}")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")
    
    
async def load_extension():
    await bot.load_extension("commands")

def init_dbs():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    guilds.init_db(supabase)
    users.init_db(supabase)
    user_guilds.init_db(supabase)

async def main():
    init_dbs()
    await load_extension()
    await bot.start(os.getenv("TOKEN"))
    
if __name__ == "__main__":
    asyncio.run(main())