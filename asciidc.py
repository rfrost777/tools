#!/usr/bin/env python3
#########################################################################
# Quick Python tool to decode the output of the nice netcat living at:
# nc mercury.picoctf.net 49039 > message.txt
# for picoCTF (plain text ASCII values, separated by \n)...
#########################################################################
import sys
import os.path


def main() -> None:
    if not (1 < len(sys.argv) <= 2):
        # something seems off, better print out usage and exit nonzero
        print(f"Usage: {sys.argv[0]} <filename> to decode the ASCII contents of filename.\n")
        sys.exit(1)
    else:
        # looks good, get the argument(s) from argv
        [_, f_name] = sys.argv

    # check if argument is a path to an existing file, else print an error
    if os.path.isfile(f_name):
        with open(f_name) as file:
            content = file.read().splitlines()
        # iterate over the file contents of f_name and output the decoded chars in one line for easier copypasta
        for c in content:
            print(chr(int(c)), end="")
        sys.exit(0)
    else:
        print(f"File: {f_name} does not exist. Nothing to do.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
