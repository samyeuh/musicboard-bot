import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/users/"

def search_user(username: str):
    """ search for a musicboard user by username """
    params = {
        "username": username,
    }
    
    res = requests.get(BASE_URL, params=params)
    
    if res.status_code == 200:
        data = res.json()
        return data["results"]
    else:
        raise MBBException("search user exception!", f"error when trying to search user {username} :c")   
    