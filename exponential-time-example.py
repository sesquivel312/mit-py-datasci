#!/usr/bin/env python

"""
This is code from the book associated w/the course - it's from the chapter on
complexity (i.e. BigOh notation, etc.).  This example generates a power set
from a string of unique characters, the runnable part calls the function that
builds the power set and prints the resulting length of that "set" (coded as
a list of lists here).  The idea is to see how the time increases as the
length of the input string increases (it's exponential)
"""

import argparse
from pprint import pprint as pp

p = argparse.ArgumentParser()
p.add_argument('--string', help='enter a string of unique characters, will consider it a set and produce the power sets')
args = p.parse_args()

def get_binary_rep(n, num_digits):
   """Assumes n and numDigits are non-negative ints
      Returns a str of length numDigits that is a binary
      representation of n"""
   result = ''
   while n > 0:
      result = str(n%2) + result
      n = n//2
   if len(result) > num_digits:
      raise ValueError('not enough digits')
   for i in range(num_digits - len(result)):
      result = '0' + result
   return result

def gen_powerset(L):
   """Assumes L is a list
      Returns a list of lists that contains all possible
      combinations of the elements of L. E.g., if
      L is [1, 2] it will return a list with elements
      [], [1], [2], and [1,2]."""
   powerset = []
   for i in range(0, 2**len(L)):
      bin_str = get_binary_rep(i, len(L))
      subset = []
      for j in range(len(L)):
         if bin_str[j] == '1':
            subset.append(L[j])
      powerset.append(subset)
   return powerset

if __name__ == '__main__':

   pp(len(gen_powerset(args.string)))

