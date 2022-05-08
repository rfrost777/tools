###################################################
# Decode a ROT13 encoded string and print out its
# content. Used for picoCTF MOD26 challenge.
# I KNOW there is a function for this in codecs,
# but where is the fun in that?
###################################################
import sys


def rot13hardcoded(phrase):
    # Let's hardcode a transformation scheme:
    key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    crypt = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    transform = dict(zip(key, crypt))
    # Transform every character accordingly!
    return ''.join(transform.get(char, char) for char in phrase)


def rot13elegant(phrase):
    # Try each character in phrase and ROT13 if it is an ASCII alpha character:
    d = {}
    for character in (65, 97):
        for i in range(26):
            d[chr(i+character)] = chr((i+13) % 26 + character)
    return ''.join([d.get(character, character) for character in phrase])


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} '<your text to encode or decode>'\n")
else:
    print(f"Original string is: {sys.argv[1]}\n")

    # This works both ways because ROT13 is mathematically an involution.
    print(f"* Encoded/decoded string is: {rot13hardcoded(sys.argv[1])}\n")
    print(f"* More elegant encoded: {rot13elegant(sys.argv[1])}\n")
