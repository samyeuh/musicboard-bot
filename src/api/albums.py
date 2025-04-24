import requests
from exception.MBBException import MBBException

BASE_URL = "https://api.musicboard.app/v2/albums/"

def find_album(album_name):
    """ find an album with a name"""
    
    params = {
        "title__icontains": album_name,
        "order_by": "-average_rating",
        "order_by": "-ratings_count"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise MBBException("no album found!", f"there are no albums matching {album_name}")
    