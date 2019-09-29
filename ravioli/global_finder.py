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
    code = re.sub(r'{[^}]*}', '{}', code, flags=re.DOTALL)
    # Find all the globals.
    global_matcher = re.compile(r'([\w\t\f\v {}]+)\s+(\w+)[\d\[\]]*(?:;|\s*=)')
    for m in global_matcher.finditer(code):
        qualifiers = m.group(1)
        name = m.group(2)
        line_number = __get_line_number(m.group(), original_code)
        if ('static' not in qualifiers
                and 'typedef' not in qualifiers
                and 'extern' not in qualifiers
                and 'const' not in qualifiers):
            results.append(GlobalVariable(name, line_number))
    return results


def __get_line_number(match, code):
    if '{}' in match:
        # Handle the special case where we've matched a global struct declared as part of its
        # definition. We strip the contents out of the brackets to help with parsing, so we
        # won't be able to find this match in the original code.
        match = match.split('}')[1]
    for line_number, line in enumerate(code.splitlines(True), 1):
        if match in line:
            return line_number
    return 0


def __strip_preprocessor_directives(code):
    code_lines = code.splitlines(True)
    non_pound_defines = [line for line in code_lines if not line.lstrip().startswith("#")]
    code = "".join(non_pound_defines)
    return code


