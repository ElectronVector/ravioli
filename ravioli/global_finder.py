import re

from ravioli.code_item import CodeItem
from ravioli.strip_comments import strip_comments


def find_globals(code):
    original_code = code
    results = []
    # Remove all comments.
    code = strip_comments(code)
    # Remove #ifs, #elifs, #ifdefs
    code = __strip_preprocessor_directives(code)
    # Remove anything between brackets.
    code = re.sub(r'{.*}', '{}', code, flags=re.DOTALL)
    # Remove whitespace around any equals.
    code = re.sub(r'\s*=\s*', '=', code)
    # Find all the globals.
    global_matcher = re.compile(r'(.*)\s+(\w+)[;|=]')
    for m in global_matcher.finditer(code):
        qualifiers = m.group(1)
        name = m.group(2)
        line_number = __get_line_number(m.group(), original_code)
        if ('static' not in qualifiers
                and 'typedef' not in qualifiers
                and 'extern' not in qualifiers):
            results.append(CodeItem(name, line_number))
    return results


def __get_line_number(match, code):
    for line_number, line in enumerate(code.splitlines(True), 1):
        if match in line:
            return line_number
    return 0


def __strip_preprocessor_directives(code):
    code_lines = code.splitlines(True)
    non_pound_defines = [line for line in code_lines if not line.lstrip().startswith("#")]
    code = "".join(non_pound_defines)
    return code
