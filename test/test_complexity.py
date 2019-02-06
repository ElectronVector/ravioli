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


def test_a_function_with_2_decisions_has_complexity_3():
    code = """
            int else_if(int i) {
                if (i >= 5) {
                    return i + 1;
                }
                else if (i >= 0) {
                    return i + 2;
                }
                else {
                    return i - 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["else_if"] == 3)


def test_a_function_with_a_nested_if():
    code = """
            int nested_if(int i) {
                if (i >= 0) {
                    if (i >= 5) {
                        return i + 2;
                    }
                    else {
                        return i + 1;
                    }
                }
                else {
                    return i - 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["nested_if"] == 3)


def test_a_function_with_a_nested_else_if():
    code = """
            int nested_else_if(int i) {
                if (i >= 0) {
                    if (i >= 5) {
                        return i + 2;
                    }
                    else if (i >= 3) {
                        return i + 4;
                    }
                    else {
                        return i + 1;
                    }
                }
                else {
                    return i - 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["nested_else_if"] == 4)


def test_a_function_with_a_nested_else_if_and_extra_statements():
    code = """
            int nested_else_if_with_extra_statements(int i) {
                i = i + 1;
                if (i >= 0) {
                    i = i + 1;
                    if (i >= 5) {
                        i = i + 1;
                        return i + 2;
                    }
                    else if (i >= 3) {
                        i = i + 1;
                        return i + 4;
                    }
                    else {
                        return i + 1;
                    }
                }
                else {
                    return i - 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["nested_else_if_with_extra_statements"] == 4)


def test_a_function_with_a_while_loop():
    code = """
            int while_loop() {
                i = 0;
                while (i < 10){
                    global_variable += 1;
                    i++;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["while_loop"] == 2)


def test_complexity_of_a_for_loop():
    code = """
            int for_loop() {
                for (i = 0; i < 10; i++){
                    global_variable += 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["for_loop"] == 2)


def test_a_function_with_a_do_while_loop():
    code = """
            int do_while_loop() {
                i = 0;
                do {
                    global_variable += 1;
                    i++;
                } while (i < 10);
            }
            """
    results = calculate_complexity(code)
    assert (results["do_while_loop"] == 2)


def test_a_function_with_a_do_while_loop_and_no_whitespace():
    code = """
            int do_while_loop() {
                i = 0;
                do {
                    global_variable += 1;
                    i++;
                }while (i < 10);
            }
            """
    results = calculate_complexity(code)
    assert (results["do_while_loop"] == 2)


def test_complexity_of_a_switch():
    code = """
            void switch_statement(int x) {
                switch (x) {
                    case 1:
                        global_variable += 2;
                    case 2:
                        global_variable += 3;
                    default:
                        global_variable += x;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results["switch_statement"] == 3)


# This tests for "strict cyclomatic complexity" (SCC), also called CC2.
def test_compound_conditional_in_if():
    code = """
            int compound_if(int i) {
                if ((i >= 0) && (i < 10)){
                    return i + 2;
                }
                else {
                    return i + 1;
                }
            }"""
    results = calculate_complexity(code)
    assert (results["compound_if"] == 3)


def test_compound_conditional_in_if_no_whitespace():
    code = """
            int compound_if(int i) {
                if ((i >= 0)&&(i < 10)){
                    return i + 2;
                }
                else {
                    return i + 1;
                }
            }"""
    results = calculate_complexity(code)
    assert (results["compound_if"] == 3)


def test_compound_conditional_with_or_in_if():
    code = """
            int compound_if(int i) {
                if ((i >= 0) || (i < 10)){
                    return i + 2;
                }
                else {
                    return i + 1;
                }
            }"""
    results = calculate_complexity(code)
    assert (results["compound_if"] == 3)


def test_a_while_loop_with_a_compound_conditional():
    code = """
            int compound_while_loop(int j, int i) {
                i = 0;
                while ((j == 1) && (i < 10)) {
                    global_variable += 1;
                    i++;
                    j++;
                }
            }"""
    results = calculate_complexity(code)
    assert (results["compound_while_loop"] == 3)
