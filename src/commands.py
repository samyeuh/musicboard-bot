from discord.ext import commands
from discord import app_commands, Interaction
from modal.link  import Link

class MusicboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    USERS COMMANDS
    """

    @app_commands.command(name="ping", description="test if bot is online/ok")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("pong :p")
        
    @app_commands.command(name="link", description="link your discord account to your Musicboard account")
    async def link(self, interaction: Interaction):
        await interaction.response.send_modal(Link())
        
        

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))