from ravioli.find_globals import find_globals_by_function


# TODO
# - pointers
# - enums, arrays
# - stucts that are initialized
# - dot and arrow notation for structs


def test_find_function_defintions():
    code = """  int a_function (int x, int y) {
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []}]


def test_find_multiple_function_definitions():
    code = """  int a_function (int x, int y) {
                }
                int another_function (float z) {
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []},
                                              {"name": "another_function",
                                               "line_number": 3,
                                               "undefined_usages": []}]


def test_find_globals_usages_in_function():
    code = """  int a_function (int x, int y) {
                x = a_global;
            }
            """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a_global", 2)]}]


def test_dont_count_a_static_variable_access():
    code = """  static int not_a_global;
                int a_function (int x, int y) {
                    x = not_a_global;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": []}]


def test_dont_count_multiply_defined_static_variable_access():
    code = """  static int not_a_global, also_not_a_global;
                int a_function (int x, int y) {
                    x = not_a_global;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": []}]


def test_dont_count_a_const_variable_access():
    code = """  const int const_value;
                int a_function (int x, int y) {
                    x = const_value;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": []}]


def test_count_a_global_that_is_defined_locally():
    code = """  int a_global;
                int a_function (int x, int y) {
                    x = a_global;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": [("a_global", 3)]}]


def test_nested_counting():
    code = """  int a_global;
                int a_function (bool x) {
                    if (x)
                    {
                        a_global = 1;
                    }
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": [("a_global", 5)]}]


def test_count_global_usages_more_than_once():
    code = """  int a_global;
                int a_function (bool x) {
                    if (x)
                    {
                        a_global = 1;
                    }
                    else
                    {
                        a_global = 2;
                    }
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": [("a_global", 5), ("a_global", 9)]}]


def test_dont_count_variable_defined_at_a_higher_scope():
    code = """  int a_function (bool x) {
                    int y = 0;
                    if (x)
                    {
                        y = 1;
                    }
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []}]


def test_dont_count_variable_defined_at_a_higher_scope_with_more_nesting():
    code = """  int a_function (bool x, bool y) {
                    int z = 0;
                    if (x)
                    {
                        if (y)
                        {
                            z = 1;
                        }
                    }
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []}]


def test_dont_process_struct_as_function_at_top_level():
    code = """  struct my_struct {
                    int a;
                    int b;
                    int c;
                };
                
                int a_function (bool x, bool y) {
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 7,
                                               "undefined_usages": []}]


def test_dont_count_struct_member_def_in_function_as_variable_definition():
    code = """  int a_function (int x) {
                    struct my_struct {
                        int a;
                        int b;
                    };
                    a = x;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a", 6)]}]


def test_dont_count_local_struct_declaration_as_undefined():
    code = """  int a_function (int x) {
                    struct my_struct {
                        int a;
                        int b;
                    } c;
                    c = x;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []}]


def test_dont_count_multiple_local_struct_declarations_as_undefined():
    code = """  int a_function (int x) {
                    struct my_struct {
                        int a;
                        int b;
                    } y, z;
                    y = x;
                    z = x;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": []}]


def test_something_more_complicated():
    code = """  int a_function (bool x, bool y) {
                    int z = 0;
                    if (x) {
                        if (y) {
                            z = a_global;
                        }
                    }
                    if (z) {
                        another_global = 0;
                    }
                }
                int another_function (bool x, bool y) {
                    int z = 0;
                    if (x) {
                        if (y) {
                            z = another_global;
                        }
                    }
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a_global", 5), ("another_global", 9)]},
                                              {"name": "another_function",
                                               "line_number": 12,
                                               "undefined_usages": [("another_global", 16)]}]


def test_count_global_struct_member_accesses_as_global_usages():
    code = """  int a_function () {
                    a_global_struct.value = 5;
                    a_global_struct.another_value = 5;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a_global_struct", 2), ("a_global_struct", 3)]}]


def test_count_global_struct_member_accesses_from_global_pointer_as_global_usages():
    code = """  int a_function () {
                    a_global_struct->value = 5;
                    a_global_struct->another_value = 5;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a_global_struct", 2), ("a_global_struct", 3)]}]


def test_count_global_array_accesses():
    code = """  int a_function () {
                    a_global_array[0] = 5;
                    a_global_array[1] = 6;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 1,
                                               "undefined_usages": [("a_global_array", 2), ("a_global_array", 3)]}]

def test_count_global_array_accesses_if_defined_in_same_file():
    code = """  int a_global_array[10];
                int a_function () {
                    a_global_array[0] = 5;
                    a_global_array[1] = 6;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": [("a_global_array", 3), ("a_global_array", 4)]}]

def test_do_not_count_static_array_accesses():
    code = """  static static_global_array[10];
                int a_function () {
                    static_global_array[0] = 5;
                    static_global_array[1] = 6;
                }
                """
    assert find_globals_by_function(code) == [{"name": "a_function",
                                               "line_number": 2,
                                               "undefined_usages": []}]


# TODO: This finds the struct definition at the top of the file, but we don't want that.
def test_sample_code():
    import pprint
    pp = pprint.PrettyPrinter(depth=4)
    with open('c/sample.c') as f:
        results = find_globals_by_function(f.read())

    pp.pprint(results)
    assert len(results) == 20

