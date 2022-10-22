###################################################
# Decode a ROT13 encoded string and print out its
# content. Used for picoCTF MOD26 challenge.
# I KNOW there is a function for this in codecs,
# but where is the fun in that?
#
# 17-08-2022:   Added a ROT47 function for use in
#               the THM Overpass room.
###################################################
import sys


def rot13hardcoded(phrase: str) -> str:
    # Let's hardcode a transformation scheme:
    key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    crypt = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    # with import string: key = string.ascii_letters; crypt = key[13:] + key[:13]
    # but let's limit our self's to pure build-in functions ;)
    transform = dict(zip(key, crypt))
    # Transform every character accordingly!
    return ''.join(transform.get(char, char) for char in phrase)


def rot13elegant(phrase: str) -> str:
    # Try each character in phrase and ROT13 if it is an ASCII alpha character:
    d = {}
    for character in (65, 97):
        for i in range(26):
            d[chr(i+character)] = chr((i+13) % 26 + character)
    return ''.join([d.get(character, character) for character in phrase])


def rot47elegant(phrase: str) -> str:
    d = []
    # I basically use the same trick as in rot13elegant(), check if phrase[i] is a printable
    # ASCII character, if yes then shift it, this time 47 "places"...
    for i in range(len(phrase)):
        j = ord(phrase[i])
        if 33 <= j <= 126:
            d.append(chr(33 + ((j+14) % 94)))
        else:
            d.append(phrase[i])
    return ''.join(d)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} '<your text to encode or decode>'\n")
    else:
        print(f"Original string is: {sys.argv[1]}\n")

    # This works both ways because ROT13/47 are mathematically involutions.
    print(f"* Encoded/decoded string is: {rot13hardcoded(sys.argv[1])}\n")
    print(f"* More elegant encoded: {rot13elegant(sys.argv[1])}\n\n")
    print(f"* ROT47 en-/decoded should be: {rot47elegant(sys.argv[1])}\n")


if __name__ == "__main__":
    main();