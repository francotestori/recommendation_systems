from utils import ROOT_DIR, read_pickle_file, write_pickle_file
from models.base import PlaylistProfile

CHALLENGE_SET_FILE_PATH = f'{ROOT_DIR}/results/challenge_set.pickle'
TRACKS_GENRES_FILE_PATH = f'{ROOT_DIR}/results/tracks_genres.pickle'
OS_PATH = f'{ROOT_DIR}/results'

challenge_set = read_pickle_file(CHALLENGE_SET_FILE_PATH)
tracks_genres = read_pickle_file(TRACKS_GENRES_FILE_PATH)

playlist_profiles = {}
for pid, tracks in challenge_set.items():
    if tracks:
        genres = [tracks_genres[track].genres for track in tracks]
    else:
        genres = []

    playlist_profiles[pid] = PlaylistProfile(
        pid=pid,
        tracks=tracks,
        genres=genres
    )

write_pickle_file(
    filename=f'{OS_PATH}/challenge_set_profile.pickle',
    data=playlist_profiles
)




