#!/usr/bin/python3
"""Pascal's triangle module."""


def pascal_triangle(n):
    """Return a list of lists representing Pascal's triangle of size n.

    Args:
        n (int): Number of rows.

    Returns:
        list[list[int]]: Pascal's triangle rows, or [] if n <= 0.
    """
    if n <= 0:
        return []

    triangle = [[1]]
    for row_index in range(1, n):
        previous_row = triangle[row_index - 1]
        row = [1]

        for col_index in range(1, row_index):
            row.append(previous_row[col_index - 1] + previous_row[col_index])

        row.append(1)
        triangle.append(row)

    return triangle
