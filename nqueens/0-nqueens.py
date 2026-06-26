#!/usr/bin/python3
import sys


def solve(n, row, cols, diag1, diag2, placement):
    if row == n:
        print(placement)
        return
    for col in range(n):
        if col in cols or (row - col) in diag1 or (row + col) in diag2:
            continue
        cols.add(col)
        diag1.add(row - col)
        diag2.add(row + col)
        placement.append([row, col])
        solve(n, row + 1, cols, diag1, diag2, placement)
        placement.pop()
        cols.remove(col)
        diag1.remove(row - col)
        diag2.remove(row + col)


if len(sys.argv) != 2:
    print("Usage: nqueens N")
    sys.exit(1)

try:
    n = int(sys.argv[1])
except ValueError:
    print("N must be a number")
    sys.exit(1)

if n < 4:
    print("N must be at least 4")
    sys.exit(1)

solve(n, 0, set(), set(), set(), [])
