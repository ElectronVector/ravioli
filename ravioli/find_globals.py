from collections import namedtuple

from ravioli.extract_declarations_and_usages import extract_declarations, extract_usages
from ravioli.extract_statements import extract_statements, Block


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


# A usage is a name and a line number tuple. Give the elements names to make things more readable.
Use = namedtuple("Use", ["name", "line_number"])


def __find_undefined_usages(statements):
    undefined_usages = []
    declarations = []
    usages = []
    for s in statements:
        if isinstance(s, Block):
            # If this is a block, recursively calculate the undefined usages in each deeper-nested block.
            # Only add undefined usages if they are not defined at this level.
            undefined_usages += [u for u in __find_undefined_usages(s.children) if u.name not in declarations]
            declarations.append(s.trailing_content)
        else:
            # Attempt to extract and save declarations and usages from all statements at this nesting level.
            for new_declaration in extract_declarations(s.text):
                declarations.append(new_declaration)
            for new_usage in extract_usages(s.text):
                usages.append(Use(new_usage, s.line_number))

    # Undefined usages are usages that haven't been declared.
    undefined_usages += [u for u in usages if u.name not in declarations]

    return undefined_usages


def find_globals_by_function(code):
    not_globals = []
    functions = []
    statements = extract_statements(code)
    for s in statements:
        if isinstance(s, Block):
            if "struct" in s.title.split():
                continue
            # The title includes the return type so we need to get the last word as the name of the function.
            # Find the undefined usages in the child statements belonging to the block.
            functions.append({"name": get_last_word(s.title),
                              "line_number": s.line_number,
                              "undefined_usages": __find_undefined_usages(s.children)})
        else:
            # Look for non-global variable definitions.
            for decl in extract_declarations(s.text):
                # For each potential new declaration, check for the use of a keyword that would make it not a global.
                if is_not_a_global(s.text):
                    # This is not a global variable.
                    not_globals.append(decl)

    # Remove any undefined uses from functions for variables declared as static.
    for function in functions:
        function["undefined_usages"] = [u for u in function["undefined_usages"] if u.name not in not_globals]

    return functions
