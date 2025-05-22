import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/ratings/"

def last_five_reviews(musicboard_id):
    """Get the last 5 ratings from the Musicboard API."""
    
    params = {
        "creator": musicboard_id,
        "order_by": "-created_at",
        "limit": 5
    }
    
    res = requests.get(BASE_URL, params=params)
    
    if res.status_code == 200:
        data = res.json()
        return data["results"]
    else:
        return MBBException("last five reviews exception!", f"{res.text}")
        
        
def get_album_rated(album_id, token):
    """Get the ratings of the user from the Musicboard API."""
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    params = {
        "content_id": album_id,
        "limit": 1
    }
    
    res = requests.get(BASE_URL + "mine/", headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        return data["results"]
    else:
        return MBBException("get mine ratings exception!", f"{res.text}")
    