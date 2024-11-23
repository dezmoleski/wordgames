# Copyright (C) 2024 Dez Moleski dez@moleski.com
# MIT License: All uses allowed with attribution.
#

"""Elements for making word game generators and solvers.
"""
import random
import sys
from dataclasses import dataclass
from dataclasses import field

A = 'A'
B = 'B'
C = 'C'
D = 'D'
E = 'E'
F = 'F'
G = 'G'
H = 'H'
I = 'I'
J = 'J'
K = 'K'
L = 'L'
M = 'M'
N = 'N'
O = 'O'
P = 'P'
Q = 'Q'
R = 'R'
S = 'S'
T = 'T'
U = 'U'
V = 'V'
W = 'W'
X = 'X'
Y = 'Y'
Z = 'Z'
    
ALPHABET_LIST = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z]

VOWELS_STR = 'AEIOUY'
VOWELS_SET = set(VOWELS_STR)

CHAR_BITMASK = {
    A: 0b000000000000000000000000001,
    B: 0b000000000000000000000000010,
    C: 0b000000000000000000000000100,
    D: 0b000000000000000000000001000,
    E: 0b000000000000000000000010000,
    F: 0b000000000000000000000100000,
    G: 0b000000000000000000001000000,
    H: 0b000000000000000000010000000,
    I: 0b000000000000000000100000000,
    J: 0b000000000000000001000000000,
    K: 0b000000000000000010000000000,
    L: 0b000000000000000100000000000,
    M: 0b000000000000001000000000000,
    N: 0b000000000000010000000000000,
    O: 0b000000000000100000000000000,
    P: 0b000000000001000000000000000,
    Q: 0b000000000010000000000000000,
    R: 0b000000000100000000000000000,
    S: 0b000000001000000000000000000,
    T: 0b000000010000000000000000000,
    U: 0b000000100000000000000000000,
    V: 0b000001000000000000000000000,
    W: 0b000010000000000000000000000,
    X: 0b000100000000000000000000000,
    Y: 0b001000000000000000000000000,
    Z: 0b010000000000000000000000000
}


@dataclass()
class LetterSetBitmask:
    bitmask: int = 0
    
    def __repr__(self) -> str:
        return bin(self.bitmask)
    
    def __len__(self) -> int:
        return self.bitmask.bit_count()
    
    def add(self, c: str):
        bit = CHAR_BITMASK.get(c[0].upper(), 0)
        self.bitmask |= bit
    
    def add_set(self, s: set):
        for c in s:
            self.add(c)
    
    def copy(self) -> object:
        return LetterSetBitmask(self.bitmask)
    
    def is_subset(self, other: object) -> bool:
        return (self.bitmask & other.bitmask) == self.bitmask
    
    def subtract(self, other: object):
        self.bitmask &= ~(other.bitmask)
    

@dataclass(order=True, frozen=True)
class Word:
    word: str
    letter_set: set = field(default_factory=set, init=False, repr=False, compare=False)
    letter_set_bits: LetterSetBitmask = field(default_factory=LetterSetBitmask, init=False, repr=False, compare=False)
    letter_set_mask: int = field(init=False, repr=False, compare=False)

    def __repr__(self) -> str:
        return self.word

    def __len__(self) -> int:
        return len(self.word)

    def __post_init__(self):
        object.__setattr__(self, 'word', self.word.upper())
        object.__setattr__(self, 'letter_set', set(self.word))
        self.init_bitmask()
        object.__setattr__(self, 'letter_set_mask', self.letter_set_bits.bitmask)
        
    def init_bitmask(self):
        for c in self.letter_set:
            self.letter_set_bits.add(c)
        
    def count_vowels(self) -> float:
        '''Returns the count of unique vowels (not counting repeats) used in the word.
           Y counts as 0.5 of a vowel.
        '''
        v: float = len(self.letter_set & VOWELS_SET)
        if 'Y' in self.letter_set:
            v -= 0.5
        return v
    
    def count_vowels_strict(self) -> float:
        '''Returns the count of vowels (including repeats) used in the word.
           Y counts as 0.5 of a vowel.
        '''
        v = 0
        for l in self.word:
            if l == 'Y':
                v += 0.5
            elif l in VOWELS_SET:
                v += 1
        return v
    
    def is_anagram_of_word(self, word: object) -> bool:
        '''A word is NOT an anagram of itself.'''
        return self.letter_set == word.letter_set and self.word != word.word

    def is_anagram_of_str(self, s: str) -> bool:
        return self.is_anagram_of_word(Word(s))

    def is_heterogram(self) -> bool:
        '''Heterograms by definition contain no repeated letters.'''
        return len(self.word) == len(self.letter_set)

    def is_palindrome(self) -> bool:
        halflen: int = len(self.word) // 2 # use floor division operator //
        front_half = self.word[0:halflen]
        rev_back_half = self.word[:-(halflen+1):-1]
        return front_half == rev_back_half

    def reversed(self) -> object:
        return Word(self.word[::-1])
        
    def sorted_letters(self) -> str:
        '''Returns the letter set as a string of letters in alphabetic order.'''
        letters = list(self.letter_set)
        letters.sort()
        return ''.join(letters)

