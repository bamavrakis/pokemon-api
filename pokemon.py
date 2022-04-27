import requests

def at_counter(string):
    a_counter = 0
    has_at_substring = False
    latest_character = None
    for character in string:
        if character == 'a': 
            a_counter += 1
        if latest_character == 'a' and character == 't': 
            latest_character = character
    return a_counter == 2 and has_at_substring

def is_first_generation_pokemon(url):
    split_url = url.split('/')
    pokemon_id = int(split_url[-2])
    return pokemon_id <= 151

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.HTTPError as error:
        print("There is an error connecting to the API. Please try again later.")
        return

def pregunta_1():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1126')
    response_data = response.json()
    pokemons = response_data['results']
    pokemon_count = 0 
    for pokemon in pokemons:
        pokemon_name = pokemon['name']
        if at_counter(pokemon_name):
            pokemon_count += 1
    return pokemon_count

def pregunta_2():
    raichu_data = fetch_data(
        'https://pokeapi.co/api/v2/pokemon-species/raichu')
    egg_groups = raichu_data['egg_groups']
    pokemon_species_names = []
    for egg_group in egg_groups:
        egg_group_url = egg_group['url']
        egg_group_response = requests.get(egg_group_url)
        egg_group_data = egg_group_response.json()
        pokemon_species = egg_group_data['pokemon_species']
        for species in pokemon_species:
            pokemon_species_names.append(species['name'])
    return len(list(set(pokemon_species_names)))


def pregunta_3():
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
