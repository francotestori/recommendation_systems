PLAYLISTS_FIELDS = [
    'pid',
    'name',
    'description',
    'collaborative',
    'modified_at',
    'num_albums',
    'num_tracks',
    'num_followers',
    'num_edits',
    'num_artists',
    'duration_ms',
]

TRACKS_FIELDS = [
    'track_uri',
    'artist_name',
    'artist_uri',
    'track_name',
    'album_uri',
    'album_name',
    'duration_ms'
]

INTERACTIONS_FIELDS = [
    'pid',
    'track_uri',
    'pos'
]

GENRES_FIELDS = [
    'track_uri',
    'genres'
]

TRACKS_CAP = 500
