


def extract_statements(code):
    statements = []
    current_statement = ""
    for c in code:
        if c == ";":
            # Save the current statement.
            statements.append(clean_up_whitespace(current_statement))
            current_statement = ""
        else:
            current_statement += c

    return statements


def clean_up_whitespace(s):
    return " ".join(s.strip().split())


def extract_definitions_from_statement(statement):
    tokens = statement.split()
    if is_valid_identifier(tokens[0]) and is_valid_identifier(tokens[1]):
        # This is a declaration. Extract the second token.
        return tokens[1]


def is_valid_identifier(s):
    """
    Determine if this string is a valid c variable name.
    """
    # The first character must be a letter or underscore.
    if s[0].isdigit():
        return False
    for c in s:
        if not (c == "_" or c.isalpha() or c.isdigit()):
            return False

    return True


def extract_usages_from_statement(statement):
    usages = []
    if "=" in statement:
        # Usage must be directly to the left of the = or after the equal
        tokens = statement.split()
        eq_index = tokens.index('=')
        usages.append(tokens[eq_index - 1])
        usages += [t for t in tokens[eq_index:] if is_valid_identifier(t)]
    return usages


def extract_undefined_usages(code):
    statements = extract_statements(code)
    declarations = []
    usages = []
    for s in statements:
        new_declarations = extract_definitions_from_statement(s)
        if new_declarations:
            declarations += new_declarations
        new_usages = extract_usages_from_statement(s)
        if new_usages:
            usages += new_usages

    print(f"usages: {usages}")
    print(f"declarations: {declarations}")
    return [u for u in usages if u not in declarations]