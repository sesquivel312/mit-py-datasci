import math
import random
from typing import Tuple, List

random.seed(0)


class Location:

    def __init__(self, start: Tuple[int, int]):
        """
        start is a tuple representing the starting x, y location of a thing

        :param start: tuple (int or float)
        """
        self._loc = start  # loc is the property defined below

    def move(self, dx, dy):
        """
        return a new loc instance moved by dx, dy from the current location, b/c
        if not then this location will likely end up used in unexpected ways -
        e.g. when calculating a distance after several moves - you'll have the
        same point as the start and end b/c you updated the  same object

        :param dx:
        :param dy:
        :return:
        """

        # new = (self.loc[0] + dx, self.loc[1] + dy)

        return Location((self.loc[0] + dx, self.loc[1] + dy))

    @property
    def loc(self) -> 'Location':
        return self._loc  # use _ (underscore) b/c already using name 'loc' for the property itself, which == method name

    @loc.setter
    def loc(self, point: Tuple[int, int]):
        self._loc = point

    def distance_to(self, other):
        l = other.loc
        d = math.sqrt((self._loc[0] - l[0]) ** 2 + (self._loc[1] - l[1]) ** 2)
        return d

    def __str__(self):
        return f'({self.loc[0]}, {self.loc[1]})'


class Drunk(object):
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        if self.name is not None:
            return self.name
        return 'anonymous'


class UsualDrunk(Drunk):
    """


    Notes:

    """

    @staticmethod
    def step():
        """
        move some amount in x & y, chosen randomly from a set of options
        in this case it's step L, R, Up or Down by 1 unit
        """

        choices = [
            (0,  1),
            (0, -1),
            (1,  0),
            (-1, 0)
        ]
        return random.choice(choices)


class ArcticDrunk(Drunk):
    @staticmethod
    def step():
        """
        biased northward
        :return:
        """
        choices = [
            (0, 1.1),  # moves >1 when moving "north"
            (0, -0.9),  # moves <1 when moving "south"
            (1, 0),
            (-1, 0)
        ]
        return random.choice(choices)


class Field:
    """
    maps drunks to locations, moves them, ???

    this is effectively a wrapper around a mapping of drunk: location

    """

    def __init__(self):
        self.drunks = {}

    def add_drunk(self, drunk: Drunk, loc: Location):

        # check for dup before adding
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        self.drunks[drunk] = loc  # todo confirm if prevents this when if is matched; this is a Location

    def get_location(self, drunk):
        if drunk not in self.drunks:  # todo convert to use .get() and check for None?? or factor existence check out
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]  # the location of drunk in the field

    def move(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')

        dx, dy = drunk.step()

        # move returns a location, set the given drunks location to that new location
        self.drunks[drunk] = self.drunks[drunk].move(dx, dy)


def walk(field: Field, drunk: Drunk, num_steps: int) -> float:
    """
    walk - given a field and a Drunk, and a number of steps, take a random
    walk - i.e. move the drunk #steps times in a random direction - using
    the drunk's step method

    :param field:
    :param drunk:
    :param num_steps:
    :return:
    """

    start = field.get_location(drunk)

    for s in range(num_steps):
        field.move(drunk)

    end = field.get_location(drunk)

    return end, start.distance_to(end)


def walks(steps_per_walk: int, num_walks: int, drunk_type: str) -> List[float]:
    """
    run multiple walks of a given length for a given drunk type.  Keep track of
    and return the distance moved (from start) to last position of each (in a
    list)

    run a steps_per_walk length walk for the given drunk num_walks times,
    returning the distance from the origin for each walk in a list

    :param steps_per_walk: number of steps to take per walk - same for all walks
    :param num_walks: how many walks of a given length to generate
    :param drunk: drunk type
    :return: list of the distances from the start position for ea walk taken
    """

    # drunk = DrunkType(Drunk)  # create instance of DrunkType
    drunk = globals()[drunk_type](drunk_type)  # create instance of DrunkType
    origin = Location((0, 0))
    walk_distances = []
    final_positions = []

    for w in range(num_walks):

        f = Field()
        f.add_drunk(drunk, origin)

        p, d = walk(f, drunk, steps_per_walk)
        final_positions.append(p)
        walk_distances.append(d)

    return final_positions, walk_distances


def sim_walks(walk_lengths: List[int], nwalks: int, DrunkType) -> dict:
    """
    run a number of walks of varying length for a given drunk type.  Run ea
    such walk nwalks times.

    Notes:
        Ea walk (called by this function) will generate a list of length
        nwalks, therefore there will be nwalks * len(walk_lengths) datapoints
        generated

        return dict format is:
            walk_len: {'min': n, 'max': x, 'mean': u}, ... ; n,x,u are floats

    :param walk_lengths: the list of different walk lengths to simulate
    :param nwalks:  the number of times to run a walk of a given length
    :param DrunkType: type of drunk - which determines how it moves
    :return: None
    """

    d = []  # list receiving walk results, maps to walk_lengths argument

    for length in walk_lengths:

        final_positions, distances = walks(length, nwalks, DrunkType)
        mean = round(sum(distances)/len(distances), 3)
        minn = min(distances)  # minn, maxx b/c collision w/built-in functions
        maxx = max(distances)

        # print(f'{DrunkType.__name__} walk of {length} steps')
        # print(f'mean: {mean}, min: {minn}, max: {maxx}')
        # print('*' * 10 + '\n')

        d.append({'min': minn, 'max': maxx, 'mean': mean, 'positions': final_positions})

    return d

