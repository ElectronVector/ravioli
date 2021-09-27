from ravioli.extract_statements import extract_statements


def extract_declarations(text):
    """
    Find all declarations of new variables in the current text.
    :param text: A bit of C code that ends with a semi-colon.
    :return: An array of variable names declared in the text.
    """
    # Ensure that there is whitespace around all commas.
    text = add_spaces_around_punctuation(text)
    # Split the text into tokens by spaces.
    tokens = text.split()
    declarations = []

    type_found = None
    potential_declaration = []
    on_right_side_of_equals = False
    # Iterate over the list, looking for two or more identifiers next to each other from the start, commas that
    # separate compound identifiers or equals signs, were we can't have identifiers after them.
    for i, t in enumerate(tokens):
        if t == ",":
            # A comma potentially ends a declaration.
            # A declaration should be saved if 1) there are at least two consecutive valid identifiers or 2) we
            # previously found two consecutive identifiers and this is another declaration after a comma.
            if (type_found or (len(potential_declaration) >= 2)) and potential_declaration:
                declarations.append(potential_declaration[-1])
                type_found = True
            # After a comma we need to start a new potential declaration.
            potential_declaration = []
            # Once we get to a comma, we are back on the left side of the equals sign.
            on_right_side_of_equals = False
        elif t == "=":
            # We can't find an assignment on the right side of an equals sign.
            on_right_side_of_equals = True
        elif is_valid_identifier(t) and not on_right_side_of_equals:
            # Save all the valid consecutive identifier so that we can eventually save the last one.
            potential_declaration.append(t)

    if potential_declaration:
        # A declaration should be saved if 1) there are at least two consecutive valid identifiers or 2) we previously
        # found two consecutive identifiers and this is another declaration after a comma.
        if type_found or (len(potential_declaration) >= 2):
            declarations.append(potential_declaration[-1])

    return declarations


def is_valid_identifier(s):
    """
    Determine if this string is a valid C language variable name.
    """
    # The first character must be a letter or underscore.
    if s[0].isdigit():
        return False
    for c in s:
        if not (c == "_" or c.isalpha() or c.isdigit()):
            return False

    return True


def add_spaces_around_punctuation(s):
    punctuation = ['+', '-', '*', '/', '=', '(', ')', ',']
    return ''.join(map(lambda c: f" {c} " if c in punctuation else c, s))


def extract_usages(text):
    operators = ["+", "="]
    # Ensure that there is whitespace around operators so that they are correctly parsed.
    text = add_spaces_around_punctuation(text)
    usages = []
    if "=" in text:
        # Usage must be directly to the left of the = or after the equal
        tokens = text.split()
        eq_index = tokens.index('=')
        if is_valid_identifier(tokens[eq_index - 1]):
            usages.append(tokens[eq_index - 1])
        usages += [t for t in tokens[eq_index:] if is_valid_identifier(t)]
    return usages
