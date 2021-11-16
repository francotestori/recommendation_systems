import ssl
import tqdm
from typing import List

from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
from elasticsearch.helpers import streaming_bulk


INDEX_NAME = 'tracks_genres'
TRACKS_CAP = 500
TOP_500_QUERY = {
    'sort': [
        {
            'interactions': {
                'order': 'desc'
            }
        },
    ],
    "query": {
        "match_all": {}
    }
}


def _open_distro_ssl_context() -> ssl.SSLContext:
    open_distro_ssl_context = create_ssl_context()

    # next two lines are if you're running localhost with a self-signed cert (aka docker)
    open_distro_ssl_context.check_hostname = False
    open_distro_ssl_context.verify_mode = ssl.CERT_NONE

    return open_distro_ssl_context


class ElasticClient:

    def __init__(self) -> None:
        super().__init__()
        self.ssl_context = _open_distro_ssl_context()
        self.client = Elasticsearch(
            scheme="https",
            hosts=[{
                'port': 9200,
                'host': 'localhost'
            }],
            ssl_context=self.ssl_context,
            http_auth=("admin", "admin"),
            verify_certs=False
        )

    def create_index(self, name: str):
        self.client.indices.create(name, ignore=400)

    @staticmethod
    def _generate_actions(tracks_genres: dict):
        """Reads the file through csv.DictReader() and for each row
        yields a single document. This function is passed into the bulk()
        helper to create many documents in sequence.
        """
        for track_uri, track_genre in tracks_genres.items():
            doc = track_genre.__dict__
            yield doc

    def bulk_store(self, tracks_genres: dict):
        number_of_docs = len(tracks_genres)
        print("Indexing documents...")
        progress = tqdm.tqdm(unit="docs", total=number_of_docs)
        successes = 0
        for ok, action in streaming_bulk(
                client=self.client,
                index="tracks_genres",
                actions=self._generate_actions(tracks_genres)
        ):
            progress.update(1)
            successes += ok
        print(f"Indexed {successes}/{number_of_docs}documents")

    def _execute_query(self, query: dict, size: int = 500):
        results = self.client.search(
            index=INDEX_NAME,
            body=query,
            size=size
        )
        return results

    def query_top_500_tracks(self) -> List[str]:
        results = self._execute_query(
            query=TOP_500_QUERY
        )

        top_500_tracks = []
        for hit in results['hits']['hits']:
            _id = hit['_id']
            top_500_tracks.append(f'spotify:track:{_id}')

        return top_500_tracks

    @staticmethod
    def _flatten(t: List[List[str]]) -> List[str]:
        return [item for sublist in t for item in sublist]

    @staticmethod
    def _genre_to_bool_query_clause(genre: str) -> dict:
        return {
            'match': {
                'genres': genre
            }
        }

    def query_genres(self, genres: List[List[str]], size: int, exclusions: List[str]) -> List[str]:
        flattened = self._flatten(genres)
        unique_genres = list(set(flattened))

        genres_clauses = [self._genre_to_bool_query_clause(genre=genre) for genre in unique_genres]
        query = {
            'sort': [
                {
                    'interactions': {
                        'order': 'desc'
                    }
                },
            ],
            "query": {
                "bool": {
                    'should': genres_clauses
                }
            }
        }

        results = self._execute_query(
            query=query,
            size=size
        )

        tracks = []
        for hit in results['hits']['hits']:
            _id = hit['_id']

            if _id in exclusions:
                continue

            tracks.append(f'spotify:track:{_id}')
            if len(tracks) == TRACKS_CAP:
                break

        return tracks
