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
import sys

import mw_tools

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit("Usage: clook <word>")

    word = sys.argv[1]
    
    print(f'Looking up: "{word}" in {mw_tools.PRODUCT_DICTIONARY}', file=sys.stderr, flush=True)

    mw_tools.dictionary_request(word)
