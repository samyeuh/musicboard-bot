import math
from api import artists
from api import ratings
from db import users as db_users
from db import user_guilds
from discord import Embed
from exception.MBBException import MBBException

def compute_pertinence_score(artist_id, user_token, avg_rate):
    if not artist_id:
        return -1, -1, -1, -1, None
    artist = ratings.get_artist_rated(artist_id, user_token)
    if not artist:
        return -1, -1, -1, -1, None
    rating = artist['rating']
    likes = artist['like_count']
    comments = artist['comment_count']
    impressions = artist["impression_count"]
    slug = artist["review_url_slug"]

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

async def get_embed_info(query, discord_user, discord_guild):
    artist = artists.find_artist(query)
    if not artist:
        return MBBException("artist not found", "there are no artists matching your query").getMessage()
    
    artist_name = artist['name']
    artist_url = f"https://musicboard.app{artist['url_slug']}"
    artist_cover = artist['picture']
    artist_rating_count = artist['ratings_count']
    artist_average_rate = artist['average_rating']
    artist_average_rate = math.floor(artist_average_rate / 2 * 10) / 10
    
    
    u = db_users.get_user(discord_user.id)
    _, token, _ = u
    user_rate = ratings.get_artist_rated(artist['id'], token)
    
    if user_rate:
        rating = user_rate['rating']
        rating = math.floor(rating / 2 * 10) / 10
        if rating.is_integer():
            rating = str(int(rating))
        else:
            rating = str(rating)
        user_rate = f"{rating}/5"
    else:
        user_rate = "unrated"
    
    if not discord_guild:
        return embed_artist(
            artist_name=artist_name,
            artist_url=artist_url,
            guild_name="",
            artist_cover=artist_cover,
            discord_name=discord_user.display_name,
            user_rate=user_rate,
            average_rate=artist_average_rate,
            rating_count=artist_rating_count,
            display_ratings=""
        )
        
    users_guild = user_guilds.get_users_in_guild(discord_guild.id)
    for user in users_guild:
        token = user['token']
        if not token:
            continue
        score, rate, likes, comments, slug = compute_pertinence_score(artist['id'], token, artist_average_rate)
        if slug is None and likes > 0:
            u_info = artists.me(user['token'])
            slug = f"/{u_info['username']}"
        user['artist_score'] = score
        user['artist_rate'] = rate
        user['likes'] = likes
        user['comments'] = comments
        user['artist_slug'] = slug
    
    users_guild = sorted(users_guild, key=lambda x: x['artist_score'], reverse=True)
    users_guild = [u for u in users_guild if u['artist_score'] > 0]
    users_rates_list = []
    max =  len(users_guild) if len(users_guild) <= 10 else 10
    for i in range(max):
        ug = users_guild[i]
        member = discord_guild.get_member(ug['discord_id']) 
        if not member:
            member = await discord_guild.fetch_member(ug['discord_id']) 
        is_sender = member.display_name == discord_user.display_name
        if is_sender:
            res = f"**[{member.display_name}](https://musicboard.app{ug['artist_slug']}): {ug['artist_rate']}/5 - _{ug['likes']} likes, {ug['comments']} comments_**"
        else:
            res = f"[{member.display_name}](https://musicboard.app{ug['artist_slug']}): {ug['artist_rate']}/5 - _{ug['likes']} likes, {ug['comments']} comments_"

        users_rates_list.append(res)
    
    if len(users_rates_list) == 0:
        display_ratings = f"no one rated **{artist['name']}** yet"
    else:
        display_ratings = "\n".join(users_rates_list)

    
    
    return embed_artist(
            artist_name=artist_name,
            artist_url=artist_url,
            guild_name=discord_guild.name,
            artist_cover=artist_cover,
            discord_name=discord_user.display_name,
            user_rate=user_rate,
            average_rate=artist_average_rate,
            rating_count=artist_rating_count,
            display_ratings=display_ratings
        )
    
    
def embed_artist(artist_name, artist_url, guild_name,
                 artist_cover, 
                 discord_name, user_rate, 
                 average_rate, rating_count,
                 display_ratings):
    
    in_server = f"in {guild_name}" if guild_name != "" else ""
    embed = Embed(
        title=f"{artist_name} {in_server}",
        url=artist_url
    )
    
    embed.set_thumbnail(url=artist_cover)
    
    embed.add_field(
        name="your rate",
        value=f"**{str(discord_name)}**: {str(user_rate)}",
        inline=True
    )
    
    embed.add_field(
        name="                ",
        value="                                                                  ",
        inline=True
    )
    
    embed.add_field(
        name="artist info",
        value=(
            f"average rate: {average_rate} \n"
            f"rating count: {rating_count} \n"
        ),
        inline=True
    )
    
    if guild_name != "":
        embed.add_field(
            name=f"{guild_name}'s rating",
            value=display_ratings,
            inline=True
        )
        
    return embed
    
    