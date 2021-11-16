import gzip
import tqdm
from collections import abc
from typing import List
from abc import ABC, abstractmethod
from utils import  ROOT_DIR, read_pickle_file
from constants import TRACKS_CAP


def _recommendations_output_storage(strategy_name: str, recommendations: dict, progress: tqdm.std):
    os_path = f'{ROOT_DIR}/results/{strategy_name}_submission.csv.gz'

    with gzip.open(os_path, 'wt') as submit_file:
        _ = submit_file.write("team_info,francotestori,franco.testori@hotmail.com\n")
        for pid, tracks in recommendations.items():
            _ = submit_file.write(f"{pid},{','.join(tracks)}\n")
            progress.update(1)


class Strategy(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.strategy_name = self._strategy_name()

    def execute(self):
        challenge_set = self._retrieve_challenge_tracks()

        recommendation_progress = tqdm.tqdm(unit="docs", total=len(challenge_set.items()))
        recommendations = self._add_recommendations(challenge_set, progress=recommendation_progress)

        os_progress = tqdm.tqdm(unit="docs", total=len(recommendations.items()))
        _recommendations_output_storage(
            strategy_name=self.strategy_name,
            recommendations=recommendations,
            progress=os_progress
        )

    @abstractmethod
    def _strategy_name(self) -> str:
        pass

    @abstractmethod
    def _retrieve_challenge_tracks(self) -> dict:
        pass

    @abstractmethod
    def _add_recommendations(self, challenge_tracks: dict, progress: tqdm.std) -> dict:
        pass


class BaselineStrategy(Strategy):

    def _strategy_name(self) -> str:
        return 'top_interactions'

    def _retrieve_challenge_tracks(self) -> dict:
        challenge_tracks_file = f'{ROOT_DIR}/results/challenge_set.pickle'
        return read_pickle_file(challenge_tracks_file)

    @staticmethod
    def _retrieve_sorted_popular_tracks() -> List[abc.ItemsView]:
        popular_tracks_file = f'{ROOT_DIR}/results/tracks_interaction_count.pickle'
        popular_tracks = read_pickle_file(popular_tracks_file)
        return sorted(
            popular_tracks.items(),
            key=lambda track: track[1],
            reverse=True
        )

    def _add_recommendations(self, challenge_tracks: dict, progress: tqdm.std) -> dict:
        popular_tracks = self._retrieve_sorted_popular_tracks()

        recommendations = {}
        for pid, tracks in challenge_tracks.items():
            recommended_tracks = []
            for p_track, count in popular_tracks:
                if p_track in tracks:
                    continue

                recommended_tracks.append(f'spotify:track:{p_track}')
                if len(recommended_tracks) == TRACKS_CAP:
                    break
            recommendations[pid] = recommended_tracks
            progress.update(1)

        return recommendations
