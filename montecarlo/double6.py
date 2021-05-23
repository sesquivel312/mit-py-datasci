#!/usr/bin/env python
from mycode.lib.lib import d6


t = 100000
w = 0
for i in range(t):
    for j in range(24):
        d1 = d6()
        d2 = d6()

        if d1 == d2 == 6:
            w += 1
            break

print(f'Win probability: {w/t}')

# todo simulate craps game (from the book p458)

