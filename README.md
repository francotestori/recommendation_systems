# Recommendation Systems 
## Spotify MDP Challenge

The following project is part of the course on Recommendation Systems from the Universidad of Buenos Aires course.

For this course, we are requested to submit recommendations for the [Spotify MDP Challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge).

## Project Setup
After downloading this project you should create a new python virtual environment (Python 3.8.8+) and install all the required dependencies.
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Project Structure
The project structure follows this tree structure.
```
├── README.md
├── docker-compose.yml
├── requirements.txt
├── challenge
│   ├── README.md
│   ├── data
│   │   ├── challenge_set.json
│   │   ├── challenge_set_pickle.pickle
│   │   └── sample_submission.csv
│   └── utils
│       ├── check.py
│       └── verify_submission.py
├── data
│   ├── artists.csv
│   ├── artists.csv.gz
│   └── mdp
│       └── all_mdp_json_files
├── results
└── src
    ├── datasources
    │   ├── __init__.py
    │   └── base.py
    ├── etl
    │   ├── 01_process_mdp_data.py
    │   ├── 02_get_challenge_set_tracks.py
    │   ├── 03_interactions_counter.py
    │   ├── 04_genres.py
    │   ├── 05_load_tracks_elasticsearch.py
    │   ├── 06_playlists_profile.py
    │   └── __init__.py
    ├── models
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-38.pyc
    │   │   └── base.cpython-38.pyc
    │   └── base.py
    ├── strategies
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-38.pyc
    │   │   └── base.cpython-38.pyc
    │   ├── base.py
    │   └── profile.py
    ├── constants.py
    ├── utils.py
    └── main.py
```

On the **challenge** directory, we store competititon's challenge.zip files.
On the **data** directory we store artist metadata (extracted from Spotify's API) & all mdp files (we did not upload them because it is a lot of data).
On the **results** directory we will store our processes outputs.
The source of our projects has:
- a **models** package where we store our data class definitions
- an **etl** package where we store our data wrangling scripts
- a **datsources** package where we store our elasticsearch customized client implementation
- a **strategies** package where we store our submission strategies scripts

## How to run
### Baseline Strategy
In order to run the baseline strategy you will need to execute the first 3 ETL scripts and the from a python console you can execute the strategy as following:
```python
from strategies.base import BaselineStrategy
strategy = BaselineStrategy()
strategy.execute()
```
### Profile Strategy
In order to run the profile strategy you will need to have our elasticsearch client up and running, as a first step. You can do these by executing the following docker command (Check your [Docker Installation](https://www.docker.com/get-started))
```shell
docker compose up --build -d
```
You can later, validate that elasticsearch is up & running with the following command.
```shell
curl -XGET https://localhost:9200 -u 'admin:admin' --insecure
```
After you have elasticsearch database running, you can execute ETL scripts 4 to 6. 
Finally you can execute the strategy as following:
```python
from strategies.profile import ProfileStrategy
strategy = ProfileStrategy()
strategy.execute()
```