@dataclass
class WordList:
    word_set: set = field(default_factory=set)
    word_list: list = field(default_factory=list)
    list_is_sorted: bool = False
    
    def __repr__(self) -> str:
        return ' '.join(map(lambda w: str(w), self.word_list))
    
    def __len__(self) -> int:
        return len(self.word_set)
    
    def add_word(self, word: Word):
        if not word in self.word_set:
            self.word_set.add(word)
            self.word_list.append(word)
            self.list_is_sorted = False
    
    def add_str(self, s: str):
        self.add_word(Word(s))
    
    def add_str_list(self, l: list[str]):
        for s in l:
            self.add_word(Word(s))
    
    def add_wordlist(self, wl: object):
        for word in wl.word_set:
            self.add_word(word)
    
    def contains(self, s: str) -> bool:
        return (Word(s) in self.word_set)
    
    def contains_word(self, word: Word) -> bool:
        return (word in self.word_set)
    
    def remove_word(self, word: Word):
        self.word_set.remove(word)
        self.word_list.remove(word)
        
    def remove_str(self, s: str):
        self.remove_word(Word(s))

    def digraphs_by_occurrence(self) -> dict:
        """ Returns a dictionary with the digraph as key and 
            the count of occurrences of that digraph as value.
            E.g. in KUKUS the count of 'KU' is incremented twice.
        """
        dicount = dict()
        for w in self.word_list:
            prev_letter = ''
            for letter in w.word:
                if prev_letter != '':
                    digraph = prev_letter + letter
                    count = dicount.get(digraph, 0)
                    dicount[digraph] = count + 1
                prev_letter = letter
        return dicount
        
    def digraphs_by_word(self) -> dict:
        """ Returns a dictionary with the digraph as key and 
            the count of words containing that digraph as value.
            E.g. in KUKUS the count of 'KU' is incremented only once.
        """
        dicount = dict()
        for w in self.word_list:
            prev_letter = ''
            digraphs = set()
            for letter in w.word:
                if prev_letter != '':
                    digraph = prev_letter + letter
                    digraphs.add(digraph)
                prev_letter = letter
            for digraph in digraphs:
                count = dicount.get(digraph, 0)
                dicount[digraph] = count + 1
        return dicount
        
    def heterograms(self) -> set:
        h = set()
        for word in self.word_set:
            if word.is_heterogram():
                h.add(word)
        return h
    
    def sort(self) -> None:
        if not self.list_is_sorted:
            self.word_list.sort()
            self.list_is_sorted = True

    @classmethod
    def from_strings(cls, *strs: str) -> object:
        wl = cls()
        for s in strs:
            wl.add_str(s)
        return wl

    @classmethod
    def from_file(cls, path: str) -> object:
        wl = cls()
        with open(path, 'r') as f:
            for line in f:
                wl.add_str_list(line.split())
        return wl

    @classmethod
    def random_from_wordlist(cls, wl: object, N: int) -> object:
        """ N is the desired number of words to retain out of
            the given WordList wl.
            If N > len(words) then the given WordList is returned,
            otherwise a new WordList is returned of size N.
        """
        if N > len(wl):
            return wl # PUNCH-OUT
        # Don't try to be tricky, just pick a random word
        # from the file list and add it to the random list
        # until the size of the random list meets the target N.
        rl = cls()
        while len(rl) < N:
            r = random.randrange(0, len(wl))
            rl.add_word(wl.word_list[r])
        return rl
    
    @classmethod
    def random_from_file(cls, path: str, N: int) -> object:
        """ N is the desired number of words to retain out of
            whatever is loaded from the given path.
            If N > len(words) then all the words are kept.
        """
        wl = cls.from_file(path)
        return cls.random_from_wordlist(wl, N)

    @classmethod
    def from_sub_alphabet_hgrams(cls, words: list, alphabet: set) -> object:
        sub_wl = cls()
        for w in words:
            if w.is_heterogram() and w.letter_set.issubset(alphabet):
                sub_wl.add_word(w)
        return sub_wl
    
@dataclass
class AnagramsDict:
    """ A dictionary of lists of anagrams.
        The key to each list is the sorted letter set for the anagrams.
    """
    anagrams: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.anagrams)

    def word_key(self, w: Word) -> str:
        return w.sorted_letters()
    
    def add_wordlist(self, wl: WordList):
        for word in wl.word_set:
            key = self.word_key(word)
            if not key in self.anagrams:
                self.anagrams[key] = list()
            self.anagrams[key].append(word.word)

    def anagrams_of_word(self, w: Word) -> list:
        ''' Returns None if there are no anagrams of w in the dict.
            Returns a list (not containing w) of anagram strings if w is found.
        '''
        key = self.word_key(w)
        agram_list = self.anagrams.get(key)
        agrams = None
        if not agram_list is None:
            agrams = agram_list.copy()
            agrams.remove(w.word)
        return agrams
    
    def anagrams_of_str(self, s: str) -> list:
        return self.anagrams_of_word(Word(s))
    
    def prune_keys(self, delkeys: list[str]):
        for k in delkeys:
            del self.anagrams[k]

    def prune(self):
        '''Delete keys with fewer than two anagrams - these are often uninteresting.'''
        self.prune_keys([k for k in self.anagrams if len(self.anagrams[k]) < 2])

    def sort(self):
        '''Sort each list of anagrams.'''
        for v in self.anagrams.values():
            v.sort()
            
    def total_words(self) -> int:
        '''Returns sum of length of all anagrams lists in the dictionary.'''
        total = 0
        for k,v in self.anagrams.items():
            total += len(v)
        return total

@dataclass
class PerfectAnagramsDict(AnagramsDict):
    """ A dictionary of lists of anagrams.
        The key to each list is the sorted letter LIST, joined back into a string, for the anagrams.
        This yields what are called "perfect" anagrams, ie formed from exactly the same letters
        respecting repeats, vs regular anagrams, formed from the same SET of letters without
        regard to repeated letters.
    """
    def word_key(self, w: Word) -> str:
        letters = sorted(list(w.word))
        return ''.join(letters)
    
WORDNIK_WORDLIST_PATH = './wordnik-wordlist'
WORDNIK_ADDITIONS_PATH = './wordnik-additions'

WORDLE_ANSWERS_PATH = 'wordle/ANSWERS'
WORDLE_GUESSES_PATH = 'wordle/NON-ANSWERS'
WORDLE_PU_PATH = 'wordle/PU'

