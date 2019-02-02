from ravioli.complexity import calculate_complexity

# Test that functions names are extracted correctly.
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


def test_a_function_with_a_do_while():
    code = """
            int a_function (int a){
                int x = 0;
                do {
                    x++;
                } while (x < 5);
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)


def test_a_function_with_a_switch():
    code = """
            int a_function (int a){
                switch (a)
                {
                case 0:
                    return 0;
                    break;
                case 1:
                    return 1;
                    break;
                default
                    return a;
                    break;
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


# Test that complexity is calculated correctly.
def test_a_function_with_no_decisions_has_complexity_1():
    code = """
        int no_decisions () {
            int a_local_variable = 0;
            return 0;
        }
        """
    results = calculate_complexity(code)
    assert (results["no_decisions"] == 1)


def test_a_function_with_1_decision_has_complexity_2():
    code = """
            int if_else(int i) {
                if (i >= 0) {
                    return i + 1;
                }
                else {
                    return i - 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["if_else"] == 2)


