#########################################################################
# Quick Python tool to decode the output of the nice netcat living at:
# nc mercury.picoctf.net 49039
# for picoCTF (plain text ASCII values, separated by \n)...
#########################################################################
import sys
import os.path

if len(sys.argv) != 2:
    # check if the user provided us with an argument
    print(f"Usage: {sys.argv[0]} <filename> to decode the ASCII contents of filename.\n")
else:
    # check if argument is a path to an existing file, else print an error
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as file:
            content = file.read().splitlines()
        # iterate over the file contents and output the decoded chars in one line for easier copypasta
        for c in content:
            print(chr(int(c)), end="")
    else:
        print(f"File: {sys.argv[1]} does not exist. Nothing to do.\n")
