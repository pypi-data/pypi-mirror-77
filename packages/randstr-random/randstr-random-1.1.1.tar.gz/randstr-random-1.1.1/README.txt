randstr-random

A Python package for generating strings with random characters built on top of the random module.

Make sure to have the latest version of Python 3 installed although this should work with previous versions. 

To install the package with pip enter command in terminal:
    pip install randstr-random

To uninstall the package with pip enter command in terminal:
    pip uninstall randstr-random


randdigit(): 	                        Generates a random digit ranging from 0 to 9 (Digits in Decimal Number System) and returns it as a string.

randalpha(): 	                        Generates a random lowercase letter from the english alphabet and returns it as a string.

randspec(): 	                        Generates a random special character and returns it as a string.

generate(string_length, seed_type): 	Return a string with random values of designated int length (Cap of 10000). The random value combos are selected by using a specific string for the seed_type argument.

The seed_type argument value options (not case sensitive) are as follows:

"al" - (Alphabet Lower) Random lowercase alphabet letters.

"au" - (Alphabet Upper) Random uppercase alphabet letters.

"dig" - (Digit) Random digits 0-9.

"spec" - (Special) Random special characters.

"ad" - (Alphabet Lower | Alphabet Upper | Digit) Random lowercase & uppercase alphabet letters. Random digits 0-9.

"ads" - (Alphabet Lower | Alphabet Upper | Digit | Special) Random lowercase & uppercase alphabet letters. Random digits 0-9. Random special characters.

isspec(arg): 	                    Return true if all characters in arg string are special characters.

isads(arg): 	                    Return true if all characters in arg string are either upper/lower case alphabet, decimal or special characters. 