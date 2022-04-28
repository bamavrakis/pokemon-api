from concurrent.futures import ThreadPoolExecutor
import requests
from constants import MAX_WORKERS, NAME_LABEL


def check_first_challenge_condition(pokemon):
    '''
    Returns boolean indicating if Pokemon has 'at' substring and
    2 'a' occurences.
    '''
    pokemon_name = pokemon[NAME_LABEL]
    return 'at' in pokemon_name and pokemon_name.count('a') == 2


def fetch_concurrently(urls):
    '''
    Returns a list of responses from concurrent queries.
    '''
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        responses = list(executor.map(fetch_data, urls))
        return responses


def fetch_data(url):
    '''
    Returns a response from a simple query. 
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)


def is_first_generation_pokemon(url):
    '''
    Returns boolean indicating if Pokemon is of first generation.
    '''
    split_url = url.split('/')
    pokemon_id = int(split_url[-2])
    return pokemon_id <= 151
