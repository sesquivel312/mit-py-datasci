#!/bin/env python
"""
this is used for finding solutions to a knapsack problem - i.e. how can I maximize
the value of the food items I eat in a meal while fitting them into a calorie budget.

Value = how much I like a given food item

The calorie budget is the size of the knapsack in this case

I've implemented this version of the code from the course resources
myself.  The only real difference is that I used the property builtin
for creating class properties, rather than simply coding methods.  This
allows the properties to be referenced using "dot notation", e.g.
Food1.cost
"""

from pprint import pprint as pp


class Food(object):
    def __init__(self, name, preference, calories):
        """

        :param name: name of the food
        :type name: str
        :param preference: how much I prefer this item, 0-100
        :type preference: int
        :param calories: calories in one serving of this food item
        :type calories: int
        """

        self._name = name
        self._preference = preference
        self._calories = calories

    @property
    def preference(self):
        return self._preference

    @preference.setter
    def preference(self, v):
        self._preference = v

    @property
    def calories(self):
        return self._calories

    @calories.setter
    def calories(self, v):
        self._calories = v

    @property
    def cost(self):
        return self._calories

    @property
    def value(self):
        return self._preference

    @property
    def density(self):
        return self.preference / self.cost

    def __repr__(self):
        return f'{self._name}: pref:{self._preference} cal: {self._calories}'


def build_menu(items, preferences, calories):
    """
    construct a menu of food items given each ones various properties in separate lists

    Notes:
        The lists must be compatibly ordered, i.e. first food item properties in each list and so on

    :param items: list of food item names, e.g. pizza
    :type items: list(str)
    :param preferences: list indicating how much the eater likes each food item in the list on a scale of 0-100
    :type preferences: list(int)
    :param calories: list of integers indicating the calories contained in each food item in the list
    :type calories: list(int)
    :return: list of instances of Food class
    :rtype: list(Food)
    """

    if not (len(items) == len(preferences) == len(calories)):
        raise RuntimeError('The lengths of the items, preferences, and calories lists were not equal')

    return [Food(items[i], preferences[i], calories[i]) for i in range(len(items))]


def greedy(items, max_cost, cost_func):
    """
    apply a greedy algo to put the "best" items "into the knapsack" (take/include them)

    best is defined by the cost function, which is passed to sorted

    sorted returns the list from smallest to largest, we need it reversed - i.e.
    we want the "most best" item first, then the next, and so on

    Notes:
        When using the property built-in/decorator, the properties themselves are not
        callable, but they contain callable items, e.g. fget, fset (need to look up
        the names of the items that property() generates).  Be aware of this when
        trying to pass properties, you'll probably have to pass something like:

          object.propname.fget

    :param items: list of items to choose from
    :param max_cost: budget constraint - how much can we spend (in this case in calories)
    :param cost_func: how do we order items - this could be based on anything, and doesn't have to be the "cost"
    :return: the items we took and the total value for those items (value = how much we like these things)
    """

    # get a sorted copy of the items list (i.e. don't muck w/the list directly)
    _items = sorted(items, key=cost_func, reverse=True)

    taken = []
    accumulated_value, accumulated_cost = 0.0, 0.0

    for i in range(len(_items)):

        t = _items[i]  # a bit less repeated typing below

        if (accumulated_cost + t.cost) <= max_cost:  # adding this item doesn't exceed the allowed budget

            taken.append(t)  # record that we took this item
            accumulated_cost += t.cost  # track the constraint budget
            accumulated_value += t.value  # see how much we prefer all the items we took

    return taken, accumulated_value


def run_greedy(items, max_cost, cost_func):
    """
    run the greed algo with the given cost function

    Also display results of this run to the user

    :param items:
    :param max_cost:
    :param cost_func:
    :return:
    """
    taken, val = greedy(items, max_cost, cost_func)

    print(f'Value of items taken: {val}')

    for t in taken:
        print(' ' * 2, t)

    print('\n\n-------------')


def run_greedys(foods, max_units):
    """
    this function runs the run_greedy function with a few different cost functions

    :param foods:
    :param max_units:
    :return:
    """

    print(f'Use greedy by value/pref to allocate {max_units} calories')
    run_greedy(foods, max_units, Food.value.fget)  # best is defined by preference value

    print(f'Use greedy by cost to allocate {max_units} calories')
    run_greedy(foods, max_units, lambda v: 1 / Food.cost.fget(v))  # best is defined by lowest calorie (aka cost) item, hence the inversion

    print(f'Use greedy by density to allocate {max_units} calories')
    run_greedy(foods, max_units, Food.density.fget)  # best is value/calories ratio (aka density)


def maximize(remaining_items, remaining_budget):
    """
    this function uses a tree traversal to brute force the answer - in theory it would
    find every possible solution - i.e. the power set, but it includes code to
    throw out options that would exceed the constraint - i.e. it doesn't traverse
    a branch that would do so.

    :param remaining_items: list of items not yet considered for inclusion - i.e. put into knapsack
    :param remaining_budget: how much of the initial cost budget remains
    :return:
    """

    if not (remaining_items and remaining_budget):  # if no items left or no budget left
        result = (0, ())
        print(f'remaining budget: {remaining_budget} or items: {remaining_items} are 0/empty')

    elif remaining_items[0].cost > remaining_budget:  # can't take the next item, following the right branch - i.e. drop the "current" item, then recurse with what's left
        print(f'The next item: {remaining_items[0]} cost more than the remaining budget: {remaining_items[0].cost} > {remaining_budget}')
        result = maximize(remaining_items[1:], remaining_budget)

    else:  # take the next item, following the left branch

        # save a bit of typing, but perhaps it's just extra work? todo add timers with/without this typing saver code
        nxt = remaining_items[0]  # the next item up for consideration
        remainder = remaining_items[1:]  # the list of items remaining to consider after this run, slice to get copy rather than pop (changes list in place)

        # print(f'take or leave? assume take then calling again with reduced budget: {remainder}, {remaining_budget - nxt.cost}')
        take_value, items_after_take = maximize(remainder, remaining_budget - nxt.cost)  # get the updated value if item is taken > recurse w/reduced budget
        take_value += nxt.value  # the current value/preference of items taken so far

        # print(f'take or leave? assume leave then calling again with same budget: {remainder}, {remaining_budget}')
        leave_value, items_after_leave = maximize(remainder, remaining_budget)  # get the updated value if item is left > recurse w/same budget

        if take_value > leave_value:  # if the accumulated value > when current item is taken, update the result with the new take value and the updated list of items taken
            # print(f'Take increased the value setting result to: {take_value}, {items_after_take + (nxt, )}')
            result = (take_value, items_after_take + (nxt,))

        else:  # otherwise update by leaving it out
            # print(f'Take did NOT inc value, setting result to: {leave_value, items_after_leave}')
            result = (leave_value, items_after_leave)

    # print(f'About to return result: {result}')
    return result


def run_maximize(food_list, cost_budget, show=True):

    print(f'Use search tree to allocate {cost_budget} calories')

    value, kept = maximize(food_list, cost_budget)

    print(f'Value of items taken is {value}')

    if show:
        for k in kept:
            print(' '*4, k)

if __name__ == '__main__':

    names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut']
    values = [89, 90, 95, 100, 90, 79, 50, 10]
    calories = [123, 154, 258, 354, 365, 150, 95, 195]

    menu = build_menu(names, values, calories)

    run_greedys(menu, 750)
    run_maximize(menu, 750)
