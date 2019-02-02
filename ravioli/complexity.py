import re


# Determine if this name is keyword that makes a decision/
def is_a_decision(name):
    decision_keywords = ['if', 'while', 'for']
    return name in decision_keywords


# Determine if this name is a function (and not a keyword that looks like one).
def is_a_function(name):
    keywords_that_look_like_functions = ['if', 'while', 'for', 'switch']
    return name not in keywords_that_look_like_functions


def calculate_complexity(code):
    results = {}
    function_matcher = re.compile(r'\s+(\w+)\s*\(.*\)\s*{', re.MULTILINE)
    current_function = ''
    for m in function_matcher.finditer(code):
        name = m.group(1)
        if is_a_function(name):
            # We found a new function. Add it to the results.
            results[name] = 1
            # Save the current function.
            current_function = name
        elif is_a_decision(name):
            # This is a decision, increment the complexity of the current function.
            results[current_function] += 1
    return results
