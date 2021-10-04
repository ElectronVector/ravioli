def strip_comments(code):
    # Remove comments that start with "//" all the way to the end of the line.
    code_lines = code.splitlines(True)
    lines_with_no_comments = [line if not ("//" in line) else (line[:line.index("//")] + "\n") for line in code_lines]
    code = "".join(lines_with_no_comments)

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
