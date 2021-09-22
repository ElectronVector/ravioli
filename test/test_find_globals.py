from ravioli.find_globals import find_globals_by_function


# Test extracting undefined usages.

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
                                               "undefined_usages": ["a_global"]}]


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
                                               "undefined_usages": ["a_global"]}]


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
                                               "undefined_usages": ["a_global"]}]


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
                                               "undefined_usages": ["a_global", "a_global"]}]


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
                                               "undefined_usages": ["a_global", "another_global"]},
                                              {"name": "another_function",
                                               "line_number": 12,
                                               "undefined_usages": ["another_global"]}]


# TODO
# - Count usages for equality tests like ==, !=, >, etc.
# - Test with more operators: ++, ==, etc.
# - Test for stdbool true/false (should not be globals)
# - Find line number
# - Handle comments.