from itertools import zip_longest


three_char_operators = ["<<=", ">>="]
two_char_operators = ["<<", "<<", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=", "==", ">=", "<=",
                          "&&", "||", "++", "--", "!="]
one_char_operators = ["<", ">", "+", "-", "*", "/", "%", "=", "!", "&", "|", "^", "~"]
punctuation = ['(', ')', ',']

def extract_declarations(text):
    """
    Find all declarations of new variables in the current text.
    :param text: A bit of C code that ends with a semi-colon.
    :return: An array of variable names declared in the text.
    """
    # Ensure that there is whitespace around all commas.
    text = add_spaces_around_punctuation(text)
    text = add_spaces_around_operators(text)
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
            if type_found or (len(potential_declaration) >= 2):
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
        elif is_operator(t) or is_punctuation(t):
            # You can't have a declaration separated by an operator or punctuation.
            potential_declaration = []

    if potential_declaration:
        # A declaration should be saved if 1) there are at least two consecutive valid identifiers or 2) we previously
        # found two consecutive identifiers and this is another declaration after a comma.
        if type_found or (len(potential_declaration) >= 2):
            declarations.append(potential_declaration[-1])

    return declarations


def is_punctuation(s):
    return s in punctuation


def is_operator(s):
    return s in (one_char_operators + two_char_operators + three_char_operators)


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

    # Todo: Check for other reserved keywords.
    if s in ["if", "else", "do", "while", "break", "return"]:
        return False

    return True


def add_spaces_around_punctuation(s):
    return ''.join(map(lambda c: f" {c} " if is_punctuation(c) else c, s))


def add_spaces_around_operators(s):
    s_with_spaces = ""
    i = 0
    while i < len(s):
        if s[i:i+3] in three_char_operators:
            s_with_spaces += " " + s[i:i+3] + " "
            i += 3
        elif s[i:i+2] in two_char_operators:
            s_with_spaces += " " + s[i:i + 2] + " "
            i += 2
        elif s[i] in one_char_operators:
            s_with_spaces += " " + s[i] + " "
            i += 1
        else:
            s_with_spaces += s[i]
            i += 1

    return s_with_spaces


def simplify_assignment_operators(s):
    extra_assignment_operators = ["+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|="]
    for x in extra_assignment_operators:
        s = s.replace(x, "=")
    return s


def extract_usages(text):
    # Ensure that there is whitespace around operators and punctuation so that they are correctly parsed.
    text = add_spaces_around_operators(text)
    text = add_spaces_around_punctuation(text)
    # Convert multicharacter assignment operators to = so that can detect them all the same way. We really don't\
    # car about what the actual assignment operator is.
    text = simplify_assignment_operators(text)
    usages = []
    # Look at all the whitespace-delimited tokens in the text.
    tokens = text.split()
    if "=" in tokens:
        # Usage must be directly to the left of the = or after the equal
        eq_index = tokens.index('=')
        if is_valid_identifier(tokens[eq_index - 1]):
            # Before the =
            usages.append(tokens[eq_index - 1])
        # After the =
        usages += [t for t in tokens[eq_index:] if is_valid_identifier(t)]
    elif not extract_declarations(text):
        # If there are no declarations in this text, then we can look at everything for tokens.
        for token, next_token in zip_longest(tokens, tokens[1:]):
            if is_valid_identifier(token) and not next_token == "(":
                usages.append(token)

    return usages
