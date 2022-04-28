from constants import (EGG_GROUP_LABEL, NAME_LABEL, POKEMON_LABEL,
                       POKEMON_SPECIES_LABEL, RESULTS_LABEL, URL_LABEL,
                       WEIGHT_LABEL)
from utilities import (check_first_challenge_condition, fetch_concurrently,
                       fetch_data, is_first_generation_pokemon)


def first_challenge():
    '''
    Returns number of Pokemon that have 'at' substring and 2 'a' occurences.
    '''
    pokemon_data = fetch_data('https://pokeapi.co/api/v2/pokemon/?limit=-1')
    pokemon_data = pokemon_data[RESULTS_LABEL]
    filtered_pokemon = [
        pokemon for pokemon in pokemon_data if check_first_challenge_condition(pokemon)]
    return len(filtered_pokemon)


def second_challenge():
    '''
    Returns number of Pokemon species that can procreate with Raichu.
    '''
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


def third_challenge():
    '''
    Returns min and max weight of first generation fighting type Pokemon.
    '''
    fighting_data = fetch_data(
        'https://pokeapi.co/api/v2/type/fighting')
    fighting_pokemon = fighting_data[POKEMON_LABEL]
    pokemon_urls = []
    for pokemon in fighting_pokemon:
        pokemon_url = pokemon[POKEMON_LABEL][URL_LABEL]
        if is_first_generation_pokemon(pokemon_url):
            pokemon_urls.append(pokemon_url)
    pokemon_responses = fetch_concurrently(pokemon_urls)
    pokemon_weights = [pokemon_data[WEIGHT_LABEL]
                       for pokemon_data in pokemon_responses]
    return [max(pokemon_weights), min(pokemon_weights)]
