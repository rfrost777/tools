#!/usr/bin/env python3
########################################################
# date_gen.py -
# generates a custom wordlist of format YYYYMMDD
# I needed for a CTF challenge.
#
# TODO: make more customizable using command line arguments?
########################################################


def main() -> None:
    year: int = 2020
    for month in range(10, 13):
        for day in range(1, 32):
            print(f"{year}{month:0>2}{day:0>2}")


if __name__ == '__main__':
    main()
