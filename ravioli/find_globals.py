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


def find_globals_by_function(code):
    functions = {}
    statements = extract_statements(code)
    for s in statements:
        if isinstance(s, Block):
            functions[s.title.split()[-1]] = []
    return functions

