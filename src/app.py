import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
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
        await bot.tree.sync()
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")
    
    
async def load_extension():
    await bot.load_extension("commands")

async def main():
    await load_extension()
    await bot.start(os.getenv("TOKEN"))
    
if __name__ == "__main__":
    asyncio.run(main())