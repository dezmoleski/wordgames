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
import random
import sys
import time

from wordgames import Word, WordList

import mw_tools

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

    print(f'Powered by {mw_tools.PRODUCT_THESAURUS} API', file=sys.stderr, flush=True)
    
    # Read ALL GUESSES file
    ALL_FILE = "./ALL"
    print("Reading all valid guesses file:", ALL_FILE, "...", end=' ', file=sys.stderr, flush=True)
    valid_guesses = WordList.from_file(ALL_FILE)
    sample = random.sample(valid_guesses.word_list, N)
    print(f'Random sample of {N}:', file=sys.stderr, flush=True)

    index = 0
    for w in sample:
        print("-------------------------------------------------------", file=sys.stderr, flush=True)
        index += 1
        print(f'{index} of {N} - ', end='', file=sys.stderr, flush=True)
        mw_tools.thesaurus_cache(w.word.lower())
        time.sleep(120)
