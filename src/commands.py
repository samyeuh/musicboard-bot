from discord.ext import commands
from discord import app_commands, Interaction, Member
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
        
    @app_commands.command(name="profile", description="see a musicboard profile")
    @app_commands.describe(user="the user whose profile you want to see (optional)")
    async def profile(self, interaction: Interaction, user: Member = None):
        target = user or interaction.user

        embed, view = profile.get_embed_info(
            guild_id=interaction.guild.id,
            discord_id=target.id,
            discord_name=target.display_name
        )

        await interaction.response.send_message(embed=embed, view=view)
        
        

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))