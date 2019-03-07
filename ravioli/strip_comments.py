def strip_comments(code):
    # Remove single line comments.
    code_lines = code.splitlines(True)
    non_comment_lines = [line for line in code_lines if not line.lstrip().startswith("//")]
    code = "".join(non_comment_lines)
    # Remove block comments
    stripped = ""
    in_comment = False
    for i, c in enumerate(code):
        if i < (len(code) - 1):
            # Only check if there are enough characters left.
            if code[i] == '/' and code[i + 1] == '*':
                in_comment = True
        if not in_comment:
            stripped += code[i]
        elif code[i - 1] == '*' and code[i] == '/':
            in_comment = False
    return stripped
