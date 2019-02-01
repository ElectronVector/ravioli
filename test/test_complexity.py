import re


def calculate_complexity(code):
    keywords = ['if', 'while', 'for']
    results = {}
    function_matcher = re.compile(r'\s+(\w+)\s*\(.*\)\s*{', re.MULTILINE)
    for m in function_matcher.finditer(code):
        name = m.group(1)
        if name not in keywords:
            results[name] = 1
    return results


def test_a_function_can_be_parsed():
    code = """
            int a_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_two_functions_can_be_parsed():
    code = """
            int a_function(){}
            int another_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert ('another_function' in results)


def test_a_function_with_arguments():
    code = """
            int a_function(int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_a_function_with_some_whitespace():
    code = """
            int a_function (int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_a_function_with_an_if():
    code = """
            int a_function (int a){
                if (a > 5) {
                    return 0;
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)


def test_a_function_with_a_while():
    code = """
            int a_function (int a){
                int x = 0;
                while (x < 5) {
                    x++;
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)


def test_a_function_with_a_for_loop():
    code = """
            int a_function (int a){
                for (int x = 0; x < 5; x++) {
                    a++;
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)

def test_a_function_which_calls_another_function():
    code = """
            int a_function (int a){
                if (a > 5) {
                    call_another_function(a + 1);
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)


def test_a_function_with_different_brace_placement():
    code = """
            int a_function (int a)
            {
                if (a > 5) {
                    call_another_function(a + 1);
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)

