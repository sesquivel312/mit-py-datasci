#!/bin/env python
"""
using to test out lib functions, etc.
"""
from mycode.lib.lib import craps_sim

nhands = 10000
stats = craps_sim(nhands)

for k,v in stats.items():
    stats[k] = v/nhands

print(stats)
