import re


def count(string):
    # Remove all block comments.
    string = re.sub(r'/\*.*\*/', '', string, flags=re.DOTALL)
    lines = string.splitlines()
    # Remove lines containing only whitespace.
    lines = [l for l in lines if not l.isspace()]
    # Remove comment lines.
    lines = [l for l in lines if not l.lstrip().startswith("//")]
    # Remove blank lines.
    lines = [l for l in lines if len(l) > 0]
    return len(lines)


def count_file(filename):
    with open(filename, 'r') as f:
        line_count = count(f.read())
    return line_count
