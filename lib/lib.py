"""
This is intended to take a stab at creating a set of functions, etc.
to be used across the various problems in this course
"""
import operator
import random
from enum import auto, Enum
from functools import reduce
from typing import List, Tuple, Mapping


def roll_die(sides: int) -> int:
    return random.choice(range(1, sides + 1))


def d6() -> int:
    return roll_die(6)


def nd6(n: int) -> List:
    return [d6() for i in range(n)]


class Bet(Enum):
    PASS = auto()
    DONT_PASS = auto()


class COutcome(Enum):
    WIN = auto()
    LOSE = auto()
    PUSH = auto()


def craps_hand() -> COutcome:
    """
    Play a simplified game of craps.  Given a bet of "pass" (default) or "dontpass" and
    a dice rolling function (roll 2d6 by default) return an indication of win/loss as a tuple for
    each bet type (pass, don't pass)

    todo add summary stats as in book
    todo generalize to an arbitrary roller function & number of rolls (closure?)
    """

    r = nd6(2)  # list of results of roll for each die
    p = reduce(operator.add, r)  # get the total or point

    if p in [7, 11]:
        return COutcome.WIN, COutcome.LOSE  # pass wins, don't pass loses

    if p in [2, 3]:
        return COutcome.LOSE, COutcome.WIN  # pass loses, don't pass wins

    if p == 12:
        return COutcome.PUSH, COutcome.PUSH

    while True:
        r = nd6(2)
        t = reduce(operator.add, r)

        if t == p:
            return COutcome.WIN, COutcome.LOSE
        if t == 7:
            return COutcome.LOSE, COutcome.WIN


def craps_sim(nhands: int) -> Mapping[str, int]:
    """
    run a number of craps hands, returning the wins for each outcome type: pass win, don't pass win, push

    todo update w/groups, i.e. hands/sim, #sims, stats are per sim

    Args:
        nhands:

    Returns:

    """

    stats = {
        'pass': 0,
        'dpass': 0,
        'push': 0
    }

    result = {
        COutcome.WIN: 'pass',
        COutcome.LOSE: 'dpass',
        COutcome.PUSH: 'push'
    }

    for i in range(nhands):

        outcome, _ = craps_hand()  # return outcome enum value todo verify only need pass value b/c implies dpass
        stats[result[outcome]] += 1  # use the outcome to lookup and increment the corresponding value in the stats dict

    return stats