WORDLE_UNSCORED = ''
WORDLE_BLACK = '-'
WORDLE_YELLOW = 'y'
WORDLE_GREEN = 'G'

@dataclass
class Wordle:
    word_str: str = ''
    word: Word = field(init=False)
    word_letters: list = field(default_factory=list)

    def set_word(self, word_str: str):
        self.word = Word(word_str)
        self.word_str = str(self.word)
        self.word_letters = list(self.word_str)

    def guess(self, guess_str: str) -> list[str]:
        '''Score a guess against this word, returns a list of "-", "y", "G"
           where:
             "-" = WORDLE_BLACK, letter is not in the word
             "y" = WORDLE_YELLOW, letter is in the word but in a different position
             "G" = WORDLE_GREEN, letter is in the correct position
           Returns None if the length of the guess is different from this word's length.
        '''
        result = None
        if len(guess_str) == len(self.word_str):
            result = [WORDLE_UNSCORED] * len(guess_str)
            guess = guess_str.upper()

            # It's easy to score all the GREEN and *some* of the BLACK results on a single pass.
            for i in range(len(guess)):
                guess_char = guess[i]
                if not guess_char in self.word_str:
                    # BLACK
                    result[i] = WORDLE_BLACK
                elif guess_char == self.word_str[i]:
                    # GREEN
                    result[i] = WORDLE_GREEN
            # Yellows are harder because of the need to deal with repeated letters.
            n_unscored = result.count(WORDLE_UNSCORED)
            while n_unscored > 0:
                # The unscored guess chars that remain can end up YELLOW or BLACK.
                # Find the index of the first unscored guess letter.
                i = result.index(WORDLE_UNSCORED)
                guess_char = guess[i]
                # Note the invariant expected here is:
                #   n_in_wordle > 0 and n_in_guess > 0
                # because:
                #   - if the guess char appeared zero times in the wordle, we'd have already scored it BLACK above.
                #   - we just pulled the guess_char out of the guess, so it must be there, it's a tautology!
                n_in_wordle = self.word_str.count(guess_char)
                n_in_guess = guess.count(guess_char)
                assert(n_in_wordle > 0 and n_in_guess > 0)

                if n_in_wordle == 1 and n_in_guess == 1:
                    # This is the easy case, it's YELLOW (since if this one occurrence was in
                    # the right place it would already have been scored GREEN).
                    result[i] = WORDLE_YELLOW
                else:
                    # Trickier... we are dealing with repeated characters in the guess, or in
                    # the wordle, or in BOTH!
                    # For now I'm just going to brute force it and think about trying to
                    # find an elegant way to score wordle guesses another time (TODO!).
                    
                    if n_in_guess == 1:
                        # Easiest of these cases: it must be YELLOW
                        #   - we know n in wordle must be > 1
                        #   - we know this guess position doesn't match, or it'd already be a GREEN
                        assert(n_in_wordle > 1)
                        result[i] = WORDLE_YELLOW
                    elif n_in_wordle == 1 and n_in_guess > 1:
                        # At most 1 of the occurrences of guess_char in the guess can be non-BLACK.
                        # If one of the occurrences of guess_char is already GREEN, then the
                        # rest are black.
                        any_are_green = False
                        for r in range(len(result)):
                            if guess_char == guess[r] and result[r] == WORDLE_GREEN:
                                any_are_green = True
                                break # we can end this loop now, we know
                        if any_are_green:
                            for r in range(len(result)):
                                if guess_char == guess[r] and result[r] == WORDLE_UNSCORED:
                                    result[r] = WORDLE_BLACK
                        else:
                            # SUSPECT CODE! TODO!!! But we DO know the following at this point:
                            #   - the guess_char appears only once in the wordle
                            #   - the guess_char appears more than once in the guess
                            #   - NONE of the occurrences of the guess char are in the right position.
                            # So maybe this original stab at it is correct, now that we know more?
                            #
                            # If this is the first instance of this char in the guess, it's
                            # a YELLOW, otherwise it's a BLACK.
                            gi = guess.index(guess_char) # remember this is the FIRST index.
                            if i == gi:
                                result[i] = WORDLE_YELLOW
                            else:
                                # We must be "further down" in the guess/result than the first one.
                                assert(gi < i)
                                result[i] = WORDLE_BLACK
                    else:
                        # Final case, trickiest of all. We know:
                        #   - this guess char appears more than once in the wordle, AND
                        #   - this guess char appears more than once in the guess, AND
                        #   - this position of the guess char is currently unscored.
                        # Note that this pos might NOT be the first instance of the guess char,
                        # since there might have been an earlier one already scored GREEN.
                        assert(n_in_wordle > 1 and n_in_guess > 1 and result[i] == WORDLE_UNSCORED)
                        #TODO: but what now?
                        # I think what we do is score all the instances of this guess char now.
                        #
                        # Iterate from pos zero until we have visited n_in_guess instances of this
                        # this guess char (n_in_guess is how many need to be scored in the result).
                        # Once a number of guess chars equal to the number in the answer have been
                        # given either a GREEN or YELLOW result, the rest are BLACK.
                        # (this does seem finally as if this loop might generalize to score the other YELLOW/BLACK cases, too)
                        # Remember that GREENs are already all scored - so we must count all those up in advance.
                        n_to_visit = n_in_guess
                        n_green = 0 # TODO: there's probably a nice one-liner count with a lambda predicate to collapse these 4 lines
                        for r in range(len(result)):
                            if guess_char == guess[r] and result[r] == WORDLE_GREEN:
                                n_green += 1                 
                        n_yellow_to_give = n_in_wordle - n_green # this is the MOST yellows to give, not necessarily how many yellows there may be
                        assert(n_yellow_to_give >= 0) # we might even know it's strictly > 0 but it surely better not be negative!
                        for r in range(len(result)):
                            if guess_char == guess[r]:
                                if result[r] == WORDLE_UNSCORED:
                                    if n_yellow_to_give > 0:
                                        result[r] = WORDLE_YELLOW
                                        n_yellow_to_give -= 1
                                    else:
                                        result[r] = WORDLE_BLACK
                                n_to_visit -= 1
                                if n_to_visit == 0:
                                    break # we can stop this loop, we've visited all instances of this guess_char

                # No matter what, we must reduce n_unscored each time around this loop!
                new_n_unscored = result.count(WORDLE_UNSCORED)
                # TODO: leave this here once I think I'm done:
                #assert(new_n_unscored < n_unscored)
                if new_n_unscored >= n_unscored: # oops!
                    print("PUNCH OUT!")
                    return result # just PUNCH OUT for now (but TODO: this should go away)
                n_unscored = new_n_unscored

        return ''.join(result), guess, self.word_str, result

    @classmethod
    def from_str(cls, word: str) -> object:
        wordle = Wordle()
        wordle.set_word(word)
        return wordle

