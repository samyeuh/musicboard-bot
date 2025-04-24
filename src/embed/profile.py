from discord import Embed
import db
from api import ratings, users
from discord.ui import View, Button
import db.users
from exception.MBBException import MBBException
import math


emoji_type = {
    "album": "<:album_mbb:1363118455687221499>",
    "track": "<:track_mbb:1363118430030663751>",
    "artist": "<:artist_mbb:1363118402570424473>",
    "star": "<a:star_mbb:1363119049621635145>",
    "musicboard": "<:musicboard:1363191447066771699>",
    "follow": "<:follow:1363190056747012258>",
    "heart": "<:heart:1363188522974056529>",
    "contributions": "<:contributions:1363191275335057701>",
    "twitter": "<:twitter:1363226841413980381>",
    "website": "<:website:1363228936967819324>",
    "reviews": "<:reviews:1363621120569249842>",
    "info": "<:info:1363621433137299638>",
    "stats": "<:stats:1363622617168351312>",
    "pro": "<:pro:1363624129739231386>"
}


def transform_rates(counts):
    counts = [c or 0 for c in counts]
    
    max_display = 5
    max_count = max(counts) or 1
    scaled = [
        math.ceil((c / max_count) * max_display) if c < max_count / 2
        else round((c / max_count) * max_display)
        for c in counts
    ]
    
    block = "■"
    cell_width = 3

    lines = []
    for level in reversed(range(1, max_display + 1)):
        line = ""
        for val in scaled:
            content = block if val >= level else " "
            line += content.center(cell_width)
        lines.append(line.rstrip())

    labels = ""
    for i in range(10):
        label = str((i + 1) / 2).rstrip("0").rstrip(".")
        labels += label.center(cell_width)
    lines.append(labels.rstrip())

    return "\n".join(lines)

def get_embed_info(discord_id, discord_name):
    user_info = db.users.get_user(discord_id)
    if not user_info:
        raise MBBException("exception", "flm")
    musicboard_id, access_token, _ = db.users.get_user(discord_id)
    users_info = users.me(access_token)
    five_ratings = ratings.last_five_reviews(musicboard_id)
    
    ratings_list = []
    for rat in five_ratings:
        
        type = rat["content"]["type"]
        rate_doubled = rat["rating"]
        
        rate = rate_doubled/2
        if rate.is_integer():
            display_rate = f"{str(int(rate))}   " 
        else:
            display_rate = str(rate)
        
        if type == "artist":
            res = f"{emoji_type['star']} **{display_rate}** /5 {emoji_type[type]} **{rat['content']['name']}**"
        else:
            res = f"{emoji_type['star']} **{display_rate}** /5 {emoji_type[type]} {rat['content']['artist']['name']} - **{rat['content']['title']}**"
        
        ratings_list.append(res)
    
    display_ratings = "\n".join(ratings_list)

    rates_tab = transform_rates(users_info['rating_counts'])

    embed = embed_profile(
            bio=users_info["biography"], 
            discord_name=discord_name, 
            musicboard_pp=users_info["profile_picture"], 
            musicboard_banner=users_info["background"],
            is_pro=users_info["is_pro"],
            
            musicboard_name=users_info["name"],
            musicboard_link=f"https://musicboard.app/{users_info['username']}",
            nb_following=users_info["counts"]["follows"] if users_info["counts"]["follows"] else 0,
            nb_followers=users_info["counts"]["followed_by"] if users_info["counts"]["followed_by"] else 0,
            nb_like=users_info["counts"]["likes"] if users_info["counts"]["likes"] else 0,
            nb_contributions=users_info["counts"]["contributions"],
            
            rating_set=users_info["counts"]["rating_set"] if users_info["counts"]["rating_set"] else 0,
            rated_album=users_info["counts"]["rated_albums"] if users_info["counts"]["rated_albums"] else 0,
            rated_artists=users_info["counts"]["rated_artists"] if users_info["counts"]["rated_artists"] else 0,
            rated_tracks=users_info["counts"]["rated_tracks"] if users_info["counts"]["rated_tracks"] else 0,
            want_list=users_info["counts"]["want_list"] if users_info["counts"]["want_list"] else 0,
            
            ratings=display_ratings,
            
            rates_tab=rates_tab
        )
    view = View()
    if users_info['twitter']:
        view.add_item(Button(
            label="twitter",
            url=f"https://x.com/{users_info['twitter']}",
            emoji=emoji_type['twitter']
        ))
    
    if users_info['website']:
        view.add_item(Button(
            label="website",
            url=users_info['website'],
            emoji=emoji_type['website']
        ))

    
    return embed, view

def embed_profile(bio, discord_name, musicboard_pp, musicboard_banner, is_pro,
                  musicboard_name, musicboard_link, nb_following, nb_followers, nb_like, nb_contributions, 
                  rating_set, rated_album, rated_artists, rated_tracks, want_list, 
                  ratings,
                  rates_tab):
    """ embed musicboard profil  """
    
    embed = Embed(title="", description=bio)
    embed.set_author(name=f"profil of {discord_name} {emoji_type['pro'] if is_pro else ''}", icon_url=None, url=None)
    embed.set_thumbnail(url=musicboard_pp)
    if musicboard_banner:
        embed.set_image(musicboard_banner)
    
    embed.add_field(
        name=f"{emoji_type['info']} info",
        value=(
            f"{emoji_type['musicboard']} **[{musicboard_name}]({musicboard_link})** \n"
            f"{emoji_type['follow']} **{nb_followers}** followers \n"
            f"{emoji_type['follow']} **{nb_following}** following \n"
            f"{emoji_type['heart']} **{nb_like}** likes \n"
            f"{emoji_type['contributions']} **{nb_contributions}** contributions"
        ),
        inline=True
    )
    
    embed.add_field(
        name=f"{emoji_type['stats']} stats",
        value=(
            f"**{rating_set}** ratings \n"
            f"**{rated_album}** album rated \n"
            f"**{rated_artists}** artist rated \n"
            f"**{rated_tracks}** tracks rated \n"
            f"**{want_list}** in listen later \n"
        ),
        inline=True
    )
    
    embed.add_field(
        name="",
        value="",
        inline=False
    )
    
    embed.add_field(
        name=f"{emoji_type['reviews']} last five ratings",
        value=ratings,
        inline=False
    )
    
    
    embed.add_field(
        name=f"{emoji_type['star']} rates",
        value=f"```{rates_tab}```",
        inline=False
    )
    
    return embed
    