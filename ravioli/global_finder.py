import re

from ravioli.strip_comments import strip_comments


def find_globals(code):
    results = []
    # Remove all comments.
    code = strip_comments(code)
    # Remove #ifs
    code_lines = code.splitlines(True)
    non_pound_defines = [line for line in code_lines if not line.lstrip().startswith("#")]
    code = "".join(non_pound_defines)
    # Remove anything between brackets.
    code = re.sub(r'{.*}', '{}', code, flags=re.DOTALL)
    # Remove whitespace around any equals.
    code = re.sub(r'\s*=\s*', '=', code)
    # Find all the globals.
    global_matcher = re.compile(r'(.*)\s+(\w+)[;|=]')
    for m in global_matcher.finditer(code):
        qualifiers = m.group(1)
        name = m.group(2)
        if ('static' not in qualifiers
                and 'typedef' not in qualifiers
                and 'extern' not in qualifiers):
            results.append(name)
    return results
