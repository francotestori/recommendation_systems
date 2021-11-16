from typing import List


class PlaylistProfile:
    def __init__(self, pid: str, tracks: List[str], genres: List[List[str]] = None) -> None:
        self.pid = pid
        self.tracks = tracks
        self.genres = genres


class ArtistMetadata:

    def __init__(self, artist_uri: str, genres: List[str], popularity: int, followers: int) -> None:
        self.artist_uri = artist_uri
        self.genres = genres
        self.popularity = popularity
        self.followers = followers


class TrackGenre:

    def __init__(self, track_uri: str, genres: List[str], popularity: int, followers: int, interactions: int) -> None:
        self._id = track_uri
        self.track_uri = track_uri
        self.genres = genres
        self.popularity = popularity
        self.followers = followers
        self.interactions = interactions
