"""
This is intended to take a stab at creating a set of functions, etc.
to be used across the various problems in this course
"""
import random


def roll_die(sides: int) -> int:
    return random.choice(range(1, sides + 1))


def d6() -> int:
    return roll_die(6)

