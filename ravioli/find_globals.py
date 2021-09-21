from ravioli.extract_declarations_and_usages import extract_declarations_from_statement, extract_usages_from_statement
from ravioli.extract_statements import extract_statements, Block


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


def get_last_word(s):
    """
    Get the last whitespace delimited word in the string.
    :param s: The string to extract from.
    :return:  The last whole word present in the string.
    """
    return s.split()[-1]


def is_not_a_global(s):
    """
    Test if this statement contains keywords to suggest that a declaration here is not a global variable declaration.
    :param s: The string to check.
    :return: True if a non-global keyword is found.
    """
    not_global_keywords = ["static", "const"]
    return any(word in not_global_keywords for word in s.split())


def find_undefined_usages(statements):
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


def find_globals_by_function(code):
    not_globals = []
    functions = {}
    statements = extract_statements(code)
    for s in statements:
        if isinstance(s, Block):
            # The title includes the return type so we need to get the last word as the name of the function.
            # Find the undefined usages in the child statements belonging to the block.
            functions[get_last_word(s.title)] = find_undefined_usages(s.children)
        else:
            # Look for non-global variable definitions.
            for decl in extract_declarations_from_statement(s):
                # For each potential new declaration, check for the use of a keyword that would make it not a global.
                if is_not_a_global(s):
                    # This is not a global variable.
                    not_globals.append(decl)

    # Remove any undefined uses from functions for variables declared as static.
    for function, undefined_usages in functions.items():
        # items() makes a copy of the dictionary so we can modify the original.
        functions[function] = [u for u in undefined_usages if u not in not_globals]

    return functions