@dataclass
class ExclusiveLetterSets:
    """ This is a set of sets (kept as a list of sets) of letters,
        where no letter appears in more than one of the subsets.
        In other words the subsets are all mutually disjoint.
    """
    letter_sets: list = field(default_factory=list)
    letter_groups: list = field(default_factory=list)
    all_letters: set = field(default_factory=set)

    def __repr__(self) -> str:
        return str(self.letter_sets)

    def add_letter_group(self, new_group: str):
        """ Ensure the exclusivity / mutual disjoint aspect by only
            adding the difference of the new letters from the current
            combined set of all the previously-added subsets.
        """
        new_set = set(new_group)
        if len(new_set) != len(new_group):
            # There are repeated letters in the group.
            # TODO: adjust the group to remove repeats but keep the given sequence otherwise.
            print("ERROR: repeated letters in group:", new_group)
        letter_set = new_set.difference(self.all_letters)
        if len(letter_set) != len(new_set):
            # The new_group contained letters that were already in previous sets.
            # TODO: adjust the group to remove letters that were previously added.
            print("ERROR: group contains previously-added letters:", new_group)
        self.letter_sets.append(letter_set)
        self.letter_groups.append(new_group)
        self.all_letters.update(letter_set)
        
    def set_letter_sets(self, sets_str: str):
        for w in sets_str.split():
            self.add_letter_group(w.upper())

    def allow_letter(self, letter: str) -> bool:
        """ A letter is allowed if its uppercase self is in the all_letters set.
        """
        if len(letter) == 1:
            return letter.upper() in self.all_letters
        return False

    def set_containing(self, l: str):
        for s in self.letter_sets:
            if l in s:
                return s
        return None
    
    def allow_adjacency(self, letter_one: str, letter_two: str) -> bool:
        """ Letter 1 and Letter 2 are allowed to be adjacent if they
            appear in different subsets of the exclusive letter sets.
        """
        if self.allow_letter(letter_one) and self.allow_letter(letter_two):
            s1 = self.set_containing(letter_one.upper())
            s2 = self.set_containing(letter_two.upper())
            if (s1 is not None) and (s2 is not None):
                return (s1 is not s2)
        return False
    
