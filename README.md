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
