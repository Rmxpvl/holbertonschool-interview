#!/usr/bin/python3
"""Log parsing script."""

import sys
import re


status_codes = [200, 301, 400, 401, 403, 404, 405, 500]
counts = {code: 0 for code in status_codes}
file_size = 0
line_count = 0
pattern = re.compile(
    r'^\d+\.\d+\.\d+\.\d+ - \[[^\]]+\] "GET /projects/\d+ HTTP/1\.1" (\d{3}) (\d+)$'
)


def print_stats():
    """Print accumulated log statistics."""
    print("File size: {}".format(file_size))
    for code in status_codes:
        if counts[code]:
            print("{}: {}".format(code, counts[code]))


if __name__ == "__main__":
    try:
        for raw_line in sys.stdin:
            line_count += 1
            match = pattern.match(raw_line.rstrip("\n"))
            if match:
                status = int(match.group(1))
                size = int(match.group(2))
                file_size += size
                if status in counts:
                    counts[status] += 1
            if line_count % 10 == 0:
                print_stats()
        if line_count == 0 or line_count % 10 != 0:
            print_stats()
    except KeyboardInterrupt:
        print_stats()
        raise
