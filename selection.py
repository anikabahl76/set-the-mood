import requests
from spotify import *
from creds import CLIENT_ID, CLIENT_SECRET

def find_playlist_from_user_library(username, track):
    all_playlists_vibes = get_vibes_for_all_playlists(username)
    track_vibes = get_audio_features(track)
    distances = []
    for playlist_vibes in all_playlists_vibes:
        distances.append(distance(track_vibes, playlist_vibes))
    min_index = distances.index(min(distances))
    min_playlist_id = get_users_nth_playlist_id(username, min_index)
    min_playlist_name = get_playlist_name(min_playlist_id)
    return min_playlist_name
    
def distance(track, playlist):
    total_dist = 0
    for characteristic in CHARACTERISTICS:
        total_dist += (track[characteristic] - playlist[characteristic])**2
    return total_dist

print(find_playlist_from_user_library("anikabahl76", "2m6Ko3CY1qXNNja8AlugNc"))





