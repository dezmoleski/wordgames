#!/usr/bin/python3
# Copyright (C) 2025 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
# Powered by Merriam-Webster's Collegiate® Dictionary API
# Powered by Merriam-Webster's Collegiate® Thesaurus API
# https://dictionaryapi.com/
#
# Follows up the cached lookups of Wordleable words in the Merriam-Webster's Collegiate®
# Dictionary with a lookup using the Merriam-Webster's Collegiate® Thesaurus API.
#
# Successful lookups are followed by a two minute sleep to keep the total lookups well
# under the noncommercial limit of 1000 requests per day.
#
# Results are written to files in pre-existing subdir ./cache-thes/
# where files are named <word>.json if the response returned what
# looks like a list of entries for the word, or <word>.not-found if
# what was returned looks like a list of strings (near-misses/matches).
#
# Some basic checks are made to avoid repeating and overwriting
# results that are already known.
#
from glob import glob
import os
import sys
import time

import mw_tools

if __name__ == "__main__":
    if len(sys.argv) != 1:
        exit("Usage: wthesfollow")

    print("Following-up found words from cache-coll/*.json with thesaurus lookups", file=sys.stderr, flush=True)
    coll_cache_dir = mw_tools.CACHE_DICT
    if os.path.isdir(coll_cache_dir):
        # Consider each .json file in the collegiate dictionary cache dir
        paths = sorted(glob(coll_cache_dir+'*.json'))
        index = 0
        for filepath in paths:
            print("-------------------------------------------------------", file=sys.stderr, flush=True)
            index += 1
            print(f'{index} of {len(paths)} - ', end='', file=sys.stderr, flush=True)
            if not os.path.isfile(filepath):
                print(f'ERROR: file is not a regular file: {filepath}', file=sys.stderr, flush=True)
            else:
                word = os.path.splitext(os.path.split(filepath)[1])[0] # yields e.g. 'treat' from path_json='./cache-coll/treat.json'
                print(word)
                result = mw_tools.thesaurus_cache(word)
                if result == mw_tools.Result.SUCCESS: # successful round-trip request, sleep longest
                    time.sleep(10)
                elif result == mw_tools.Result.NOT_FOUND: # round-trip result was a not-found, sleep a little bit
                    time.sleep(2)
                # For other results we don't need to pause at all, just carry on...