@dataclass
class WordTrains:
    letters: str = ''
    bonus_solution: str = ''
    letter_sets: ExclusiveLetterSets = field(init=False, repr=False)
    completed_bonus_words: set = field(default_factory=set, init=False, repr=False)
    completed_trains: set = field(default_factory=set, init=False, repr=False)
    in_progress_train: list = field(default_factory=list, init=False)
    in_progress_word: str = ''
    in_progress_remains: set = field(default_factory=set, init=False, repr=False)
    total_score: int = 0
    word_list: WordList = field(default_factory=WordList, init=False, repr=False)
    
    def set_letter_sets(self, sets_str: str):
        self.letter_sets = ExclusiveLetterSets()
        self.letter_sets.set_letter_sets(sets_str)
        self.letters = sets_str.upper()
        self.reset_trains()

    def reset_trains(self):
        # TODO: there will be more initializing to do here!
        self.completed_bonus_words = set()
        self.completed_trains = set()
        self.new_train(False)

    def new_train(self, TODO_print_sep: bool = True):
        """ Intended to be bound to the ESC key to abandon the
            current in-progress train, or to happen automatically
            upon entering a word that completes the train (i.e.
            uses every letter in the set in that train).
            Updates the game score as a side effect, since this
            is always required immediately after this operation.
        """
        self.in_progress_word = ''
        self.in_progress_train = list()
        self.in_progress_remains = self.letter_sets.all_letters.copy()
        self.update_score()
        if TODO_print_sep and self.total_score > 0:
            print("-----")
            
    def update_score(self):
        score: int = 0
        # 5 points for each completed train of length > 3 words.
        # 10 points for a train of length 3.
        # 20 points for a train of length 2.
        # 500 points for a train of length 1.
        for train in self.completed_trains:
            # Train length is number of colons in the train string plus one.
            train_len = train.count(':') + 1
            if train_len > 3:
                score += 5
            elif train_len == 3:
                score += 10
            elif train_len == 2:
                score += 20
            elif train_len == 1:
                score += 500
            else:
                # Huh?
                print("ERROR: zero-length train!")
            # Bonus: 30 points for finding the bonus solution
            if train == self.bonus_solution:
                score += 30
                
        # For words that consume six or more characters (bonus words), their
        # score is just the word length minus five, so at least one point each.
        for word in self.completed_bonus_words:
            score += len(word) - 5
        self.total_score = score
    
    def add_letter(self, letter: str) -> bool:
        """ Append the letter (if allowed) to the in-progress word.
        """
        # If this is the first letter of the in-progress word, then we just
        # need to know if it's a member of the exclusive letter sets.
        if len(self.in_progress_word) == 0:
            if self.letter_sets.allow_letter(letter):
                self.in_progress_word = letter.upper()
                return True
        else:
            last_letter = self.in_progress_word[-1]
            if self.letter_sets.allow_adjacency(last_letter, letter):
                self.in_progress_word += letter.upper()
                return True
        return False

    def enter_word(self):
        """ Test the accumulated letters of the in-progress word to see if
            it can be added to the in-progress train.
            Intended to be bound to the ENTER key.
        """
        if len(self.in_progress_word) > 2:
            if self.word_list.contains(self.in_progress_word):
                # Append the word to the train and set the last letter
                # of the word to be the first letter of the next word.
                # Remove the word's letters from the remainder set.
                accepted_word = self.in_progress_word
                accepted_word_letters = set(accepted_word)
                self.in_progress_train.append(accepted_word)
                self.in_progress_word = accepted_word[-1]
                self.in_progress_remains.difference_update(accepted_word_letters)
                # If the word uses six or more unique letters it's a bonus word.
                # TODO: this little section is awkward but will clean up when
                #       we get rid of the "print mode" UI
                if len(accepted_word_letters) > 5:
                    if not accepted_word in self.completed_bonus_words:
                        print(accepted_word, "! Bonus =", len(accepted_word) - 5, "!")
                        self.completed_bonus_words.add(accepted_word)
                        self.update_score()
                    else:
                        print(accepted_word)
                else:
                    print(accepted_word)
                    
                # If the remainder set is empty, this train is complete!
                # Woot woot! Put it on the completed trains list and
                # start a new train (which updates the score, too).
                if len(self.in_progress_remains) == 0:
                    train_str = ':'.join(self.in_progress_train)
                    self.completed_trains.add(train_str)
                    self.new_train(False)
                    bonus_msg = ''
                    if train_str == self.bonus_solution:
                        bonus_msg = "! Bonus = 30 !"
                    print("=== score:", self.total_score, "===", train_str, bonus_msg)
            else:
                print("ERROR: word rejected, not found:", self.in_progress_word)
        else:
            print("ERROR: word rejected, too short:", self.in_progress_word)
        
    def test_play_letters(self, letters: str):
        """ This is really meant to be just a testing function. In the
            actual intended implementations, typed / clicked letters are
            accumulated one-by-one by calling add_letter.
        """
        for letter in letters:
            if not self.add_letter(letter):
                print("ERROR: letter rejected:", letter)
        self.enter_word()

    def letters_are_playable(self, letters: str) -> bool:
        """ Returns true if the given letters are playable in the current game.
            Resets the in-progress items before & after testing the sequence.
        """
        playable: bool = True
        self.new_train(False)
        for letter in letters:
            if not self.add_letter(letter):
                playable = False
        self.new_train(False)
        return playable
    
    def read_word_list(self, path: str):
        new_word_list = WordList.from_file(path)
        self.word_list.add_wordlist(new_word_list)
        self.word_list.sort() # not really necessary but I like to keep it sorted...

    def set_bonus_solution(self, bonus_solution_word1: str, bonus_solution_word2: str) -> bool:
        # To be an achievable bonus solution, word1 and word2 must appear in the
        # word list, they must be playable within the given letter sets, they
        # must chain last-to-first letter, and their combined letter set must
        # be the same as the letter set in the given letters.
        bonus_ok: bool = True
        word1 = bonus_solution_word1.upper()
        word2 = bonus_solution_word2.upper()
        if not self.word_list.contains(word1):
            print("ERROR:", word1, "is not in the word list.")
            bonus_ok = False
        if not self.word_list.contains(word2):
            print("ERROR:", word2, "is not in the word list.")
            bonus_ok = False
        if not self.letters_are_playable(word1):
            print("ERROR:", word1, "cannot be played in this game:", self.letters)
            bonus_ok = False
        if not self.letters_are_playable(word2):
            print("ERROR:", word2, "cannot be played in this game:", self.letters)
            bonus_ok = False
        if not (word1[-1] == word2[0]):
            print("ERROR:", word1, word2, "does not connect.")
            bonus_ok = False
        test_set = set(word1) | set(word2)
        all_letters = self.letter_sets.all_letters # just convenience
        if len(test_set) > len(all_letters):
            print("ERROR:", word1, word2, "contains more letters than", self.letters)
            bonus_ok = False
        elif not test_set == all_letters:
            print("ERROR:", word1, word2, "does not solve the game.")
            bonus_ok = False
        if bonus_ok:
            self.bonus_solution = "{}:{}".format(word1, word2)
        return bonus_ok
    
    @classmethod
    def new_game(cls, letters: str, bonus_solution_word1: str, bonus_solution_word2: str) -> object:
        word_train = WordTrains()
        word_train.set_letter_sets(letters)
        word_train.read_word_list(WORDNIK_WORDLIST_PATH)
        word_train.read_word_list(WORDNIK_ADDITIONS_PATH)
        word_train.set_bonus_solution(bonus_solution_word1, bonus_solution_word2)
        return word_train

