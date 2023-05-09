#!/usr/bin/env python3
#############################################################
#   Custom Fuzzing Script for a basic, Captcha protected
#   login page.
#   Used in the TryHackMe Room: Capture!
#   ( https://tryhackme.com/room/capture )
#############################################################
# import urllib.request
# from bs4 import BeautifulSoup

# Point this to your target box:
target_ip: str = '10.10.10.10'


def solve_captcha(captcha: str) -> int:
    # This function calculates the actual captcha and returns the result.
    # First split the captcha string by blanks:
    components: list = captcha.split()
    print(f"I have gotten {components} out of the string!")
    operand_one: int = int(components[0])
    operator: str = components[1]
    operand_two: int = int(components[2])
    # Return a result depending upon the operator
    match operator:
        case '+':
            return operand_one + operand_two
        case '-':
            return operand_one - operand_two
        case '*':
            return operand_one * operand_two
        case '%':
            return operand_one % operand_two
        case _:
            # Catch all the remaining cases and raise an error:
            raise NotImplementedError("Operator not supported (yet).")


def load_dictionary(filename: str) -> list:
    # Logic for loading our wordlists and converting them
    # into lists line-by-line for easier handling later on.
    with open(filename, 'r', encoding="utf-8") as file:
        raw_data: str = file.read()
    wordlist: list = raw_data.splitlines()
    print(f"[=] Loaded wordlist {filename} for: {len(wordlist)} items.")
    return wordlist


if __name__ == '__main__':
    print(f"First Test: {solve_captcha('200 % 10')}, second Test: {solve_captcha('200 - 10')}.")

    passwords: list = load_dictionary('./passwords.txt')
    usernames: list = load_dictionary('./usernames.txt')
    # login_page = urllib.request.urlopen(f'http://{target_ip}/login')
    # print(login_page.read())
    