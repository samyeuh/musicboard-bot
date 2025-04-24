from discord.ext import commands
from discord import app_commands, Interaction, Member
from modal.link import Link, only_linking
from embed import profile, album
from exception.MBBException import MBBException
from db import guilds, user_guilds, users

# TODO: attention aux commandes en DM (donc pas de serveur)

class MusicboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    LISTENERS
    """

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds.add_guild(str(guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        user_guilds.remove_all_users(str(guild.id))
        guilds.remove_guild(str(guild.id))
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if users.get_user(str(member.id)) is not None:
            user_guilds.link_user_to_guild(str(member.id), str(member.guild.id))
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if user_guilds.is_linked(str(member.id), str(member.guild.id)):
            user_guilds.unlink_user_from_guild(str(member.id), str(member.guild.id))
    
    """
    USERS COMMANDS
    """

    @app_commands.command(name="ping", description="test if bot is online/ok")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("pong :p", ephemeral=True)
        
    @app_commands.command(name="link", description="link your discord account to your Musicboard account")
    async def link(self, interaction: Interaction):
        if not interaction.guild:
            await interaction.response.send_modal(Link(None, interaction.user.id))
            return
            
        if user_guilds.is_linked(str(interaction.user.id), str(interaction.guild.id)):
            await interaction.response.send_message(embed=MBBException("account already linked", "your account is already linked").getMessage(), ephemeral=True)
            return
        
        if users.get_user(interaction.user.id):
            if not interaction.guild:
                await only_linking(interaction, interaction.user.id, None)
            else:
                await only_linking(interaction, interaction.user.id, interaction.guild.id)
            return
        
        await interaction.response.send_modal(Link(interaction.guild.id, interaction.user.id))
            
        
    @app_commands.command(name="profile", description="see a musicboard profile")
    @app_commands.describe(user="the user whose profile you want to see (optional)")
    async def profile(self, interaction: Interaction, user: Member = None):
        target = user or interaction.user
        if interaction.guild and not user_guilds.is_linked(str(target.id), str(interaction.guild.id)):
            await interaction.response.send_message(embed=MBBException("profil not found", "please do /link before").getMessage(), ephemeral=True)
            return
    
        embed, view = profile.get_embed_info(
            discord_id=target.id,
            discord_name=target.display_name
        )

        await interaction.response.send_message(embed=embed, view=view)
        
    @app_commands.command(name="mb", description="see reviews of an album!")
    @app_commands.describe(query="the album whose reviews you want to see")
    async def mb(self, interaction: Interaction, query: str):
        await interaction.response.defer()
        mbalbum = album.get_embed_info(
            query, 
            interaction.user.display_name, 
            interaction.guild.name,
            interaction.user.id,
            interaction.guild.id
        )
        
        await interaction.followup.send(embed=mbalbum)
        
        

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))