def how_many_wordles_can_yield_5_yellows():
    valid_guesses = WordList.from_file('wordle/wordle-nyt-allowed-guesses-update-12546.txt')
    answers = WordList.from_file('wordle/wordle-nyt-answers-alphabetical.txt')
    print('nonanswer guesses len=', len(valid_guesses))
    #print('answers len=', len(answers))
    valid_guesses.add_wordlist(answers)
    print('valid guesses (includes answers) len=', len(valid_guesses))

    # The guess_anagrams dict INCLUDES answers
    guess_anagrams = AnagramsDict()
    guess_anagrams.add_wordlist(valid_guesses)
    guess_anagrams.prune()
    #print('len GUESS anagrams(pruned)=', len(guess_anagrams))
    #print('total words in GUESS anagrams(pruned)=', guess_anagrams.total_words())

    # answer_anagrams is JUST answers.
    answer_anagrams = AnagramsDict()
    answer_anagrams.add_wordlist(answers)
    # answer_anagrams.prune() - don't prune answer angrams: these might have anagrams in the total valid guesses set, that didn't appear in the answers-only set.
    #print('len ANSWER anagrams=', len(answer_anagrams))
    #print('total words in ANSWER anagrams=', answer_anagrams.total_words())

    # Now figure out which possible guess anagrams contain at least one answer - this is the set we're interested in.
    # This is the same as removing any guess anagram set whose key sorted_letters does NOT appear in the answer anagrams.
    delkeys = [k for k in guess_anagrams.anagrams if not k in answer_anagrams.anagrams]
    guess_anagrams.prune_keys(delkeys)
    #print('len GUESS/ANSWER anagrams=', len(guess_anagrams))
    #print(guess_anagrams)

    print('# of answers:', len(answers.word_list))
    print('# of anagram sets containing an answer:',len(guess_anagrams))
    n_with_anagrams = 0
    n_with_yyyyy = 0
    MAX_N_YYYYY = 8 # found by earlier runs
    max_n_yyyyy_words = []
    word: Word = None
    dez = None
    for word in answers.word_list:
        word_letters_sorted = word.sorted_letters()
        if word_letters_sorted in guess_anagrams.anagrams:
            n_with_anagrams += 1
            guesses = guess_anagrams.anagrams[word_letters_sorted]
            if word.word == 'STARE':
                dez = guesses
            wordle = Wordle.from_str(word.word)
            n_yyyyy = 0
            for guess in guesses:
                if guess != word.word:
                    score, g, w, sl = wordle.guess(guess)
                    assert(g == guess and w == word.word)
                    if (score == 'yyyyy'):
                        n_yyyyy += 1
                        print(score, g, w)
            if n_yyyyy > 0:
                n_with_yyyyy += 1
                if n_yyyyy == MAX_N_YYYYY:
                    max_n_yyyyy_words.append(word.word)

    print('# of answer words in an anagram set:', n_with_anagrams)
    print('# of answer words with an anagram scored yyyyy:', n_with_yyyyy)
    print('words with max # (8) of anagrams scored yyyyy:', max_n_yyyyy_words)
    print('STARE anagrams:', dez)
    
def wordle_tests():
    # Now I have a Wordle scorer!
    #wordle = Wordle.from_str('three')
    #wordle = Wordle.from_str('there')
    # print(wordle.guess('plain'))
    # print(wordle.guess('roust'))
    # print(wordle.guess('array'))
    # print(wordle.guess('terry'))
    # print(wordle.guess('three'))
    # print(wordle.guess('emcee'))
    # print(wordle.guess('there'))
 
    # wordle = Wordle.from_str('tibia')
    # print(wordle.guess('video'))
    # print(wordle.guess('first'))
    # print(wordle.guess('minty'))
    # print(wordle.guess('pitch'))
    # print(wordle.guess('timid'))
    # print(wordle.guess('idiot'))
    # print(wordle.guess('radii'))
    # print(wordle.guess('tibia'))

    # wordle = Wordle.from_str('brisk')
    # print(wordle.guess('judge'))
    # print(wordle.guess('faint'))
    # print(wordle.guess('crisp'))
    # print(wordle.guess('brisk'))

    # wordle = Wordle.from_str('soggy')
    # print(wordle.guess('nobly'))
    # print(wordle.guess('wormy'))
    # print(wordle.guess('poesy'))
    # print(wordle.guess('soggy'))

    # wordle = Wordle.from_str('usurp')
    # print(wordle.guess('hunch'))
    # print(wordle.guess('strum'))
    # print(wordle.guess('brusk'))
    # print(wordle.guess('usury'))
    # print(wordle.guess('unsur'))
    # print(wordle.guess('usurp'))

    # wordle = Wordle.from_str('howdy')
    # print(wordle.guess('panty'))
    # print(wordle.guess('lousy'))
    # print(wordle.guess('roomy'))
    # print(wordle.guess('boggy'))
    # print(wordle.guess('cocky'))
    # print(wordle.guess('hooey'))
    # print(wordle.guess('howdy'))
    # print('\nBOT:')
    # print(wordle.guess('least'))
    # print(wordle.guess('crony'))
    # print(wordle.guess('doggy'))
    # print(wordle.guess('howdy'))

    # wordle = Wordle.from_str('floor')
    # print(wordle.guess('ruing'))
    # print(wordle.guess('tread'))
    # print(wordle.guess('porky'))
    # print(wordle.guess('whorl'))
    # print(wordle.guess('floor'))

    # wordle = Wordle.from_str('catch')
    # print(wordle.guess('crumb'))
    # print(wordle.guess('carom'))
    # print(wordle.guess('catty'))
    # print(wordle.guess('catch'))

    # wordle = Wordle.from_str('denim')
    # print(wordle.guess('apple'))
    # print(wordle.guess('steer'))
    # print(wordle.guess('decoy'))
    # print(wordle.guess('debug'))
    # print(wordle.guess('denim'))

    # wordle = Wordle.from_str('mummy')
    # print(wordle.guess('plain'))
    # print(wordle.guess('roust'))
    # print(wordle.guess('duchy'))
    # print(wordle.guess('gummy'))
    # print(wordle.guess('mummy'))

    # wordle = Wordle.from_str('libel')
    # print(wordle.guess('phone'))
    # print(wordle.guess('teary'))
    # print(wordle.guess('embed'))
    # print(wordle.guess('libel'))

    # wordle = Wordle.from_str('waltz')
    # print(wordle.guess('lithe'))
    # print(wordle.guess('stall'))
    # print(wordle.guess('bloat'))
    # print(wordle.guess('malty'))
    # print(wordle.guess('waltz'))
    pass

