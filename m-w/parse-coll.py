#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Dictionary API
# https://dictionaryapi.com/
#
# This script parses entries previously requested via the API,
# and cached in files named ./cache-coll/<word>.json
# 
from glob import glob
import json
import os
import sys

def parse_word_path(word: str, path_json: str):
    """ Parse entries for a given word from given M-W lookup .json file and print what I'm interested in """
    #print(f'Parsing: "{word}" entries from file: {path_json}', file=sys.stderr, flush=True)
    try:
        entries = None
        with open(path_json, 'r') as f:
            entries = json.load(f)
        if entries is not None:
            func_list = list()
            offensive_count = 0
            for entry in entries:
                meta = entry['meta']
                if 'offensive' in meta:
                    if meta['offensive']:
                        offensive_count += 1
                    
                if 'fl' in entry:
                    functional_label = entry['fl']
                    if not functional_label in func_list:
                        func_list.append(functional_label)
            
            print(f'{word} ents={len(entries)} off={offensive_count} func=', end='')
            first=True
            for f in func_list:
                if not first:
                    print(',', end='')
                print(f.replace(' ', '-'), end='')
                if first:
                    first = False
            print('')
        
    except Exception as e:
        print(f'ERROR: Exception: {type(e)} {e}', file=sys.stderr, flush=True)
    
def parse_word(word: str):
    """ Given a word, construct path to a cached M-W lookup .json file and pass both to parse_word_path """
    path_json = f'cache-coll/{word}.json'
    if not os.path.isfile(path_json):
        print(f'ERROR: File not found: {path_json}', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    parse_word_path(word, path_json)
    
def parse_path(path_json: str):
    """ Given a path to a cached M-W lookup .json file, parse out the word and pass both to parse_word_path """
    if not os.path.isfile(path_json):
        print(f'ERROR: File not found: {path_json}', file=sys.stderr, flush=True)
        return # PUNCH-OUT
    word = os.path.splitext(os.path.split(path_json)[1])[0] # yields e.g. 'treat' from path_json='./cache-coll/treat.json'
    parse_word_path(word, path_json)
    
    
if __name__ == "__main__":
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help")):
        exit("Usage: parse-coll [<word>]")

    if len(sys.argv) == 2:
        parse_word(sys.argv[1])
    else:
        print("Parsing all words from cache-coll/*.json", file=sys.stderr, flush=True)
        cache_dir = "./cache-coll/"
        if os.path.isdir(cache_dir):
            # Parse each .json file in the cache dir
            paths = sorted(glob(cache_dir+'*.json'))
            for filepath in paths:
                parse_path(filepath)
