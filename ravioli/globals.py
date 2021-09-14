


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
    if tokens[0].isalpha() and tokens[1].isalpha():
        # This is a declaration. Extract the second token.
        return tokens[1]


def extract_usages_from_statement(statement):
    usages = []
    if "=" in statement:
        # Usage must be directly to the left of the = or after the equal
        tokens = statement.split()
        eq_index = tokens.index('=')
        usages.append(tokens[eq_index - 1])
        usages += [t for t in tokens[eq_index:] if t.isalpha()]
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