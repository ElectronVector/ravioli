from ravioli.find_globals import extract_undefined_usages, find_globals_by_function


# Test extracting undefined usages.


def test_do_not_find_a_defined_usage():
    code = """
            int a;
            a = 0;
        """
    assert extract_undefined_usages(code) == []


def test_find_an_undefined_usage():
    code = """
            a = 0;
        """
    assert extract_undefined_usages(code) == ["a"]


def test_do_not_find_an_undefined_usage_after_definition_and_assignment():
    code = """
            int a = 0;
            a = 1;
        """
    assert extract_undefined_usages(code) == []


def test_find_usage_on_the_right_side_of_the_equals():
    code = """
            int a = 0;
            a = global + 1;
        """
    assert extract_undefined_usages(code) == ["global"]


def test_find_usages_with_underscores():
    code = """
            int a = 0;
            a = some_global + 1;
        """
    assert extract_undefined_usages(code) == ["some_global"]


def test_find_function_defintions():
    code = """
    int a_function (int x, int y) {
    }
    """
    assert find_globals_by_function(code) == {"a_function": []}


def test_find_multiple_function_definitions():
    code = """
    int a_function (int x, int y) {
    }
    int another_function (float z) {
    }
    """
    assert find_globals_by_function(code) == {"a_function": [], "another_function": []}


def test_find_globals_usages_in_function():
    code = """
    int a_function (int x, int y) {
        x = a_global;
    }
    """
    assert find_globals_by_function(code) == {"a_function": ["a_global"]}


def test_dont_count_a_static_variable_access():
    code = """
    static int not_a_global;
    int a_function (int x, int y) {
        x = not_a_global;
    }
    """
    assert find_globals_by_function(code) == {"a_function": []}