def all_wordleable_wordlist() -> WordList:
    wordleable = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    wordleable.add_wordlist(answers)
    wordleable.sort()
    return wordleable

def count_repeat_letters():
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    #print('nonanswer guesses len=', len(valid_guesses))
    #print('answers len=', len(answers))
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()
    
    for w in valid_guesses.word_list:
        # Count repeated letters in each word.
        # If the word's letter set length is 5, there are no repeated letters = 0
        if len(w.letter_set) == 5:
            print("h-gram:", w) # count: 9365 (these are heterograms aka h-grams)
        elif len(w.letter_set) == 4: # There can only be one letter repeated one time: DL(a)
            print("1 DL (case a):", w) # count: 4899 (but this is an undercount so far)
        elif len(w.letter_set) == 3: # There can be one or two repeated letters
            # 578 words fall into this case.
            # If there are two repeated letters, each is repeated once: DL(b) eg ANNAL
            # If there's only one repeated letter, it's a triple (TL) eg NANNY

            # Count how many letters in the set occur more than once in the word.
            letters_list = list(w.word)
            n_repeated_letters = 0
            for c in w.letter_set:
                if letters_list.count(c) > 1:
                    n_repeated_letters += 1
            if n_repeated_letters == 2:
                print("2 DL (case b):", w) # 430 words
            elif n_repeated_letters == 1:
                print("TL (case a):", w) # 148 words
            else:
                print('!!!!!', w) # No words should fall into this case!

        elif len(w.letter_set) == 2:
            # There are 14 words (as of this writing: 16 Sept 2023) in this case.
            # These all comprise one triple and one double letter.
            # AGGAG ALALA ANANA ANNAN AYAYA COCCO ESSES LOLLO MAMMA NANNA NONNO PEEPE SUSUS TAATA
            print("TL (case b):", w) 
        else:
            print('!!!!!', w) # No words should fall into this case!
        
    #pass

def count_palindromes():
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    non_answers = WordList.from_file(WORDLE_GUESSES_PATH)
    print('answers len=', len(answers))
    for w in answers.word_list:
        if w.is_palindrome():
            print(w)
    print('non-answers len=', len(non_answers))
    for w in non_answers.word_list:
        if w.is_palindrome():
            print(w)
        
def find_subsets(subset_list):
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()

    for subset_str in subset_list:
        print("####", subset_str)
        test_set = set(subset_str.upper())
        for w in valid_guesses.word_list:
            # If the candidate letter set is a subset of the word's letter set then that's what we're looking for!
            if test_set.issubset(w.letter_set):
                print("1. `{}`".format(w))
        
def find_subsets_of(superset_list):
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()

    for superset_str in superset_list:
        print("####", superset_str)
        test_set = set(superset_str.upper())
        for w in valid_guesses.word_list:
            # If the word's letter set is a subset of this superset, then that's what we're looking for!
            if w.letter_set.issubset(test_set):
                print("1. `{}`".format(w))
        
def find_month_abbrev_words():
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()
    
    mondict = {'JAN': "January", 'FEB': "February", 'MAR': "March", 'APR': "April", 'MAY': "May", 'JUN': "June", 'JUL':"July", 'AUG': "August", 'SEP': "September", 'OCT': "October", 'NOV': "November", 'DEC': "December"}
    
    for mon, month in mondict.items():
        print("####", mon, month)
        mon_set = set(mon)
        month_set = set(month.upper())
        for w in valid_guesses.word_list:
            # If the month letter set is a subset of the word's letter set then that's what we're looking for!
            if mon_set.issubset(w.letter_set):
                # Check also and put a '*' on words that are also a proper subset of the full month name.
                asterisk = '*' if w.letter_set.issubset(month_set) else ''
                if asterisk != '':
                    print("1.", w, asterisk)
        
