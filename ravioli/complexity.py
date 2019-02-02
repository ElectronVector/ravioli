import re

decision_keywords = ['if', 'while', 'for']

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
        elif name in decision_keywords:
            # This is a decision, increment the complexity.
            results[current_function] += 1
    return results
