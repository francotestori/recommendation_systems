import tqdm
from datasources.base import ElasticClient
from base import Strategy
from utils import ROOT_DIR, read_pickle_file
from constants import TRACKS_CAP


class ProfileStrategy(Strategy):

    def __init__(self) -> None:
        super().__init__()
        self.elastic_client = ElasticClient()
        self.top_500_tracks = self.elastic_client.query_top_500_tracks()

    def _strategy_name(self) -> str:
        return 'genre_profiled'

    def _retrieve_challenge_tracks(self) -> dict:
        challenge_tracks_file = f'{ROOT_DIR}/results/challenge_set_profile.pickle'
        return read_pickle_file(challenge_tracks_file)

    def _add_recommendations(self, challenge_tracks: dict, progress: tqdm.std) -> dict:
        recommendations = {}
        for pid, profile in challenge_tracks.items():
            tracks = profile.tracks

            if tracks:
                size = TRACKS_CAP + len(tracks)
                recommended_tracks = self.elastic_client.query_genres(
                    genres=profile.genres,
                    size=size,
                    exclusions=tracks
                )
            else:
                recommended_tracks = self.top_500_tracks

            if len(recommended_tracks) < TRACKS_CAP:
                tracks = [f'spotify:track:{t}' for t in tracks]
                for track in self.top_500_tracks:
                    if track not in tracks and track not in recommended_tracks:
                        recommended_tracks.append(track)
                    if len(recommended_tracks) == TRACKS_CAP:
                        break

            recommendations[pid] = recommended_tracks
            progress.update(1)

        return recommendations
