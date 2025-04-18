from discord import ui, TextStyle, Embed, Color
from db import profiles
from exception.MBBException import MBBException
from api import users, login

class Link(ui.Modal, title="link your account"):
    def __init__(self, guild_id, discord_id):
        super().__init__()
        self.name = ui.TextInput(
            label="your musicboard name",
            style=TextStyle.short,
            placeholder="exemple: samyeuh",
            required=True,
            max_length=25,
        )
        
        self.password = ui.TextInput(
            label="password (not stored, don't worry!)",
            style=TextStyle.short,
            placeholder="exemple: ilovecatgirls.xyz",
            required=True,
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
                profiles.link_profile(self.guild_id, self.discord_id, musicboard_id, musicboard_token)
                await interaction.followup.send(embed=okEmbed, ephemeral=True)
            else:
                raise MBBException("user not found!", f"{self.name.value} is not found on musicboard ! :/")
        except MBBException as e:
            await interaction.followup.send(embed=e.getMessage(), ephemeral=True)
        
        