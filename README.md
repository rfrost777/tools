# Tools
Assorted tools I wrote for CTF's, pen-testing or as a pastime of sorts.


## asciidc.py
I used this to decode an ASCII-output I got from picoCTF's mercury.picoctf.net
netcat. Reads a file with numbers in it, one number per line ending in \n and interprets those as
ASCII-Codes. Writes the characters to STDOUT for easy copypasta.

Usage:
`python3 asciidc.py <filename>`


## b64tool.py
Encodes/decodes strings Base64, normal and url-safe. Wrote this because I was too lazy to pull up
CyberChef in my browser... and I really needed this one string decoded!

Usage:
`python3 b64tool.py [-h] [--urlsafe] {dec,enc} <inputstring>`

## ntlm_passwordspray.py
A simple Password sprayer for NTLM (web-)endpoints.
I used this to throw a company standard password at enumerated user accounts on a NTLM weblogin endpoint to where it sticks. Aka what users did not change their
default credentials as they were told to do...
You _could_ use hydra for this, but this way I had more control over the process,
as hydra tends to make alot of noise.
*TODO* Switch from getopt to argparse for a less redundant options handling?

Usage:
`ntlm_passwordspray.py -u <enumerated_userfile> -f <fqdn> -p <std_password> -a <attackurl>`


## get_exports.py / proxy.c
Rips the export table from a WINDOWS DLL and dumps it to a file. Used for WINDOWS PrivEsc via
proxy DLL (use the code in proxy.c as a simple example). See resp. comments in those files for more info.
Credit: borrowed and modified from the Cobalt-Strike git repo.

Usage:
`python3 get_exports.py --target <FILENAME>.dll --originalPath 'C:\Windows\System32\<FILENAME>.dll' > proxy.def`


## ltdis.sh
Shell-script wrapper that leverages objdump to extract the .text section of a given binary. Use it to discover
interesting strings in binary's, like c2-server addresses or bitcoin wallets. Very useful in forensic CTF's.

Usage:
`ltdis.sh <binary>`


## dvwa_bruteit.sh / dvwa_patator.sh
Two shell scripts I improvised while attacking the webapp login page of a DVWA machine, following the THM room
"Brute Force Heroes" (https://tryhackme.com/room/bruteforceheroes). Using ZAP and/or hydra did not work at all for me
so I used good old curl. The command line in the Patator task seemed wrong to me too and did not work in my
Kali 2023.2 VM, so I improved and fixed that. The provided TryHackMe DVWA used "Impossible" security level settings,
so I had to work arround a PHP-SessionID and a Cross-Site-Request-Forgery (CSRF) token. Edit the setup section in those
scripts to your needs and fire away.

Usage:
`./dvwa_bruteit.sh` or
`./dvwa_patator.sh`


## lyrics2.rock
A CTF challenge written in Rockstar. Yeah, I know. That's really a thing. Roll with it...


## rot_encode.py
10 ways of encoding/decoding a string in ROT13/47 without using python library's. Okay I could only think of two
ways right now. *TODO*: Maybe add some more ways later?

Usage:
`python3 rot_encode.py <Your Text here>`


## zerologon.py
Windows ZeroLogon Exploit (CVE-2020-1472) using the python impacket toolset.
Credit: Modified and weaponized from the Secura PoC found at
https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon_tester.py

Usage:
`python3 zerologon.py <dc-name> <dc-ip>`


## portscan.py
Simple TCP Portscanner that scans ports from 1 to max_port. 
Added: --debug switch to write a logfile with more information.
*TODO*: Make it more useful. Maybe increase efficiency?

Usage:
`python3 portscan.py [-h] [--debug] <ip_address> <max_port>`


## redirect.py
Sets up a simple http redirect (302) using Python's own HTTPServer module.
Useful in some CTF-Boxes. Exit using <CTRL><C>. *TODO*: Use argparse to check command line arguments.

Usage:
`python3 redirect.py <port_number> <target-url>`


## captcha_fuzz.py
Custom username/password fuzzing Script for a basic, Captcha-protected login page.
Used in the TryHackMe Room: Capture! (https://tryhackme.com/room/capture)
*TODO*: WIP...


## timing_exploit.py
Timing attack exploit of a poorly designed hashing function on the login form from the THM-hackerNote Room:
https://tryhackme.com/room/hackernote
You can increase your success chance by adding your own username to the top of the name list
Assumes you have at least ONE correct username, use the "create account" button for that.
*Credit(s)*: Borrowed and improved from NinjaJc01 (James):
https://github.com/NinjaJc01/hackerNoteExploits

Usage:
`Edit the top of the python code with <target_hostname> and your <namelist_to_use>, then fire away.`


## date_gen.py
Outputs a custom date world-list in the format YYYYMMDD to STDOUT. I needed this for a CTF and couldn't
get it done using CRUNCH, so, there you go. Write to a file using:
`python3 date_gen.py > my_wordlist.txt`


## shellcode_dropper.cpp
A simple Windows shellcode dropper template that tries to take an educated guess if it's run in a sandbox environment.
Downloads and executes a raw msfvenom tcp reverse_shell payload from a C2 server if not sandboxed. I used this in the TryHackMe
Room: Sandbox Evasion. For educational purposes only!
*TODO*: Add more (elaborate) sandbox checks to refine the guess.
*ADDED*: Simple, basic anti-debugging code using SuspendThread().

## rogue_http_server.py
Extended python http.server module to capture (and save) post requests from indirect (blind)
SSRF attacks and so on...
*TODO*: It works as-is, but I coded it like a caveman (method overloading in python, bruah?).
Add more nifty features I might need in the future.
