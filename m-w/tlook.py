#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Thesaurus API
# https://dictionaryapi.com/
#
# Requests one word using Merriam-Webster's Collegiate® Thesaurus API,
# and does some very basic sanity-checks on the response. If the response
# is JSON that parses to a Python list of dicts, then just print that out.
#
import json
import os
import requests
import sys

import keys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit("Usage: tlook <word>")

    word = sys.argv[1]
    API  = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/'
    KEY  = keys.MW_THESAURUS
    URL  = f'{API}{word}?key={KEY}'
    
    print(f'Looking up: "{word}" in Merriam-Webster\'s Collegiate® Thesaurus', file=sys.stderr, flush=True)
    
    response = requests.get(URL)
    if "Invalid API key" in response.text:
        print(f'ERROR: Invalid key. Check key={KEY} is correct for API {API}',
              file=sys.stderr, flush=True)
    elif response:  # Evaluates to True for status codes < 400
        #print(f'Request succeeded with status code: {response.status_code}', file=sys.stderr, flush=True)
        data = response.json()
        if not isinstance(data, list):
            exit(f'ERROR: returned data is not a list')
        if isinstance(data[0], str):
            exit(f'ERROR: "{word}" NOT FOUND: did you mean any of these?\n{data}')
        if not isinstance(data[0], dict):
            exit(f'ERROR: returned data[0] is not a dict')
        if data[0]['meta']['src'] != "coll_thes":
            exit(f'ERROR: returned data is not from expected source')
        
        print(response.text)
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)
