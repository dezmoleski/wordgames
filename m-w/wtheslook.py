#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Thesaurus API
# https://dictionaryapi.com/
#
# Requests a random sample of given size (N) out of all Wordleable words
# from the Merriam-Webster's Collegiate® Thesaurus. API requests are
# made one every two minutes to keep well under the noncommercial limit
# of 1000 requests per day (1 per two minutes is 720 per day).
#
# Results are written to files in pre-existing subdir ./cache-thes/
# where files are named <word>.json if the response returned what
# looks like a list of entries for the word, or <word>.not-found if
# what was returned looks like a list of strings (near-misses/matches).
#
# Some basic checks are made to avoid repeating and overwriting
# results that are already known. (TODO: add a "force" option)
# These checks allow multiple instances of this script to be run
# in parallel as a super easy way to test, and/or to speed up the eventual
# collection of all the thesaurus entries for Wordleable words ;-)
#
import json
import os
import random
import requests
import sys
import time
from wordgames import Word, WordList

import keys

def lookup(word: str):
    path_not_found = f'cache-thes/{word}.not-found'
    path_json = f'cache-thes/{word}.json'
    
    if os.path.exists(path_not_found):
        print(f'Path exists: {path_not_found}, not requesting.', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    
    if os.path.exists(path_json):
        print(f'Path exists: {path_json}, not requesting.', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    
    print(f'Requesting thesaurus listing for: "{word}"', file=sys.stderr, flush=True)

    URL=f'https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={keys.MW_THESAURUS}'
    #print(URL, file=sys.stderr, flush=True)
    
    response = requests.get(URL)
    #exit(f'DEZ! {response}\nHEADERS:{response.headers}\nTEXT:{response.text}')
    
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={keys.MW_THESAURUS} is correct for API https://dictionaryapi.com/api/v3/references/thesaurus/json/',
              file=sys.stderr, flush=True)
    elif response:  # Evaluates to True for status codes < 400
        #print(f'Request succeeded with status code: {response.status_code}', file=sys.stderr, flush=True)
        data = response.json()
        if not isinstance(data, list):
            print(f'ERROR: returned data is not a list', file=sys.stderr, flush=True)
        elif isinstance(data[0], str):
            print(f'ERROR: "{word}" NOT FOUND: did you mean any of these?\n{data[:5]}', file=sys.stderr, flush=True)
            if os.path.exists(path_not_found):
                print(f'Path exists: {path_not_found}, not overwriting.', file=sys.stderr, flush=True)
            else:
                with open(path_not_found, 'w') as f:
                    f.write(response.text)
        elif not isinstance(data[0], dict):
            print(f'ERROR: returned data[0] is not a dict', file=sys.stderr, flush=True)
        elif data[0]['meta']['src'] != "coll_thes":
            print(f'ERROR: returned data is not from expected source', file=sys.stderr, flush=True)
        else:
            if os.path.exists(path_json):
                print(f'Path exists: {path_json}, not overwriting.', file=sys.stderr, flush=True)
            else:
                with open(path_json, 'w') as f:
                    f.write(response.text)
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit("Usage: wtheslook <N>")

    N = 0
    try:
        N = int(sys.argv[1])
    except ValueError:
        exit(f'ERROR: {sys.argv[1]} must be an integer.')
    if N < 1 or N > 14855:
        exit(f'ERROR: {N} must be an integer between 1 and 14855.')

    # Read ALL GUESSES file
    ALL_FILE = "./ALL"
    print(f'Powered by Merriam-Webster\'s Collegiate® Thesaurus API', file=sys.stderr, flush=True)
    print("Reading all valid guesses file:", ALL_FILE, "...", end=' ', file=sys.stderr, flush=True)
    valid_guesses = WordList.from_file(ALL_FILE)
    valid_guesses.sort()
    sample = random.sample(valid_guesses.word_list, N)
    print(f'Random sample of {N}:', file=sys.stderr, flush=True)

    index = 0
    for w in sample:
        print("-------------------------------------------------------", file=sys.stderr, flush=True)
        index += 1
        print(f'{index} of {N} - ', end='', file=sys.stderr, flush=True)
        lookup(w.word.lower())
        time.sleep(120)
