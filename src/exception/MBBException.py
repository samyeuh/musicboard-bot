from discord import Embed, Color

class MBBException(Exception):
   
    def __init__(self, title, message):
        self.embed = Embed(title=title, description=message, color=Color.red())
    
    def getMessage(self):
        return self.embed