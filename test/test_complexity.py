from ravioli.complexity import calculate_complexity


def names_of(results):
    return [result.name for result in results]


# Test that functions names are extracted correctly.
def test_a_function_can_be_parsed():
    code = """
            int a_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in names_of(results))


def test_two_functions_can_be_parsed():
    code = """
            int a_function(){}
            int another_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in names_of(results))
    assert ('another_function' in names_of(results))


def test_a_commented_function_is_not_extracted():
    code = """
            //int a_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' not in names_of(results))


def test_a_function_in_a_block_is_not_extracted():
    code = """
            /*
            int a_function(){
                //do something
            }
            */
            """
    results = calculate_complexity(code)
    assert ('a_function' not in names_of(results))


def test_a_function_with_arguments():
    code = """
            int a_function(int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in names_of(results))


def test_a_function_with_some_whitespace():
    code = """
            int a_function (int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in names_of(results))


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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
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
    assert ('a_function' in names_of(results))
    assert (len(results) == 1)


def test_an_entire_file_finds_all_functions():
    with open('c/sample.c') as f:
        results = calculate_complexity(f.read())
    assert(len(results) == 20)


# Test that complexity is calculated correctly.
def test_a_function_with_no_decisions_has_complexity_1():
    code = """
        int no_decisions () {
            int a_local_variable = 0;
            return 0;
        }
        """
    results = calculate_complexity(code)
    assert (results[0].complexity == 1)


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
    assert (results[0].complexity == 2)


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
    assert (results[0].complexity == 3)


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
    assert (results[0].complexity == 3)


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
    assert (results[0].complexity == 4)


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
    assert (results[0].complexity == 4)


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
    assert (results[0].complexity == 2)


def test_complexity_of_a_for_loop():
    code = """
            int for_loop() {
                for (i = 0; i < 10; i++){
                    global_variable += 1;
                }
            }
            """
    results = calculate_complexity(code)
    assert (results[0].complexity == 2)


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
    assert (results[0].complexity == 2)


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
    assert (results[0].complexity == 2)


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
    assert (results[0].complexity == 3)


def test_switch_statement_with_a_nested_if():
    code = """
            void switch_statement_with_nested_if(int x, int y) {
                switch (x) {
                    case 1:
                        if (y > 1) {
                            global_variable += 1;
                        }
                        else {
                            global_variable += 2;
                        }
                    case 2:
                        global_variable += 3;
                    default:
                        global_variable += x;
                }
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 4)


def test_nested_switch_statements():
    code = """
            void nested_switches(int x, int y) {
                switch (x) {
                    case 1:
                        switch(y) {
                            case 1:
                                global_variable += 5;
                                break;
                            case 2:
                                global_variable += 10;
                                break;
                            default:
                                global_variable += y;
                        }
                    case 2:
                        global_variable += 3;
                    default:
                        global_variable += x;
                }
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 5)


# These test for "strict cyclomatic complexity" (SCC), also called CC2.
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
    assert (results[0].complexity == 3)


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
    assert (results[0].complexity == 3)


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
    assert (results[0].complexity == 3)


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
    assert (results[0].complexity == 3)


def test_a_for_loop_with_a_compound_conditional():
    code = """
            int compound_for_loop() {
                for (int i = 0, j = 0; (i < 10) && (result == 0); i++) {
                    global_variable++;
                }
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 3)


def test_nested_for_loops():
    code = """
            int nested_for_loops() {
                for (i = 0; i < 10; i++){
                    for (j = 0; j < 10; j++) {
                        global_variable += 1;
                    }
                }
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 3)


def test_a_complicated_example():
    code = """
            int a_complicated_example(int x, int y, int z) {
                int answer = 0;
                if (x > 15) {
                    answer += 3;
                }
                else if ((x > 10) && (y > 5)) {
                    answer += 4;
                }
                else if ((x > 5) && (y > 3) && (z > 1)) {
                    answer += 1;
                    result = 0;
                    for (int i = 0, j = 0; (i < 10) && (result == 0); i++) {
                        if ((global_variable == 15) || (another_global == 12)) {
                            result = 1;
                        }
                    }
                }
                else {
                    answer += 10;
                }
                return answer;
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 11)


def test_a_more_complicated_example():
    code = """
            int a_more_complicated_example(int x, int y, int z) {
                int answer = 0;
                if (x > 15) {
                    answer += 3;
                } else if ((x > 10) && (y > 5)) {
                    answer += 4;
                } else if ((x > 5) && (y > 3) && (z > 1)) {
                    answer += 1;
                    result = 0;
                    for (int i = 0, j = 0; (i < 10) && (result == 0); i++) {
                        if ((global_variable == 15) || (another_global == 12)) {
                            result = 1;
                        }
                    }
                } else {
                    answer += 1;
                    switch (z) {
                        case 1:
                            answer += 4;
                            if (y == 2) {
                                answer += 2;
                            }
                            break;
                        case 2:
                            answer += 5;
                            break;
                        default:
                            answer += 1;
                    }
                    answer += 10;
                }
                return answer;
            }"""
    results = calculate_complexity(code)
    assert (results[0].complexity == 14)


# Get the line numbers of functions.
def test_line_number():
    code = """void a_function(){
            }
    """
    results = calculate_complexity(code)
    assert (results[0].line_number == 1)


def test_a_different_line_number():
    code = """void a_function(){
            }
            void another_function(){
            }
    """
    results = calculate_complexity(code)
    assert (results[1].line_number == 3)


def test_line_number_for_a_function_with_arguments():
    code = """
            void a_function(int a){
            }
    """
    results = calculate_complexity(code)
    assert (results[0].line_number == 2)


def test_line_number_for_a_function_with_different_braces():
    code = """
            void a_function(int a)
            {
            }
    """
    results = calculate_complexity(code)
    assert (results[0].line_number == 2)


def test_line_number_is_found_for_function_not_prototype():
    code = """
            void a_function(int a);
            void a_function(int a)
            {
            }
    """
    results = calculate_complexity(code)
    assert (results[0].line_number == 3)


def test_a_function_with_signature_split_across_lines():
    code = """
            void a_function(int a, int b,
                int c)
            {
            }
    """
    results = calculate_complexity(code)
    assert (results[0].name == 'a_function')


def test_line_number_of_a_function_with_signature_split_across_lines():
    code = """
            void a_function(int a, int b,
                int c)
            {
            }
    """
    results = calculate_complexity(code)
    assert (results[0].line_number == 2)