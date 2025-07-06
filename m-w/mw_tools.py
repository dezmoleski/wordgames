#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Dictionary API
# Powered by Merriam-Webster's Collegiate® Thesaurus API
# https://dictionaryapi.com/
#
from enum import Enum, auto
import os
import requests
import sys

import keys # Local keys file


PRODUCT_DICTIONARY = 'Merriam-Webster\'s Collegiate® Dictionary'
API_DICTIONARY = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'
KEY_DICTIONARY = keys.MW_COLLEGIATE
SRC_DICTIONARY = 'collegiate'
CACHE_DICT = 'cache-coll/'

def url_dictionary(word: str) -> str:
    return f'{API_DICTIONARY}{word}?key={KEY_DICTIONARY}'


PRODUCT_THESAURUS = 'Merriam-Webster\'s Collegiate® Thesaurus'
API_THESAURUS = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/'
KEY_THESAURUS = keys.MW_THESAURUS
SRC_THESAURUS = 'coll_thes'
CACHE_THES = 'cache-thes/'

def url_thesaurus(word: str) -> str:
    return f'{API_THESAURUS}{word}?key={KEY_THESAURUS}'

class Result(Enum):
    SUCCESS = auto()
    NOT_FOUND = auto()
    ERROR = auto()
    CACHE_RESULT_FOUND = auto()
    
def api_request(word: str, url: str, key: str, api: str, src: str) -> Result:
    response = requests.get(url)
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={key} is correct for API {api}', file=sys.stderr, flush=True)
        return Result.ERROR
    
    if response:  # Evaluates to True for status codes < 400
        data = response.json()
        if not isinstance(data, list):
            print(f'ERROR: returned data is not a list', file=sys.stderr, flush=True)
            return Result.ERROR
        
        if len(data) == 0 or isinstance(data[0], str):
            print(f'ERROR: "{word}" NOT FOUND', end='', file=sys.stderr, flush=True)
            if len(data) > 0:
                print(f': did you mean any of these?\n{data[:10]}', file=sys.stderr, flush=True)
            else:
                print()
            return Result.NOT_FOUND
        
        if not isinstance(data[0], dict):
            print(f'ERROR: returned data[0] is not a dict', file=sys.stderr, flush=True)
            return Result.ERROR
        
        if (not 'meta' in data[0]) or (not 'src' in data[0]['meta']) or (data[0]['meta']['src'] != src):
            print(f'WARNING: returned data is not from expected source: {src}', file=sys.stderr, flush=True)
        
        print(response.text)
        return Result.SUCCESS
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)
        return Result.ERROR

def dictionary_request(word: str) -> Result:
    return api_request(word, url_dictionary(word), KEY_DICTIONARY, API_DICTIONARY, SRC_DICTIONARY)


def thesaurus_request(word: str) -> Result:
    return api_request(word, url_thesaurus(word), KEY_THESAURUS, API_THESAURUS, SRC_THESAURUS)


def thesaurus_cache(word: str) -> Result:
    path_not_found = f'{CACHE_THES}{word}.not-found'
    path_json = f'{CACHE_THES}{word}.json'
    
    if os.path.exists(path_not_found):
        print(f'Path exists: {path_not_found}, not requesting.', file=sys.stderr, flush=True)
        return Result.CACHE_RESULT_FOUND
    
    if os.path.exists(path_json):
        print(f'Path exists: {path_json}, not requesting.', file=sys.stderr, flush=True)
        return Result.CACHE_RESULT_FOUND
    
    print(f'Requesting thesaurus listing for: "{word}"', file=sys.stderr, flush=True)

    response = requests.get(url_thesaurus(word))
    #exit(f'DEZ! {response}\nHEADERS:{response.headers}\nTEXT:{response.text}')
    
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={KEY_THESAURUS} is correct for API {API_THESAURUS}', file=sys.stderr, flush=True)
        return Result.ERROR
    
    if response:  # Evaluates to True for status codes < 400
        data = response.json()
        if not isinstance(data, list):
            print(f'ERROR: returned data is not a list', file=sys.stderr, flush=True)
            return Result.ERROR
            
        if len(data) == 0 or isinstance(data[0], str):
            print(f'ERROR: "{word}" NOT FOUND', end='', file=sys.stderr, flush=True)
            if len(data) > 0:
                print(f': did you mean any of these?\n{data[:10]}', file=sys.stderr, flush=True)
            else:
                print()
            if os.path.exists(path_not_found):
                print(f'Path exists: {path_not_found}, not overwriting.', file=sys.stderr, flush=True)
            else:
                with open(path_not_found, 'w') as f:
                    f.write(response.text)
            return Result.NOT_FOUND
        
        if not isinstance(data[0], dict):
            print(f'ERROR: returned data[0] is not a dict', file=sys.stderr, flush=True)
            return Result.ERROR

        if (not 'meta' in data[0]) or (not 'src' in data[0]['meta']) or (data[0]['meta']['src'] != SRC_THESAURUS):
            print(f'WARNING: returned data is not from expected source: {SRC_THESAURUS}', file=sys.stderr, flush=True)
            
        if os.path.exists(path_json):
            print(f'Path exists: {path_json}, not overwriting.', file=sys.stderr, flush=True)
            return Result.CACHE_RESULT_FOUND
        
        with open(path_json, 'w') as f:
            f.write(response.text)
        return Result.SUCCESS
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)
        return Result.ERROR


if __name__ == "__main__":
    exit('TODO! Write some unit tests for this module.')
