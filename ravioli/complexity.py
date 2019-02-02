import re


def calculate_complexity(code):
    keywords = ['if', 'while', 'for', 'switch']
    results = {}
    function_matcher = re.compile(r'\s+(\w+)\s*\(.*\)\s*{', re.MULTILINE)
    for m in function_matcher.finditer(code):
        name = m.group(1)
        if name not in keywords:
            results[name] = 1
    return results