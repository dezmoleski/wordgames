#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Dictionary API
# https://dictionaryapi.com/
#
# Requests one word using Merriam-Webster's Collegiate® Dictionary API,
# and does some very basic sanity-checks on the response. If the response
# is JSON that parses to a Python list of dicts, then just print that out.
#
import json
import os
import requests
import sys

def read_key() -> str:
    keypath = './api-key-collegiate'
    if not os.path.isfile(keypath):
        exit(f'Key file not found: {keypath}')
    # M-W API key must be alone on first line of key file.
    with open(keypath, 'r') as file:
        key = file.readline().strip()
    return key

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit("Usage: clook <word>")

    word = sys.argv[1]
    KEY  = read_key()
    URL  = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={KEY}'
    
    print(f'Looking up: "{word}" in Merriam-Webster\'s Collegiate® Dictionary', file=sys.stderr, flush=True)
    
    response = requests.get(URL)
    if response:  # Evaluates to True for status codes < 400
        #print(f'Request succeeded with status code: {response.status_code}', file=sys.stderr, flush=True)
        data = response.json()
        if not isinstance(data, list):
            exit(f'ERROR: returned data is not a list')
        if isinstance(data[0], str):
            exit(f'ERROR: "{word}" NOT FOUND: did you mean any of these?\n{data}')
        if not isinstance(data[0], dict):
            exit(f'ERROR: returned data[0] is not a dict')
        if data[0]['meta']['src'] != "collegiate":
            exit(f'ERROR: returned data is not from expected source')
        
        print(response.text)
    else:
        print(f'Request failed with status code: {response.status_code}', file=sys.stderr, flush=True)
