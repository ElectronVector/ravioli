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


def find_globals_by_function(code):
    functions = {}
    statements = extract_statements(code)
    for s in statements:
        if isinstance(s, Block):
            functions[get_last_word(s.title)] = []
    return functions

