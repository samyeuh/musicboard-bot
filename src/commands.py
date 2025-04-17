import discord
from discord.ext import commands
from discord import app_commands, Interaction, TextChannel, ui, TextStyle, SelectOption

class MusicboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="test si le bot répond.")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("pong 🏓")

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))