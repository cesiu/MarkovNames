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
        # so it's a map of characters to lists of totals and maps of characters to quantities.
        # {c: [t, {l: n}]}
        vowel_map = dict(dict((char, 0) for char in self.VOWELS), **dict((char, 1) for char in self.CONSONANTS))
        cons_map = dict(dict((char, 0) for char in self.CONSONANTS), **dict((char, 1) for char in self.VOWELS))

        self.states = dict(dict((vowel, [len(self.CONSONANTS), deepcopy(vowel_map)]) for vowel in self.VOWELS), **dict((cons, [len(self.VOWELS), deepcopy(cons_map)]) for cons in self.CONSONANTS))

        self.states['y'] = [25, dict((char, 1) if char != 'y' else (char, 0) for char in string.ascii_lowercase)]

        self.begin_state = [26, dict((char, 1) for char in string.ascii_lowercase)]

    def add_name(self, name):
        self.begin_state[1][name[1]] += 1
        self.begin_state[0] += 1
        for (idx, char) in enumerate(name[:-1]):
            self.states[char][1][name[idx + 1]] += 1
            self.states[char][0] += 1

    def remove_name(self, name):
        self.begin_state[0] -= self.begin_state[1][name[1]]
        self.begin_state[1][name[1]] = 0
        for (idx, char) in enumerate(name[:-1]):
            self.states[char][0] -= self.states[char][1][name[idx + 1]]
            self.states[char][1][name[idx + 1]] = 0

    def gen_name(self):
        ret_str = self.next_char(self.begin_state, "[begin]")
        for i in range(random.randint(self.min_len, self.max_len - 1) - 1):
            ret_str += self.next_char(self.states[ret_str[-1]], ret_str[-1])
        return ret_str

    def next_char(self, cur_state, cur_char):
        choice = random.randint(0, cur_state[0] - 1)
        chance = 0

        for (pos_char, pos_qty) in cur_state[1].iteritems():
            chance += pos_qty
            if choice < chance:
                return pos_char

        raise Exception("Error: %s: invalid choice(%d) for total of %d." % (cur_char, choice, cur_state[0]))

    def __str__(self):
        return ''.join("%s:\n   %s\n\n" % (char, str(self.states[char])) for char in self.states.keys())

g = NameGen(4,9)
print g
g.add_name("test");
print g
g.remove_name("lol");
print g
print g.gen_name()
