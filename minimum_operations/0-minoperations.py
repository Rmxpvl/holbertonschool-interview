#!/usr/bin/python3
"""Calculate the minimum operations to reach n H characters."""


def minOperations(n):
    """Return the fewest Copy All and Paste operations needed."""
    if n < 2:
        return 0

    operations = 0
    divisor = 2

    while divisor * divisor <= n:
        while n % divisor == 0:
            operations += divisor
            n //= divisor
        divisor += 1

    if n > 1:
        operations += n

    return operations
