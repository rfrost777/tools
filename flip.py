#!/usr/bin/env python3
##########################################################
# THM - Flip (https://tryhackme.com/room/flip)
#
# A CTF Challenge involving an attack on AES-CBC
# encryption by intelligently using a bit flip.
#
##########################################################
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify
from pwn import *
import re

# EDIT this to point at your target address once you pressed "Start Machine"
target_ip: str = '10.10.96.249'

# I copied encrypt_data() and decrypt_data() from the "leaked" app sourcecode
# in the downloadable challenge files:


def encrypt_data(unencrypted_params: str, enc_key: bytes, i_vector: bytes) -> str:
    padded = pad(unencrypted_params.encode(),16,style='pkcs7')
    cipher = AES.new(enc_key, AES.MODE_CBC, i_vector)
    enc = cipher.encrypt(padded)
    return enc.hex()


def decrypt_data(encrypted_params: str, enc_key: bytes, i_vector: bytes) -> int:
    cipher = AES.new(enc_key, AES.MODE_CBC, i_vector)
    padded_params = cipher.decrypt(unhexlify(encrypted_params))
    print(padded_params)
    if b'admin&password=sUp3rPaSs1' in unpad(padded_params,16,style='pkcs7'):
        return 1
    else:
        return 0


def main() -> None:
    # Generate a key and an initialization vector for AES
    key: bytes = get_random_bytes(16)
    iv: bytes = get_random_bytes(16)

    # Let's do a PoC locally...
    # Flip one "s" in password to "r"
    user: str = 'admin&parsword=sUp3rPaSs1'
    password: str = 'sUp3rPaSs1'
    msg: str = 'logged_username=' + user +'&password=' + password
    print(msg, len(msg))

    xor: int = ord('r') ^ ord('s')
    cipher = encrypt_data(msg, key, iv)
    # Correct the cipher on the correct position:
    cipher = cipher[:16] + hex(int(cipher[16:18], 16) ^ xor)[2:] + cipher[18:]
    # Now this should return "1":
    print(decrypt_data(cipher, key, iv))

    # Let's connect to the THM remote machine
    # and weaponize our PoC code with pwntools:
    conn = remote(target_ip, 1337)

    print(conn.recv().decode())
    print(conn.recv().decode())

    # Send the tampered payload:
    conn.send(b'admin&parsword=sUp3rPaSs1\r\n')
    print(conn.recv().decode())
    conn.send(b'\r\n')

    match = re.match(r'Leaked ciphertext: (.+)\n', conn.recv().decode())
    print('[*] Ciphertext:', match[1])

    # Correct the leaked cipher to read "admin&password=sUp3rPaSs1" again...
    cipher = match[1]
    cipher = cipher[:16] + hex(int(cipher[16:18], 16) ^ xor)[2:] + cipher[18:]
    print('[*] Modified Ciphertext:', cipher)
    # ... and send it back to the server.
    conn.send(cipher.encode() + b'\r\n')
    # Hopefully collect our flag from the server, then close the connection:
    print(conn.recv().decode())
    conn.close()


if __name__ == '__main__':
    main()
