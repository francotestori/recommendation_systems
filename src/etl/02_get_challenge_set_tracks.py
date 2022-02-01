import json
from utils import ROOT_DIR, write_pickle_file, write_csv_file

CHALLENGE_SET_PATH = f"{ROOT_DIR}/challenge/data/challenge_set.json"
OS_PATH = f'{ROOT_DIR}/results'

pid_track_uris_for_csv = []
pid_track_uris = {}
with open(CHALLENGE_SET_PATH, 'rt') as challenge_set_file:
    challenge_set_data = json.load(challenge_set_file)

    for playlist in challenge_set_data['playlists']:
        pid = playlist['pid']

        playlist_tracks = []
        for track in playlist['tracks']:
            track_uri = track['track_uri'].replace("spotify:track:", "")
            playlist_tracks.append(track_uri)

            pid_track_uris_for_csv.append({
                'pid': pid,
                'track_uri': track_uri
            })
        if not playlist_tracks:
            pid_track_uris_for_csv.append({
                'pid': pid,
                'track_uri': None
            })

        pid_track_uris[pid] = playlist_tracks

write_pickle_file(
    filename=f'{OS_PATH}/challenge_set.pickle',
    data=pid_track_uris
)

write_csv_file(
    filename=f'{ROOT_DIR}/data/mdp_challenge_set.csv',
    field_headers=['pid', 'track_uri'],
    data=pid_track_uris_for_csv
)