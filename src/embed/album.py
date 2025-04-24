from discord import Embed
from api import albums
import math
from datetime import datetime

def get_embed_info(album_query, discord_name, guild_name, user_id, guild_id):
    albums_matches = albums.find_album(album_query)
    albums_matches = sorted(albums_matches['results'], key=lambda x: x['ratings_count'], reverse=True)
    exact_match = [album for album in albums_matches if album['title'] == album_query or album['title_slug'] == album_query.lower().replace(' ', '-')]
    if exact_match:
        album = exact_match[0]
    else:
        start_match = [album for album in albums_matches if album['title'].startswith(album_query) or album['title_slug'].startswith(album_query.lower())]
        if start_match:
            album = start_match[0]
        else:
            album = albums_matches[0]
            
    avg_rate = album['average_rating']
    avg_rate = math.floor(avg_rate / 2 * 10) / 10
    
    album_date = album['release_date']
    album_date = datetime.strptime(album_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    embed = embed_album(
        album_name=album['title'],
        album_artist=album['artist']['name'],
        guild_name=guild_name,
        album_url=f"https://musicboard.app{album['url_slug']}",
        album_cover=album['cover'],
        
        discord_name=discord_name,
        user_rate="",
        
        average_rate=avg_rate,
        rating_count=album['ratings_count'],
        release_date=album_date,
        
        ratings=""
    )
    
    return embed
        
    
        
def embed_album(album_name, album_artist, guild_name, album_url, album_cover,
                discord_name, user_rate,
                average_rate, rating_count, release_date,
                ratings
                ):
    
    embed = Embed(
        title=f"{album_name} by {album_artist} in {guild_name}",
        url=album_url
    )
    embed.set_thumbnail(url=album_cover)
    
    embed.add_field(
        name="your rate",
        value=f"{discord_name}: {user_rate}",
        inline=True
    )
    
    embed.add_field(
        name="                ",
        value="                                                                  ",
        inline=True
    )
    
    embed.add_field(
        name="album info",
        value=(
            f"average rate: {average_rate} \n"
            f"rating count: {rating_count} \n"
            f"release date: {release_date} \n"
        ),
        inline=True
    )
    
    embed.add_field(
        name=f"{guild_name}'s rating",
        value=ratings
    )
    
    return embed