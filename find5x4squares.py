#!/usr/bin/python3
# Copyright (C) 2024 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#
from wordgames import Word, WordList, AnagramsDict, LetterSetBitmask, ALPHABET_LIST
import sys
from copy import deepcopy
from glob import glob
from operator import itemgetter
from itertools import islice
import datetime
import json
import os.path

words_5l = WordList()
words_4l = WordList()

# The "partials" dicts contain WordLists indexed by the shared start
# of the words therein. For example in the partials_4l dict this
# entry appears:
# { ... "EB": [EBBS, EBON] ... }
partials_5l = dict()
partials_4l = dict()

# The two lists given are of the across & down Words & partials
# found so far. For example, if current progress towards a complete
# square looks like this:
#   R E M I T
#   A B O D E
#   B
#   I
# Then across is [REMIT, ABODE]
# and down is [RABI, EB, MO, ID, TE]
#
# The lengths of the partial down words after the zero'th must all be the same,
# and tell us the depth of the current recursion.
#
def find_squares(across: list, across_len: int, down: list, down_len: int):
   global words_5l, partials_5l
   global words_4l, partials_4l

   # The depth of the current recursion is the length of the second
   # partial down word. It's also the length of the across list.
   depth1 = len(down[1].word)
   depth2 = len(across)
   if depth1 != depth2:
      exit("Depth check one is not equal to depth check two!")
   depth = depth1

   # If depth is equal to the down_len minus one, we are on the last word.
   last_word = (depth == down_len - 1)
   
   #print(depth, across, down)
   
   # Let's try just one step, shall we?
   # Take the [depth] letter of the first down word...
   across_start = down[0].word[depth]
   
   # For each potential across word starting with across_start,
   # if there's at least one down word corresponding to each
   # down_start choosing that across word would imply, then recurse
   # (or report a found square if we've reached the down_len).
   try_acrosses = partials_5l.get(across_start)
   if try_acrosses is not None:
      for possible_next_across in try_acrosses.word_list:
         try_downs = list()
         for i in range(1,5):
            partial_next_down = down[i].word + possible_next_across.word[i]
            if last_word:
               if words_4l.contains(partial_next_down):
                  try_downs.append(Word(partial_next_down))
            else:
               if partials_4l.get(partial_next_down) is not None:
                  try_downs.append(Word(partial_next_down))
                  
         if len(try_downs) == 4:
            # Add this possible_next_across to the across list,
            # and add the next downs to the down list, to get the
            # next partial square.
            next_acrosses = across + [possible_next_across]
            next_downs = down[:1] + try_downs
            # If we just found the last across needed, we're done, just print.
            # Otherwise, recurse.
            if len(next_acrosses) == down_len:
               # We found a complete square.
               # Count up how many letters this square uses, and print that number
               # before the square word lists.
               word_strs = [w.word for w in next_acrosses]
               joined = ''.join(word_strs)
               letterset = set(joined)
               letters_list = list(letterset)
               letters_list.sort()
               print(len(letterset), ''.join(letters_list), next_acrosses, next_downs)
            else:
               find_squares(next_acrosses, across_len, next_downs, down_len)

if __name__ == "__main__":
   if len(sys.argv) != 2:
      exit("Usage: find5x4squares 5LWORD")

   # First word must be given on command line
   first_word_str = sys.argv[1]
   first_word = Word(first_word_str)
   if len(first_word) != 5:
      exit("Usage: find5x4squares 5LWORD")
      
   # Read ALL Wordle guesses file
   WORDS5L_FILE = "./wordle/ANSWERS"
   print("Reading 5-letter words file:", WORDS5L_FILE, file=sys.stderr, flush=True, end=' ')
   words_5l = WordList.from_file(WORDS5L_FILE)
   words_5l.sort()
   print("N =", len(words_5l), file=sys.stderr, flush=True)

   # Given first word must be a valid Wordle guess (5L word)
   if not words_5l.contains_word(first_word):
      exit(f"Given start word: {first_word} is not a valid 5-letter word.")
   
   # Read 4-letter wordnik words
   WORDS4L_FILE = "./WORDNIK_4L"
   print("Reading 4-letter words file:", WORDS4L_FILE, file=sys.stderr, flush=True, end=' ')
   words_4l = WordList.from_file(WORDS4L_FILE)
   words_4l.sort()
   print("N =", len(words_4l), file=sys.stderr, flush=True)

   # Build the partials dicts from 1 to the characteristic list item len-1.
   for l in range(1,5):
      for w in words_5l.word_list:
         s = w.word[0:l]
         word_list = partials_5l.get(s)
         if word_list is None:
            word_list = WordList()
            partials_5l[s] = word_list
         word_list.add_word(w)
         
   for l in range(1,4):
      for w in words_4l.word_list:
         s = w.word[0:l]
         word_list = partials_4l.get(s)
         if word_list is None:
            word_list = WordList()
            partials_4l[s] = word_list
         word_list.add_word(w)
         
   # For each 4-letter word that starts with the first letter of the given 5L word,
   # search for a 5x4 word square that can be completed. For example, given the
   # word REMIT as the first word, the first square that will be attempted begins:
   #   R E M I T
   #   A
   #   B
   #   I
   #
   # The find_squares function expects two lists of words / partial words: the
   # across words (which are always complete words) and the down words, which
   # are complete only in the first down word, and are incomplete in the second
   # through the final down word.
   #
   # The initial incomplete portion of the down words is a list of the letters
   # of the first word minus its first letter.
   down_partial_strs = list(first_word.word)[1:]
   down_partial_words = [Word(s) for s in down_partial_strs]
   for w in partials_4l[first_word.word[0]].word_list:
      find_squares([first_word], 5, [w] + down_partial_words, 4)
   
