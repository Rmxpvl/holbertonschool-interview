#!/usr/bin/python3
"""Lockboxes module

This module exposes a single function `canUnlockAll(boxes)` which returns
True if all boxes can be opened starting from box 0 using the keys found
inside the boxes. The function performs a graph traversal (DFS/BFS style)
to explore reachable boxes and ignores invalid keys.
"""

def canUnlockAll(boxes):
    """Return True if all boxes can be opened starting from box 0."""
    n = len(boxes)
    if n == 0:
        return True

    opened = set([0])   # boîte 0 déjà ouverte
    # clés disponibles au départ (protéger contre index error)
    keys = set(boxes[0]) if boxes and boxes[0] else set()

    while keys:
        key = keys.pop()

        if isinstance(key, int) and 0 <= key < n and key not in opened:
            opened.add(key)
            keys.update(boxes[key])

    return len(opened) == n
