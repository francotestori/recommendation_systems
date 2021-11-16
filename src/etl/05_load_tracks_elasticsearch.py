from utils import ROOT_DIR, read_pickle_file
from datasources.base import ElasticClient

tracks_genres = read_pickle_file(f'{ROOT_DIR}/results/tracks_genres.pickle')

ELASTICSEARCH = ElasticClient()
INDEX_NAME = 'tracks_genres'

ELASTICSEARCH.create_index(INDEX_NAME)
ELASTICSEARCH.bulk_store(tracks_genres)