def find_month_subset_words():
    find_subsets_of(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
def find_day_abbrev_words():
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()

    for day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
        print("####", day)
        day_set = set(day)
        for w in valid_guesses.word_list:
            # If the day letter set is a subset of the word's letter set then that's what we're looking for!
            if day_set.issubset(w.letter_set):
                print("1.", w)

def find_name_words():
    valid_guesses = WordList.from_file(WORDLE_GUESSES_PATH)
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    valid_guesses.add_wordlist(answers)
    print('All valid guesses (includes answers) len=', len(valid_guesses))
    valid_guesses.sort()

    for name in ['DEZ','DOC','LIZ']:
        print("####", name)
        name_set = set(name)
        for w in valid_guesses.word_list:
            # If the name letter set is a subset of the word's letter set then that's what we're looking for!
            if name_set.issubset(w.letter_set):
                print("1.", w)

def find_letter_homes(letter: str, answers: WordList):
    stats = dict()
    N = 0
    slot_count = [0, 0, 0, 0, 0]
    rl_count = 0
    for w in answers.word_list:
        # First filter: the word must contain the letter
        if letter in w.letter_set:
            N += 1
            rl = 0
            # Now each time the letter appears in the word, increment the count in that slot.
            # Also count up how many times the letter appears (repeats) in the word (RL).
            for i in range(5):
                if w.word[i] == letter:
                    slot_count[i] += 1
                    rl += 1
            if rl > 1:
                rl_count += 1
                print(w)
            
    pct_has_letter = round((N / len(answers)) * 100)
    pct_slot = [0, 0, 0, 0, 0]
    pct_slot[0] = round((slot_count[0] / N) * 100)
    pct_slot[1] = round((slot_count[1] / N) * 100)
    pct_slot[2] = round((slot_count[2] / N) * 100)
    pct_slot[3] = round((slot_count[3] / N) * 100)
    pct_slot[4] = round((slot_count[4] / N) * 100)
    print(f"`{letter}`|{N:4d}|{pct_has_letter:2d}", end='')
    for p in pct_slot:
        print(f"|{p:2d}", end='')
        
    print("|{:3d}".format(round((rl_count / N) * 100)), end='')
    
    #print(" ", slot_count)
    print()
    
def find_Z_homes():
    answers = WordList.from_file(WORDLE_ANSWERS_PATH)
    answers.sort()
    print(len(answers))
    #for letter in ALPHABET_LIST:
    #    find_letter_homes(letter, answers)
    find_letter_homes('F', answers)

def write_wordnik_words():
    wordnik_all = WordList.from_file(WORDNIK_WORDLIST_PATH)
    print("Wordnik N=", len(wordnik_all))
    for w in wordnik_all.word_list:
        print(w)

def test_word_trains():
    # how_many_wordles_can_yield_5_yellows()
    # count_repeat_letters()
    # count_palindromes()
    # find_month_subset_words()
    # find_Z_homes()
    # write_wordnik_words()
    wt = WordTrains.new_game("iod hua mpl rnc", "holdup", "panoramic")
    wt.test_play_letters("unproud")
    wt.test_play_letters("ram")
    wt.test_play_letters("ilch")
    ### End train, complete
    wt.test_play_letters("phonic")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("propound")
    wt.test_play_letters("urian")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("mandala")
    wt.test_play_letters("rmour")
    wt.test_play_letters("iparian")
    wt.test_play_letters("ach")
    ### End train, complete
    wt.test_play_letters("palomino")
    wt.test_play_letters("uch")
    wt.test_play_letters("our")
    wt.test_play_letters("ad")
    ### End train, complete
    wt.test_play_letters("AROUND")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("COLUMNAR")
    wt.test_play_letters("OUNDUP")
    wt.test_play_letters("HONIC")
    # train
    wt.test_play_letters("ROMANIUM")
    wt.test_play_letters("ulch")
    wt.test_play_letters("ip")
    wt.test_play_letters("ad")
    # train
    wt.test_play_letters("uranium")
    wt.test_play_letters("ochi")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("unipolar")
    wt.test_play_letters("omcom")
    wt.test_play_letters("orphia")
    wt.test_play_letters("nd")
    # train
    wt.test_play_letters("daphnia")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("oracular")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("raindrop")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("maildrop")
    wt.test_play_letters("ouch")
    wt.test_play_letters("on")
    # train
    wt.test_play_letters("aluminum")
    wt.test_play_letters("orphic")
    wt.test_play_letters("ad")
    # train
    wt.test_play_letters("morphium")
    wt.test_play_letters("ainland")
    wt.test_play_letters("ucal")
    # train
    wt.test_play_letters("maniacal")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("caldron")
    # Give up, dead end
    wt.new_train()
    wt.test_play_letters("holdup")
    wt.test_play_letters("anoramic")

def score_all_wordleable_words_by_digraphs():
    awl = all_wordleable_wordlist()
    wl = WordList.from_file(WORDLE_ANSWERS_PATH)
    di = wl.digraphs_by_word()

    word_digraph_score = dict()
    for w in awl.word_list:
        prev_letter = ''
        digraphs = set()
        for letter in w.word:
            if prev_letter != '':
                digraph = prev_letter + letter
                digraphs.add(digraph)
            prev_letter = letter
        score = 0
        for digraph in digraphs:
            score += di.get(digraph,0)
        word_digraph_score[w.word] = score

    for k,v in word_digraph_score.items():
        print(v, k)

def random200():
    awl = all_wordleable_wordlist()
    rwl = WordList.random_from_wordlist(awl,200)
    rwl.sort()
    for w in rwl.word_list:
        print(w)

def find_reversibles():
    awl = all_wordleable_wordlist()

    anagrams = PerfectAnagramsDict()
    anagrams.add_wordlist(awl)
    anagrams.prune() # remove items with only one anagram
    
    palindromes = list()
    seen = set()
    print("REVERSIBLE:")
    for w in awl.word_list:
        rw = w.reversed()
        if w == rw:
            palindromes.append(w)
        elif not w in seen and rw in awl.word_set:
            anas = anagrams.anagrams_of_word(w)
            print(f"1. `{w}`-`{rw}`", end='')
            if not anas is None and len(anas) > 1:
                anas.remove(rw.word)
                print("  [ ", end='')
                for a in anas:
                    print(f"`{a}` ", end='')
                print("]")
            else:
                print()
            seen.add(rw)
            
    print("PALINDROMES:", file=sys.stderr)
    for p in palindromes:
        print(f"1. `{p}`", file=sys.stderr)

def find_pu_anagrams():
    pu = WordList.from_file(WORDLE_PU_PATH)
    print("N=", len(pu))
    print("SEQUENTIAL PU ANAGRAMS:")
    prev_w = None
    for w in pu.word_list:
        if not prev_w is None:
            if w.is_anagram_of_word(prev_w):
                print(prev_w, w)
        prev_w = w

    print("ALL PU ANAGRAMS (regardless of order):")
    pu_anagrams = PerfectAnagramsDict()
    pu_anagrams.add_wordlist(pu)
    pu_anagrams.prune()
    pu_anagrams.sort()
    seq = 1
    for v in pu_anagrams.anagrams.values():
        print(seq, v)
        seq += 1

if __name__ == "__main__":
    # Print a random 100 lines from a file (presumably longer than 100 lines!)
    lines = list()
    with open('wordnik-beewords', 'r') as f:
        for line in f:
            lines.append(line)
    print("N lines = ", len(lines))
    random100 = random.sample(lines, 100)
    print("N random lines = ", len(random100))
    random100.sort()
    for l in random100:
        print(l, end='')
