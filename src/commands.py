from discord.ext import commands
from discord import app_commands, Interaction, Member
from modal.link import Link, only_linking
from embed import profile, album as album_embed, artist as artist_embed, track as track_embed
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
        target = user if user else interaction.user

        user_linked = users.get_user(str(target.id))
        
        if interaction.guild:
            if not user_guilds.is_linked(str(target.id), str(interaction.guild.id)):
                await interaction.response.send_message(
                    embed=MBBException("profil not found", "please do /link before").getMessage(),
                    ephemeral=True
                )
                return
        else:
            if not user_linked:
                await interaction.response.send_message(
                    embed=MBBException("profil not found", "please do /link before").getMessage(),
                    ephemeral=True
                )
                return

        embed, view = profile.get_embed_info(
            discord_id=target.id,
            discord_name=target.display_name
        )

        await interaction.response.send_message(embed=embed, view=view)
        
    @app_commands.command(name="mb", description="see reviews of an album!")
    @app_commands.describe(album="the album whose reviews you want to see")
    async def mb(self, interaction: Interaction, album: str):
        await interaction.response.defer()
        mbalbum = await album_embed.get_embed_info(
            album, 
            interaction.user.display_name, 
            interaction.guild,
            interaction.user.id
        )
        
        await interaction.followup.send(embed=mbalbum)
    
    @app_commands.command(name="mba", description="see reviews of an artist!")
    @app_commands.describe(artist="the artist whose reviews you want to see")
    async def mba(self, interaction: Interaction, artist: str):
        await interaction.response.defer()
        mbartist = await artist_embed.get_embed_info(artist, interaction.user, interaction.guild)
        await interaction.followup.send(embed=mbartist)
    
    @app_commands.command(name="mbt", description="see reviews of a track!")
    @app_commands.describe(track="the track whose reviews you want to see")
    async def mbt(self, interaction: Interaction, track: str):
        await interaction.response.defer()
        mbtrack = await track_embed.get_embed_info(
            track, 
            interaction.user.display_name, 
            interaction.guild,
            interaction.user.id
        )
        
        await interaction.followup.send(embed=mbtrack)
        
        

async def setup(bot):
    await bot.add_cog(MusicboardCommands(bot))