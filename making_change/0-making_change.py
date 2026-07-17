#!/usr/bin/python3
"""Determine the fewest number of coins needed to meet a given total."""


def makeChange(coins, total):
    """Return the fewest coins from coins that sum to total, or -1."""
    if total <= 0:
        return 0

    fewest = [0] + [float('inf')] * total

    for amount in range(1, total + 1):
        for coin in coins:
            if coin <= amount and fewest[amount - coin] + 1 < fewest[amount]:
                fewest[amount] = fewest[amount - coin] + 1

    return fewest[total] if fewest[total] != float('inf') else -1
