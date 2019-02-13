import re


def find_globals(code):
    results = []
    # Remove anything between brackets.
    code = re.sub(r'{.*}', '{}', code, flags=re.DOTALL)
    # Remove whitespace around any equals.
    code = re.sub(r'\s*=\s*', '=', code)
    # Find all the globals.
    global_matcher = re.compile(r'(.*)\s+(\w+)[;|=]')
    for m in global_matcher.finditer(code):
        qualifiers = m.group(1)
        name = m.group(2)
        if 'static' not in qualifiers and 'typedef' not in qualifiers and 'extern' not in qualifiers:
            results.append(name)
    return results
