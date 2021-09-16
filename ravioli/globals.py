


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


def extract_declarations_from_statement(statement):
    # Ensure that there is whitespace around all commas.
    statement = statement.replace(",", " , ")
    # Split the statement into tokens by spaces.
    tokens = statement.split()
    print(tokens)
    decl = None
    declarations = []
    on_right_side_of_equals = False
    # Iterate over the list, looking for two or more identifiers next to each other from the start.
    for i, t in enumerate(tokens):
        if t == ",":
            # A comma indicates the end of a declaration and that their will be another. Save this one and don't stop
            # yet.
            if decl:
                declarations.append(decl)
                decl = None

            # Once we get to a comma, we are back on the left side of the equals sign.
            on_right_side_of_equals = False
        elif t == "=":
            # We can't find an assignment on the right side of an equals sign.
            on_right_side_of_equals = True
        elif i > 0 and is_valid_identifier(t) and not on_right_side_of_equals:
            # Save the last valid identifier because this is going to be the declaration.
            decl = t

    if decl:
        declarations.append(decl)

    if declarations:
        return declarations


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
        new_declarations = extract_declarations_from_statement(s)
        if new_declarations:
            declarations += new_declarations
        new_usages = extract_usages_from_statement(s)
        if new_usages:
            usages += new_usages

    print(f"usages: {usages}")
    print(f"declarations: {declarations}")
    return [u for u in usages if u not in declarations]