import requests
from exception.MBBException import MBBException

BASE_URL = "http://api.musicboard.app/v2/dz_tracks/"
DEEZER_URL = "https://api.deezer.com/search/track/"

def find_deezer_id(track_name):
    """ find the Deezer ID of a track by its name """
    
    deezer_params = {
        "q": track_name,
        "limit": 1
    }
    
    response = requests.get(DEEZER_URL, params=deezer_params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            track_data = data['data'][0]
            deezer_id = track_data['id']
            return deezer_id
        else:
            raise MBBException("no track found!", f"there are no tracks matching {track_name}")
    else:
        raise MBBException("error fetching track", "could not fetch track from Deezer")


def find_track(track_name):
    """ find an artist with a name"""
    try:
        deezer_id = find_deezer_id(track_name)
    except MBBException as e:
        return e.getMessage()
    
    response = requests.get(BASE_URL + str(deezer_id))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise MBBException("no tracks found!", f"there are no tracks matching {track_name}")