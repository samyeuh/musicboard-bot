import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/login/"

def get_token(username: str, password: str):
    """ get token of an musicboard user """
    
    payload = {
        "username": username,
        "password": password,
        "email": None
    }
    
    try:
        res = requests.post(BASE_URL, json=payload)
        res.raise_for_status()
        data = res.json()
        return data["auth_info"]["access_token"]

    except requests.RequestException:
        raise MBBException("get token exception!", f"error during token retrieval for user `{username}`")

