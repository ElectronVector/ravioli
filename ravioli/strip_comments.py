import re


def strip_comments(code):
    # Remove block comments
    code = re.sub(r'/\*.*\*/', '', code, flags=re.DOTALL)
    # Remove single line comments.
    code_lines = code.splitlines(True)
    non_comment_lines = [line for line in code_lines if not line.lstrip().startswith("//")]
    return "".join(non_comment_lines)