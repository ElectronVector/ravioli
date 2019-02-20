from ravioli.global_finder import find_globals


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


def test_a_static_is_not_global():
    code = """
            int a_global;
            static int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def test_typedefs():
    code = """
            typedef int my_new_type;
            my_new_type a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in results)


def test_structs():
    code = """
            struct point_t {
                int x;
                int y;
            };
            struct point_t a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in results)


def test_struct_globals_declared_with_definition():
    code = """
            struct point_t {
                int x;
                int y;
            } a_global;
            """
    results = find_globals(code)
    assert(len(results) == 1)
    assert('a_global' in results)


def test_an_extern_is_not_global():
    code = """
            int a_global;
            extern int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def test_commented_global_is_not_global():
    code = """
            int a_global;
            /*int not_a_global;*/
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def test_global_in_single_line_comment_not_counted():
    code = """
            int a_global;
            //int not_a_global;
            """
    results = find_globals(code)
    assert ('not_a_global' not in results)


def test_dont_count_preprocessor_ifs():
    code = """
            #if configUSE_PREEMPTION == 0
            {
                taskYIELD();
            }
            #endif
            """
    results = find_globals(code)
    assert ('configUSE_PREEMPTION' not in results)

# Don't count:
# #if configUSE_PREEMPTION == 0
# {
#     taskYIELD();
# }
# #endif

# Don't count 'break' (see:queue.c)
# Don't count words with static or extern in them.