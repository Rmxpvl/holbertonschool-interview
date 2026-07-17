#!/usr/bin/python3
"""Determine who wins the most rounds of the Prime Game."""


def isWinner(x, nums):
    """Return the name of the player who won the most rounds, or None."""
    if not nums or x == 0:
        return None

    max_n = max(nums)
    sieve = [True] * (max_n + 1)
    for i in (0, 1):
        if i <= max_n:
            sieve[i] = False

    for i in range(2, int(max_n ** 0.5) + 1):
        if sieve[i]:
            for multiple in range(i * i, max_n + 1, i):
                sieve[multiple] = False

    primes_up_to = [0] * (max_n + 1)
    count = 0
    for i in range(max_n + 1):
        if sieve[i]:
            count += 1
        primes_up_to[i] = count

    maria_wins = 0
    ben_wins = 0
    for n in nums:
        primes = primes_up_to[n] if n >= 0 else 0
        if primes % 2 == 1:
            maria_wins += 1
        else:
            ben_wins += 1

    if maria_wins > ben_wins:
        return "Maria"
    if ben_wins > maria_wins:
        return "Ben"
    return None
