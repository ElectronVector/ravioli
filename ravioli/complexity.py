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

    for m in function_matcher.finditer(code):
        name = m.group(1)
        if is_a_function(name):
            # We found a new function. Add it to the results.
            results[name] = 1
            # Find the contents of this function by matching braces.
            start_index = m.end()
            i = start_index
            brace_nesting = 1
            while brace_nesting > 0:
                if code[i] == '{':
                    brace_nesting += 1
                elif code[i] == '}':
                    brace_nesting -= 1
                i += 1
            end_index = i

            # We found the start and the end of the functions in the string. Iterate over these
            for x in re.finditer(r'\s+(\w+)\s*\(.*\)', code[start_index:end_index], re.MULTILINE):
                y = x.group(1)
                if is_a_decision(y):
                    results[name] += 1
    return results
