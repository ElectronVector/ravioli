import re


def calculate_complexity(code):
    keywords = ['if', 'while', 'for', 'switch']
    results = {}
    function_matcher = re.compile(r'\s+(\w+)\s*\(.*\)\s*{', re.MULTILINE)
    current_function = ''
    for m in function_matcher.finditer(code):
        name = m.group(1)
        if name not in keywords:
            results[name] = 1
            # Save the current function.
            current_function = name
        elif name == 'if' or name == 'while' or name == 'for':
            results[current_function] += 1
    return results
