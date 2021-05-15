#!/usr/bin/env python3


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def memfib(n, m={}):

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        if m.get(n):
            return m.get(n)
        else:
            r = memfib(n-1, m) + memfib(n-2, m)
            m[n] = r
            return r


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('n', help='number to cal fib for')

    args = parser.parse_args()

    print('running memo')
    print(f'    {memfib(int(args.n))}')
    print('running std')
    print(f'    {fib(int(args.n))}')
