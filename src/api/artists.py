import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/dz_artists/"
DEEZER_URL = "https://api.deezer.com/search/artist/"

def find_deezer_id(artist_name):
    """ find the Deezer ID of an artist by its name """
    
    deezer_params = {
        "q": artist_name,
        "limit": 1
    }
    
    response = requests.get(DEEZER_URL, params=deezer_params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            artist_data = data['data'][0]
            deezer_id = artist_data['id']
            return deezer_id
        else:
            raise MBBException("no artist found!", f"there are no artists matching {artist_name}")
    else:
        raise MBBException("error fetching artist", "could not fetch artist from Deezer")


def find_artist(artist_name):
    """ find an artist with a name"""
    
    try:
        deezer_id = find_deezer_id(artist_name)
    except MBBException as e:
        return e.getMessage()
    
    response = requests.get(BASE_URL + str(deezer_id))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise MBBException("no artist found!", f"there are no artists matching {artist_name}")