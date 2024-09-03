#!/usr/bin/env python3
#################################################################################
#
#   Calculate a random Session Key from PCAP data to decrypt SMB3 traffic.
#   TryHackMe Room "BLOCK": https://tryhackme.com/r/room/blockroom
#
#   Idea stolen from Khris Tolbert: 
#   https://medium.com/maverislabs/decrypting-smb3-traffic-with-just-a-pcap-absolutely-maybe-712ed23ff6a2
#
#################################################################################
import hashlib
import hmac
import argparse
from Cryptodome.Cipher import ARC4
from Cryptodome.Hash import MD4

def calculate_ntlm_hash(password: str) -> bytes:
    passw = password.encode('utf-16le')
    return hashlib.new('md4', passw).digest()

def calculate_response_nt_key(password_hash: bytes, user: bytes, domain: bytes) -> bytes:
    h = hmac.new(password_hash, digestmod=hashlib.md5)
    h.update(user + domain)
    return h.digest()

def calculate_key_exchange_key(response_nt_key: bytes, nt_proof_str: bytes) -> bytes:
    h = hmac.new(response_nt_key, digestmod=hashlib.md5)
    h.update(nt_proof_str)
    return h.digest()

def generate_encrypted_session_key(key_exchange_key: bytes, exported_session_key: bytes) -> bytes:
    cipher = ARC4.new(key_exchange_key)
    return cipher.encrypt(exported_session_key)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate the SMB3 Random Session Key based on data from a PCAP.")

    # Use a password OR a ntlm hash, whatever is handy.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--password", help="Password of User")
    group.add_argument("-H", "--hash", help="NTLM Hash of the password (provide Hex Stream)")

    parser.add_argument("-u", "--user", required=True, help="User name")
    parser.add_argument("-d", "--domain", required=True, help="Domain name")
    parser.add_argument("-n", "--ntproofstr", required=True, help="NTProofStr. This can be found in PCAP (provide Hex Stream)")
    parser.add_argument("-k", "--key", required=True, help="Encrypted Session Key. This can be found in PCAP (provide Hex Stream)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    return parser.parse_args()

def main():
    args = parse_arguments()

    user = args.user.upper().encode('utf-16le')
    domain = args.domain.upper().encode('utf-16le')

    if args.password:
        # If password is given, calculate the corresponding ntlm hash first:
        password_hash = calculate_ntlm_hash(args.password)
    else:
        # If we can find the hash, or it's not feasible to crack the nt password, then use the hash directly:
        password_hash = bytes.fromhex(args.hash)

    response_nt_key = calculate_response_nt_key(password_hash, user, domain)

    nt_proof_str = bytes.fromhex(args.ntproofstr)
    key_exchange_key = calculate_key_exchange_key(response_nt_key, nt_proof_str)

    exported_session_key = bytes.fromhex(args.key)
    random_session_key = generate_encrypted_session_key(key_exchange_key, exported_session_key)

    if args.verbose:
        # If verbose is set then give more (useful) context:
        print(f"[-] USER: {user.decode('utf-16le')}")
        print(f"[-] DOMAIN: {domain.decode('utf-16le')}")
        print(f"[-] PASSWORD HASH: {password_hash.hex()}")
        print(f"[-] RESPONSE NT KEY: {response_nt_key.hex()}")
        print(f"[-]NT PROOF STR: {nt_proof_str.hex()}")
        print(f"KEY EXCHANGE KEY: {key_exchange_key.hex()}")

    # Print out what we came for...
    print(f"[+] RANDOM SESSION KEY is: {random_session_key.hex()}")

if __name__ == "__main__":
    main()