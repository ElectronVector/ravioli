


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


def extract_undefined_usages(code):
    statements = extract_statements(code)
    declarations = []
    usages = []
    for s in statements:
        new_declarations = extract_definitions_from_statement(s)
        if new_declarations:
            declarations += new_declarations
        else:
            usages += [t for t in s.split() if t.isalpha()]

    print(usages)
    print(declarations)
    return [u for u in usages if u not in declarations]