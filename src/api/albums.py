import requests
from exception.MBBException import MBBException

BASE_URL = "https://api.musicboard.app/v2/dz_albums/"
DEEZER_URL = "https://api.deezer.com/search/album/"

def find_deezer_id(album_name):
    """ find the Deezer ID of an album by its name """
    
    deezer_params = {
        "q": album_name,
        "limit": 1
    }
    
    response = requests.get(DEEZER_URL, params=deezer_params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            album_data = data['data'][0]
            deezer_id = album_data['id']
            return deezer_id
        else:
            raise MBBException("no album found!", f"there are no albums matching {album_name}")
    else:
        raise MBBException("error fetching album", "could not fetch album from Deezer")

def find_album(album_name):
    """ find an album with a name """
    
    try:
        deezer_id = find_deezer_id(album_name)
    except MBBException as e:
        return e.getMessage()
    
    response = requests.get(BASE_URL + str(deezer_id))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise MBBException("no album found!", f"there are no albums matching {album_name}")
    