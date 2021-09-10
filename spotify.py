import requests
from creds import CLIENT_ID, CLIENT_SECRET

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    })

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'
CHARACTERISTICS = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

def get_audio_features(track_id):
    # actual GET request with proper header
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    return r.json()


def get_user_playlist_ids(user_id):
    # actual GET request with proper header
    r = requests.get(BASE_URL + 'users/' + user_id + "/playlists", headers=headers)
    ids = []
    for playlist in r.json()["items"]:
        ids.append(playlist["id"])
    return ids

def get_users_nth_playlist_id(user_id, n):
    return get_user_playlist_ids(user_id)[n]

def get_playlist_name(playlist_id):
    r = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers)
    return r.json()["name"]


def get_playlist_track_ids(playlist_id):
    r = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers)
    ids = []
    for track in r.json()["tracks"]["items"]:
        ids.append(track["track"]["id"])
    return ids

def get_playlist_vibes(playlist_id):
    tracks = get_playlist_track_ids(playlist_id)
    num_tracks = len(tracks)
    playlist_vibes = dict.fromkeys(CHARACTERISTICS, 0)
    tracks_string = ",".join(str(x) for x in tracks)
    r = requests.get(BASE_URL + 'audio-features' + '?ids=' + tracks_string, headers=headers)
    for track in r.json()["audio_features"]:
        for characteristic in CHARACTERISTICS:
            playlist_vibes[characteristic] = playlist_vibes[characteristic] + (track[characteristic] / num_tracks)
    return playlist_vibes


def get_vibes_for_all_playlists(user_id):
    vibes = []
    playlist_ids = get_user_playlist_ids(user_id)
    for playlist_id in playlist_ids:
        vibes.append(get_playlist_vibes(playlist_id))
    return vibes



