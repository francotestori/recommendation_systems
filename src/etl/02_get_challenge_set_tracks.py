import json
from utils import ROOT_DIR, write_pickle_file

CHALLENGE_SET_PATH = f"{ROOT_DIR}/challenge/data/challenge_set.json"
OS_PATH = f'{ROOT_DIR}/results'


pid_track_uris = {}
with open(CHALLENGE_SET_PATH, 'rt') as challenge_set_file:
    challenge_set_data = json.load(challenge_set_file)

    for playlist in challenge_set_data['playlists']:
        pid = playlist['pid']

        playlist_tracks = []
        for track in playlist['tracks']:
            track_uri = track['track_uri'].replace("spotify:track:", "")
            playlist_tracks.append(track_uri)

        pid_track_uris[pid] = playlist_tracks

write_pickle_file(
    filename=f'{OS_PATH}/challenge_set.pickle',
    data=pid_track_uris
)
