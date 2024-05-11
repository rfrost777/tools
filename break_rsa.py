#!/usr/bin/env python3
#######################################################
# Breaking (weak) RSA implementations
# Room: https://tryhackme.com/room/breakrsa
#
#######################################################

# python3-gmpy2 is a C-coded Python extension module that supports
# multiple-precision arithmetic:
from gmpy2 import isqrt
from math import lcm
from Crypto.PublicKey import RSA
import os
from typing import Any

# Path to the given, weak public RSA key:
file_path: str = '~/id_rsa.pub'


# Helper function to find the Greatest Common Divisor (GCD)
# using the Euclidean Algorithm:
def euclidean_gcd(a: Any, b: Any) -> tuple[Any, Any, Any]:
    if a == 0:
        return b, 0, 1
    g, y, x = euclidean_gcd(b % a, a)
    return g, x - (b//a) * y, y


# Think of this like a division of sorts, but for modular arithmetic ;-)...
def modular_inverse(a: Any, m: Any) -> Any:
    g, x, y = euclidean_gcd(a, m)
    if g != 1:
        raise Exception('Uh-ohh! There is no modular inverse!')
    return x % m


# Python implementation of the original algorithm
# found by Pierre de Fermat (1606-1665)
# Time complexity should be roughly: O(sqrt(n))
def fermat_factorize(n: Any) -> tuple[Any, Any]:
    # First check if n is even. Since even numbers are per definitionem divisible by 2, one of the factors will
    # always be 2!
    if (n & 1) == 0:
        return n/2, 2

    # Calculate the integer square root of n
    a = isqrt(n)

    # Low-hanging fruit: If n is a perfect square (n = a^2) the factors will be ( sqrt(n), sqrt(n) )
    if a * a == n:
        return a, a

    while True:
        # Okay, no more shortcuts, let's get to work:
        a = a + 1
        bsq = a * a - n
        b = isqrt(bsq)
        if b * b == bsq:
            break

    return a + b, a - b


def main() -> None:
    # Load our given, weak public key:
    key: bytes
    with open(os.path.expanduser(file_path), 'rb') as public_key_file:
        key = public_key_file.read()
    print(f'\nLoaded {file_path} for {len(key)} bytes of content!\n')
    # ...and let the PyCryptodome.rsa object take care of the key implementation specifics:
    rsa_key = RSA.importKey(key)

    print(f'Given e in public key: {rsa_key.e}\n')
    print(f'Size (complexity) of the key in bits: {rsa_key.size_in_bits()}\n')

    (p, q) = (fermat_factorize(rsa_key.n))

    print(f'Numerical difference between p and q: {abs(p - q)}\n')
    print(f'Prime factor p:\n{p}\n\n')
    print(f'Prime factor q:\n{q}\n\n')
    print(f'Given n was:\n{rsa_key.n}\n\n')

    # RSA default for e is 65537,
    # calculate the private exponent d:
    d = modular_inverse(rsa_key.e, lcm(p - 1, q - 1))

    print(f'Private exponent d is:\n{d}')


if __name__ == '__main__':
    main()
