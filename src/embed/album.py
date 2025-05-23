from discord import Embed
from api import albums
from api import ratings
from api import users as api_users
from db import user_guilds
from db import users as u
import math
from datetime import datetime, timezone
from exception.MBBException import MBBException

def compute_pertinence_score(album_id, user_token, avg_rate):
    if not album_id:
        return -1, -1, -1, -1, None
    albums = ratings.get_album_rated(album_id, user_token)
    if not albums:
        return -1, -1, -1, -1, None
    album = albums[0]
    rating = album['rating']
    likes = album['like_count']
    comments = album['comment_count']
    impressions = album["impression_count"]
    slug = album["review_url_slug"]
    
    created_at = album["created_at"]
    if created_at:
        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_days = (now - created_at).days
    else:
        age_days = 0

    # Ex : +1 point si la note s’approche de la moyenne de l’album
    consensus_bonus = max(0, 5 - abs(rating - avg_rate))  # max 5 pts

    score = (
        rating * 0.1 +             # note * 0.1
        likes * 2 +                # like * 2
        comments * 1.5 +           # commentaire * 1.5
        impressions * 0.3 +        # impression * 0.3
        consensus_bonus * 0.5      # si proche de la moyenne = * 0.5
    )
    
    user_rate = math.floor(rating / 2 * 10) / 10
    
    if user_rate.is_integer():
        user_rate = str(int(user_rate))
    else:
        user_rate = str(user_rate)

    return round(score, 2), user_rate, likes, comments, slug

async def get_embed_info(album_query, discord_name, guild, user_id):
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

    user_token = u.get_user(user_id)
    if not user_token:
        return MBBException("User not linked", "do /link to link your account").getMessage()
    _, access_token, _ = user_token
    
    user_rating_list = ratings.get_album_rated(album['id'], access_token)
    if not user_rating_list:
        user_rate = "unrated"
    else:
        user_rating = user_rating_list[0]['rating']
        user_rate = math.floor(user_rating / 2 * 10) / 10
        if user_rate.is_integer():
            user_rate = str(int(user_rate))
        else:
            user_rate = str(user_rate)
    if guild is None:
        return embed_album(
        album_name=album['title'],
        album_artist=album['artist']['name'],
        guild_name="",
        album_url=f"https://musicboard.app{album['url_slug']}",
        album_cover=album['cover'],
        
        discord_name=discord_name,
        user_rate=user_rate,
        
        average_rate=avg_rate,
        rating_count=album['ratings_count'],
        release_date=album_date,
        
        ratings=""
    )
    users_guild = user_guilds.get_users_in_guild(guild.id)
    for user in users_guild:
        token = user['token']
        if not token:
            continue
        score, rate, likes, comments, slug = compute_pertinence_score(album['id'], token, avg_rate)
        if slug is None:
            u_info = api_users.me(ug['token'])
            slug = f"/{u_info['username']}"
        user['album_score'] = score
        user['album_rate'] = rate
        user['likes'] = likes
        user['comments'] = comments
        user['album_slug'] = slug
    
    users_guild = sorted(users_guild, key=lambda x: x['album_score'], reverse=True)
    users_guild = [u for u in users_guild if u['album_score'] > 0]
    users_rates_list = []
    max =  len(users_guild) if len(users_guild) <= 10 else 10
    for i in range(max):
        ug = users_guild[i]
        member = await guild.fetch_member(ug['discord_id'])
        if member.name == discord_name:
            user_name = f"**{member.display_name}**"
        else:
            user_name = member.display_name
        res = f"[{user_name}](https://musicboard.app{ug['album_slug']}): {ug['album_rate']}/5 - {ug['likes']} likes, {ug['comments']} comments"
        users_rates_list.append(res)
    
    if len(users_rates_list) == 0:
        display_ratings = "no one rated this album yet"
    else:
        display_ratings = "\n".join(users_rates_list)
    
    embed = embed_album(
        album_name=album['title'],
        album_artist=album['artist']['name'],
        guild_name=guild.name,
        album_url=f"https://musicboard.app{album['url_slug']}",
        album_cover=album['cover'],
        
        discord_name=discord_name,
        user_rate=user_rate,
        
        average_rate=avg_rate,
        rating_count=album['ratings_count'],
        release_date=album_date,
        
        ratings=display_ratings
    )
    
    return embed
        
    
        
def embed_album(album_name, album_artist, guild_name, album_url, album_cover,
                discord_name, user_rate,
                average_rate, rating_count, release_date,
                ratings
                ):
    guild_name_title = f"in {guild_name}" if guild_name else ""
    embed = Embed(
        title=f"{album_name} by {album_artist} {guild_name_title}",
        url=album_url
    )
    embed.set_thumbnail(url=album_cover)
    
    embed.add_field(
        name="your rate",
        value=f"**{str(discord_name)}**: {str(user_rate)}/5",
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
    if guild_name != "":
        embed.add_field(
            name=f"{guild_name}'s rating",
            value=ratings
        )
    
    return embed