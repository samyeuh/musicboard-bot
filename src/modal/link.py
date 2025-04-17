from discord import ui, TextStyle, Embed, Color
from exception import MBBException
from api import users

class Link(ui.Modal, title="link your account"):
    def __init__(self):
        super().__init__()
        self.name = ui.TextInput(
            label="your musicboard name",
            style=TextStyle.short,
            placeholder="exemple: samyeuh",
            required=True,
            max_length=25,
        )
        self.add_item(self.name)
    
    async def on_submit(self, interaction):
        okEmbed = Embed(
            title="account linked", 
            description=f"your musicboard account **{self.name}** has been linked to your discord account! :D",
            color=Color.green()
        )
        
        try:
            users.search_user(self.name)
            await interaction.response.send_message(embed=okEmbed)
        except MBBException as e:
            await interaction.response.send_message(embed=e.getMessage(), ephemeral=True)
        
        