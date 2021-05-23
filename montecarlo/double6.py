#!/usr/bin/env python
"""
this is to test a theory by ?? (pascal?) about the expected value of
betting that you'll roll a double 6 in <= 24 rolls of 2d6
"""
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
