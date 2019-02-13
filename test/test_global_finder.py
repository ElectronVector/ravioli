import re


def test_a_single_global():
    code = """
            int a_global;
            """
    results = find_globals(code)
    assert ('a_global' in results)


def test_multiple_globals():
    code = """
            int a_global;
            uint8_t another_global;
            """
    results = find_globals(code)
    assert ('a_global' in results)
    assert ('another_global' in results)


def test_a_global_with_assignment():
    code = """
            int a_global=0;
            """
    results = find_globals(code)
    assert ('a_global' in results)


def test_with_assignment_and_whitespace():
    code = """
            int a_global = 0;
            """
    results = find_globals(code)
    assert ('a_global' in results)


def test_a_function_variable_is_not_found():
    code = """
            void a_function() {
                int not_a_global;
            }
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def test_a_deeper_function_variable_is_not_found():
    code = """
            void a_function(int x) {
                if (x > 0) {
                    // do something
                }
                else {
                    int not_a_global;
                }
            }
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def find_globals(code):
    results = []
    # Remove anything between brackets.
    code = re.sub(r'{.*}', '{}', code, flags=re.DOTALL)
    # Remove whitespace around any equals.
    code = re.sub(r'\s*=\s*', '=', code)
    global_matcher = re.compile(r'\s+(\w+)[;|=]')
    for m in global_matcher.finditer(code):
        name = m.group(1)
        results.append(name)
    return results
