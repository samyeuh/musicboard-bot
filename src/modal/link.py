from discord import ui, TextStyle, Embed, Color
import db
import db.users
from exception.MBBException import MBBException
from api import users, login

async def only_linking(interaction, discord_id, guild_id):
    await interaction.response.defer(thinking=True, ephemeral=True)
    okEmbed = Embed(
            title="account linked", 
            description=f"your musicboard is linked! :D",
            color=Color.green()
        )
    if guild_id:
        db.user_guilds.link_user_to_guild(discord_id, guild_id)
    
    await interaction.followup.send(embed=okEmbed, ephemeral=True)

class Link(ui.Modal, title="link your account"):
    def __init__(self, guild_id, discord_id):
        super().__init__()
        self.name = ui.TextInput(
            label="😎",
            style=TextStyle.short,
            placeholder="your musicboard username",
            required=True,
            max_length=25,
        )
        
        self.password = ui.TextInput(
            label="🔑",
            style=TextStyle.short,
            placeholder="musicboard password (don't worry, it is not stored)",
            required=True
        )
        self.add_item(self.name)
        self.add_item(self.password)
        self.guild_id = guild_id
        self.discord_id = discord_id
    
    async def on_submit(self, interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        okEmbed = Embed(
            title="account linked", 
            description=f"your musicboard account **{self.name.value}** has been linked to your discord account! :D",
            color=Color.green()
        )
        
        try:
            if users.exists(self.name.value):
                musicboard_token = login.get_token(self.name.value, self.password.value)
                musicboard_id = users.get_uid(self.name.value)
                user_info = users.me(musicboard_token)
                lang = user_info['primary_language']
                if not db.users.get_user(self.discord_id):
                    db.users.add_user(self.discord_id, musicboard_id, musicboard_token, lang)
                if self.guild_id:
                    db.user_guilds.link_user_to_guild(self.discord_id, self.guild_id)
                await interaction.followup.send(embed=okEmbed, ephemeral=True)
            else:
                raise MBBException("user not found!", f"{self.name.value} is not found on musicboard ! :/")
        except MBBException as e:
            await interaction.followup.send(embed=e.getMessage(), ephemeral=True)
        
        