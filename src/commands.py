from discord.ext import commands
from discord import app_commands, Interaction
from modal.link  import Link
from embed import profile

class MusicboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    USERS COMMANDS
    """

    @app_commands.command(name="ping", description="test if bot is online/ok")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("pong :p", ephemeral=True)
        
    @app_commands.command(name="link", description="link your discord account to your Musicboard account")
    async def link(self, interaction: Interaction):
        await interaction.response.send_modal(Link(interaction.guild.id, interaction.user.id))
        
    @app_commands.command(name="profile", description="see your musicboard profile")
    async def profile(self, interaction: Interaction):
        await interaction.response.send_message(
            embed=profile.get_embed_info(interaction.guild.id, interaction.user.id, interaction.user.display_name)
        )
        
        

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))