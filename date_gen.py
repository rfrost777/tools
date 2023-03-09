#!/usr/bin/env python3
year = 2020
for month in range(10, 13):
    for day in range(1, 32):
        print(f"{year}{month:0>2}{day:0>2}")
