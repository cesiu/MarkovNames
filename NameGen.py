# Generates random names based on Markov chains of characters.
# A Python port of NameGen.java
# author: Christopher (cesiu)
# date: 30 Jun 2016
# Written for Python 2.6.6

import random
import string
from copy import deepcopy

class NameGen:
    # Note: use string.ascii_lowercase instead of LOWERCHARS.
    VOWELS = 'aeiouy' 
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

    def __init__(self, min_len, max_len, gen_seed = None):
        self.min_len = min_len
        self.max_len = max_len
        random.seed(gen_seed)

        # map characters to states. Individual states are tuples of totals and maps of characters to quantities. 
        # so it's a map of characters to tuples of totals and maps of characters to quantities.
        # {c: (t, {l: n})}
        vowel_map = dict(dict((char, 0) for char in self.VOWELS), **dict((char, 1) for char in self.CONSONANTS))
        cons_map = dict(dict((char, 0) for char in self.CONSONANTS), **dict((char, 1) for char in self.VOWELS))

        self.states = dict(dict((vowel, (len(self.CONSONANTS), deepcopy(vowel_map))) for vowel in self.VOWELS), **dict((cons, (len(self.VOWELS), deepcopy(cons_map))) for cons in self.CONSONANTS))

        self.states['y'] = (25, dict((char, 1) if char != 'y' else (char, 0) for char in string.ascii_lowercase))

    def __str__(self):
        return ''.join(char + ':\n   ' + str(self.states[char]) + '\n\n' for char in self.states.keys())

g = NameGen(1,1)
print g
