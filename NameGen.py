# Generates random names based on Markov chains of characters.
# A Python port of NameGen.java
# author: Christopher (cesiu)
# date: 30 Jun 2016
# Written for Python 2.6.6

import random
import string
from copy import deepcopy
from sys import argv

class NameGen:
    # all the vowels
    VOWELS = 'aeiouy'
    # all the consonants
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

    # Constructs a NameGen and initializes the states.
    # min_len - the minimum desired word length, inclusive
    # max_len - the maximum desired word length, exclusive
    # [gen_seed] - a seed for the random number generator
    def __init__(self, min_len, max_len, gen_seed = None):
        self.min_len = min_len
        self.max_len = max_len
        random.seed(gen_seed)

        # All the states are stored in a dictionary mapping characters to their
        # respective states. Individual states are lists where the first
        # element is the total number of next states and the second element is
        # a dictionary mapping next states to their frequencies.

        # Set consonants and vowels to alternate in an untrained generator.
        vowel_dict = dict(dict((char, 0) for char in self.VOWELS), \
                          **dict((char, 1) for char in self.CONSONANTS))
        cons_dict = dict(dict((char, 0) for char in self.CONSONANTS), \
                         **dict((char, 1) for char in self.VOWELS))

        self.states = dict( \
         dict((vowel, [len(self.CONSONANTS), deepcopy(vowel_dict)]) \
              for vowel in self.VOWELS), \
         **dict((cons, [len(self.VOWELS), deepcopy(cons_dict)]) \
              for cons in self.CONSONANTS))

        # 'y's can initially be followed by any other character.
        self.states['y'] = [25, dict((char, 1) if char != 'y' else (char, 0) \
                            for char in string.ascii_lowercase)]
        # The first letter can be any character.
        self.begin_state = [26, dict((char, 1) \
                            for char in string.ascii_lowercase)]

    # Trains the generator using a name.
    # name - the name to use
    def add_name(self, name):
        # Sanitize the string.
        name = string.lower(name.strip())
        if name:
            # Add the first letter to the beginning state.
            self.begin_state[1][name[1]] += 1
            self.begin_state[0] += 1
            # For every character except the last in the name:
            for (idx, char) in enumerate(name[:-1]):
                # Add the character after it to its state.
                self.states[char][1][name[idx + 1]] += 1
                self.states[char][0] += 1

    # Removes a sequence from the Markov chain.
    # name - the sequence to remove
    def remove_name(self, name):
        # Do the same as for adding, except reset to zero instead of adding one.
        self.begin_state[0] -= self.begin_state[1][name[1]]
        self.begin_state[1][name[1]] = 0
        for (idx, char) in enumerate(name[:-1]):
            self.states[char][0] -= self.states[char][1][name[idx + 1]]
            self.states[char][1][name[idx + 1]] = 0

    # Generates a random name.
    # returns a string
    def gen_name(self):
        # Pick a letter from the beginning state. 
        ret_str = self.next_char(self.begin_state, "[begin]")
        # Pick a random length with the desired bounds, then pick letters from
        # the states of the last picked letters until the string is that long.
        for i in range(random.randint(self.min_len, self.max_len - 1) - 1):
            ret_str += self.next_char(self.states[ret_str[-1]], ret_str[-1])
        # Return the name, capitalized.
        return string.capitalize(ret_str)

    # A helper function, picks a random next character from a given state.
    # cur_state - the pair representing the current state.
    # cur_char - the last picked character
    def next_char(self, cur_state, cur_char):
        # Generate a random number within the total number of states seen.
        choice = random.randint(0, cur_state[0] - 1)
        chance = 0

        # For each next character in the state:
        for (pos_char, pos_qty) in cur_state[1].iteritems():
            # Add the chance of picking that character.
            chance += pos_qty
            # If the number is less than the chance, return the character.
            if choice < chance:
                return pos_char

        # If we get this far, we generated a number that was too large.
        raise Exception("Error: %s: invalid choice(%d) for total of %d." \
                        % (cur_char, choice, cur_state[0]))

    # Returns a string representation of all the states.
    # returns a string
    def __str__(self):
        return ''.join("%s:\n   %s\n\n" % (char, str(self.states[char])) \
                       for char in self.states.keys())

def main():
    if len(argv) < 3:
        print "Usage: python NameGen.py [min] [max]"

    gen = NameGen(int(argv[1]), int(argv[2]))

    choice = raw_input("Enter a command: ")
    while choice != "quit":
        if choice == "gen":
            print gen.gen_name()
        elif choice == "file":
            filename = raw_input("Enter filename: ")
            with open(filename, 'r') as name_file:
                for name in name_file:
                    gen.add_name(name)
        choice = raw_input("Enter a command: ")

if __name__ == "__main__":
    main()
