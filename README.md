MarkovNames is a simple name generator based on Markov chains. In its initial,
untrained state, the generator returns random strings of alternating consonants
and vowels, with the possibility of using some common (English) all-consonant or
all-vowel combinations. Names can be added to the generator, and it will attempt
to generate similar random names. Undesired sequences of characters can also be
blacklisted.

Constructing a name generator:
NameGen's constructor takes two integers, representing the minumum (inclusive)
and maximum (exclusive) desired lengths. NameGen makes no attempt to error-
check these values. NameGen also provides a second constructor that takes a seed
as the third argument.

Training the name generator:
NameGen.addName takes one string and will, after that, attempt to generate
similar names. NameGen will remove whitespace from the string, but will not
handle any other non-alphabetic characters.

Generating names:
NameGen.getName will generate and return a name.

Blacklisting a character sequence:
NameGen.removeName takes one string and will prevent that sequence from being
generated. Note that, because of the Markov Property, the entire sequence is
removed, so if you remove the sequence "jfthg", the "th" combination will never
be generated. Remove "jft" and "hg" instead.

GenMain is provided as an example of NameGen's usage. GenMain is a complete
program that runs from the command line.
Usage: java GenMain [min] [max] <options>
Options:
   -d - print the Markov chain as names are generated
   -s - seed the generator with '0'
   -f - train the generator using names from a file
Commands:
   add - add a name to the Markov chain
   gen - generate a name
   like - add the last generated name to the Markov chain
   ban - remove a letter sequence from the chain
   quit - ...quits

