#!/usr/bin/env python3

def canUnlockAll(boxes):
    n = len(boxes)
    opened = set([0])   # boîte 0 déjà ouverte
    keys = set(boxes[0])  # clés disponibles au départ

    while keys:
        key = keys.pop()

        if key < n and key not in opened:
            opened.add(key)
            keys.update(boxes[key])

    return len(opened) == n
