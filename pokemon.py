from concurrent.futures import ThreadPoolExecutor
import requests

EGG_GROUP_LABEL = 'egg_groups'
MAX_WORKERS = 20
NAME_LABEL = 'name'
POKEMON_SPECIES_LABEL = 'pokemon_species'
RESULTS_LABEL = 'results'
URL_LABEL = 'url'


def is_first_generation_pokemon(url):
    split_url = url.split('/')
    pokemon_id = int(split_url[-2])
    return pokemon_id <= 151

def check_pokemon(pokemon):
    pokemon_name = pokemon[NAME_LABEL]
    return 'at' in pokemon_name and pokemon_name.count('a') == 2

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.HTTPError as error:
        print("There is an error connecting to the API. Please try again later.")
        return

def fetch_concurrently(urls):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        responses = list(executor.map(fetch_data, urls))
        return responses

def first_question():
    pokemon_data = fetch_data('https://pokeapi.co/api/v2/pokemon/?limit=-1')
    pokemon_data = pokemon_data[RESULTS_LABEL]
    filtered_pokemon = [pokemon for pokemon in pokemon_data if check_pokemon(pokemon)]
    return len(filtered_pokemon)

def second_question():
    raichu_data = fetch_data(
        'https://pokeapi.co/api/v2/pokemon-species/raichu')
    egg_groups = raichu_data[EGG_GROUP_LABEL]
    urls = [egg_group[URL_LABEL] for egg_group in egg_groups]
    pokemon_names = []
    pokemon_responses = fetch_concurrently(urls)
    for response in pokemon_responses:
        pokemon_species = response[POKEMON_SPECIES_LABEL]
        pokemon_names += [pokemon[NAME_LABEL] for pokemon in pokemon_species]
    return len(list(set(pokemon_names)))

def third_question():
    fighting_data = fetch_data(
        'https://pokeapi.co/api/v2/type/fighting')
    fighting_pokemon = fighting_data['pokemon']
    min_weight = None
    max_weight = None
    for pokemon in fighting_pokemon:
        pokemon_url = pokemon['pokemon']['url']
        if is_first_generation_pokemon(pokemon_url):
            pokemon_response = requests.get(pokemon_url)
            pokemon_data = pokemon_response.json()
            weight = pokemon_data['weight']
            if not min_weight and not max_weight:
                min_weight = max_weight = weight
                continue
            if weight < min_weight:
                min_weight = weight
            if weight > max_weight:
                max_weight = weight
    return [max_weight, min_weight]
