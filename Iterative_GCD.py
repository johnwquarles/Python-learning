"""Iterative greatest common denominator finder"""

def gcdIter(a, b):
    small = min(a,b)
    large = max(a,b)
    divisor = small
    while True:
        if large % divisor == 0 and small % divisor == 0:
            return divisor
            break
        else:
            divisor = divisor - 1
