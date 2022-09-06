def strip_comments(code):
    # Remove single line comments.
    code_lines = code.splitlines(True)
    non_comment_lines = list()
    for line in code_lines:
        if not "//" in line:
            non_comment_lines.append(line)
        elif not line.lstrip().startswith("//"):
            comment_start = line.index("//")
            non_comment_lines.append(line[0:comment_start]+"\n")
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
