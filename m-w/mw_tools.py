#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Dictionary API
# Powered by Merriam-Webster's Collegiate® Thesaurus API
# https://dictionaryapi.com/
#
import os
import requests
import sys

import keys # Local keys file

PRODUCT_THESAURUS = 'Merriam-Webster\'s Collegiate® Thesaurus'
API_THESAURUS = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/'
KEY_THESAURUS = keys.MW_THESAURUS
SRC_THESAURUS = 'coll_thes'
CACHE_THES = 'cache-thes/'

def url_thesaurus(word: str) -> str:
    return f'{API_THESAURUS}{word}?key={KEY_THESAURUS}'


def thesaurus_request(word: str):
    response = requests.get(url_thesaurus(word))
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={KEY_THESAURUS} is correct for API {API_THESAURUS}', file=sys.stderr, flush=True)
    elif response:  # Evaluates to True for status codes < 400
        data = response.json()
        if not isinstance(data, list):
            print(f'ERROR: returned data is not a list', file=sys.stderr, flush=True)
        elif isinstance(data[0], str):
            print(f'ERROR: "{word}" NOT FOUND: did you mean any of these?\n{data[:10]}', file=sys.stderr, flush=True)
        elif not isinstance(data[0], dict):
            print(f'ERROR: returned data[0] is not a dict', file=sys.stderr, flush=True)
        else:
            if (not 'meta' in data[0]) or (not 'src' in data[0]['meta']) or (data[0]['meta']['src'] != SRC_THESAURUS):
                print(f'WARNING: returned data is not from expected source: {SRC_THESAURUS}', file=sys.stderr, flush=True)
        
            print(response.text)
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)


def thesaurus_cache(word: str):
    path_not_found = f'{CACHE_THES}{word}.not-found'
    path_json = f'{CACHE_THES}{word}.json'
    
    if os.path.exists(path_not_found):
        print(f'Path exists: {path_not_found}, not requesting.', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    
    if os.path.exists(path_json):
        print(f'Path exists: {path_json}, not requesting.', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    
    print(f'Requesting thesaurus listing for: "{word}"', file=sys.stderr, flush=True)

    response = requests.get(url_thesaurus(word))
    #exit(f'DEZ! {response}\nHEADERS:{response.headers}\nTEXT:{response.text}')
    
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={KEY_THESAURUS} is correct for API {API_THESAURUS}', file=sys.stderr, flush=True)
    elif response:  # Evaluates to True for status codes < 400
        data = response.json()
        if not isinstance(data, list):
            print(f'ERROR: returned data is not a list', file=sys.stderr, flush=True)
        elif isinstance(data[0], str):
            print(f'ERROR: "{word}" NOT FOUND: did you mean any of these?\n{data[:10]}', file=sys.stderr, flush=True)
            if os.path.exists(path_not_found):
                print(f'Path exists: {path_not_found}, not overwriting.', file=sys.stderr, flush=True)
            else:
                with open(path_not_found, 'w') as f:
                    f.write(response.text)
        elif not isinstance(data[0], dict):
            print(f'ERROR: returned data[0] is not a dict', file=sys.stderr, flush=True)
        else:
            if (not 'meta' in data[0]) or (not 'src' in data[0]['meta']) or (data[0]['meta']['src'] != SRC_THESAURUS):
                print(f'WARNING: returned data is not from expected source: {SRC_THESAURUS}', file=sys.stderr, flush=True)
            if os.path.exists(path_json):
                print(f'Path exists: {path_json}, not overwriting.', file=sys.stderr, flush=True)
            else:
                with open(path_json, 'w') as f:
                    f.write(response.text)
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)


if __name__ == "__main__":
    exit('TODO! Write some unit tests for this module.')
