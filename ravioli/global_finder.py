import re

from ravioli.global_variable import GlobalVariable
from ravioli.strip_comments import strip_comments


def find_globals(code):
    original_code = code
    results = []
    # Remove all comments.
    code = strip_comments(code)
    # Remove #ifs, #elifs, #ifdefs
    code = __strip_preprocessor_directives(code)
    if "some_const_array" in code:
        print(code)
    # Remove anything between brackets.
    code = __strip_bracketed_code(code)
    # Find all the globals.
    global_matcher = re.compile(r'([\w\t\f\v {}]+)\s+\**(\w+)(?:;|\s*=|\[)')
    for m in global_matcher.finditer(code):
        qualifiers = m.group(1)
        name = m.group(2)
        line_number = __get_line_number(m.group(), name, original_code)
        if ('static' not in qualifiers
                and 'typedef' not in qualifiers
                and 'extern' not in qualifiers
                and 'const' not in qualifiers):
            results.append(GlobalVariable(name, line_number))
    return results

def __strip_bracketed_code(code):
    stripped_chars = list()
    i = 0
    brace_nesting = 0
    while i < len(code):
        if code[i] == '{':
            brace_nesting += 1
        elif code[i] == '}':
            brace_nesting -= 1
        elif brace_nesting == 0:
            stripped_chars.append(code[i])
        i += 1
    return "".join(stripped_chars)

def __get_line_number(match, name, code):
    for line_number, line in enumerate(code.splitlines(True), 1):
        if match in line:
            return line_number
    # Handle special cases, e.g. where we've matched a global struct declared as part of its
    # definition. We strip the contents out of the brackets to help with parsing, so we
    # won't be able to find this match in the original code. Instead, match on first appearance
    # of the name.
    for line_number, line in enumerate(code.splitlines(True), 1):
        if name in line and __name_is_not_substring(name, line):
            return line_number
    return 0

def __name_is_not_substring(name, line):
    return re.search(r'\b'+name+'[\b;\\[]', line) is not None

def __strip_preprocessor_directives(code):
    code_lines = code.splitlines(True)
    non_pound_defines = [line for line in code_lines if not line.lstrip().startswith("#")]
    code = "".join(non_pound_defines)
    return code


