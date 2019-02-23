import re

from ravioli.strip_comments import strip_comments


def count(string):
    string = strip_comments(string)
    lines = string.splitlines()
    # Remove lines containing only whitespace.
    lines = [l for l in lines if not l.isspace()]
    # Remove blank lines.
    lines = [l for l in lines if len(l) > 0]
    return len(lines)


def count_file(filename):
    with open(filename, 'r') as f:
        line_count = count(f.read())
    return line_count
