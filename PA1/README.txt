How to compile:
To run my code you will need python 3 install. I am using 3.6.4 but that shouldn't matter.
File names given are in relation to where the file is run. aka if it's in the same directory
just use the name. If it is in a sub directory it must be names with the directory in it
Encode:
python3 compression.py -n <x> <y> <file>
<x> => This is your encoding option. Replace w/ 0 for FC and 1 for NC
<y> => This is your decoding option. 0 => freeze, 1 => restart, 2 => LRU

Decode:
python3 compression.py -d <x> <y> <file>
<x> => This is your encoding option. Replace w/ 0 for FC and 1 for NC
<y> => This is your decoding option. 0 => freeze, 1 => restart, 2 => LRU
The same encode and decode option must be used.

How it works:
My code is built around python's ordered dictionary. For encoidng it is mapped from bytes to ints.
For decoding both a mapping from byte to int and int to byte is maintained. This duel mapping makes it
so you do not need to use a trie. This requires more memory but runs faster in most cases.
My code attempts to read in a byte and check if it is in the dictionary. If it is, it will try to keep going until
it found a grouping that is not in the dict and will then move back one space.
Once it is found, it is important to move that to the end of the dictionary to ensure that LRU will work
It is written to the file and the modifier is called. The only one of interest is LRU, in this case
LRU finds the least frequent in the dict that isn't part of the beginning 0 - 255 bytes.
This pair is removed and the new fc/nc mod takes place. This process is the same for decoding expect that
it keeps the reverse dictionary up to date.