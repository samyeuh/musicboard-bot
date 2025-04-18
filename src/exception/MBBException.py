from discord import Embed, Color

class MBBException(Exception):
   
    def __init__(self, title, message):
        self.embed = Embed(title=title, description=message, color=Color.red())
    
    def getMessage(self):
        return self.embed
    
    def __str__(self):
        return f"[MBBException] {self.embed.title} - {self.embed.description}"
