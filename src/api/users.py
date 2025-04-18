import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/users/"

def exists(username: str):
    """ returns true if  the given user exists """
    params = {
        "username": username
    }
    
    res = requests.get(BASE_URL + "exists/", params=params)
    
    if res.status_code == 200:
        data = res.json()
        return data["status"]["exists"]
    else:
        return MBBException("exists exception!", f"error when trying to verify if exists {username}")
        

def get_uid(username: str):
    """ search for a musicboard user by username """
    params = {
        "username": username,
    }
    
    try:
        res = requests.post(BASE_URL + "get_uid/", json=params)
        res.raise_for_status()
        data = res.json()
        return data["uid"]  
    except Exception as e:
        raise MBBException("search user exception!", f"error when trying to search user {username} :c")
    
    

    