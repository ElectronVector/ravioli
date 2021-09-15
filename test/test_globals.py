from ravioli.globals import extract_statements, extract_undefined_usages, is_valid_identifier, \
    extract_declarations_from_statement


def test_single_statement():
    code = """
        int a;
    """
    assert extract_statements(code) == ["int a"]


def test_multiple_statements():
    code = """
        int a; int b;
        int c;
    """
    assert extract_statements(code) == ["int a", "int b", "int c"]


def test_multiple_statements_with_extra_whitespace():
    code = """
        int   a; int b =   0;
        int
            c;
    """
    assert extract_statements(code) == ["int a", "int b = 0", "int c"]

# Test getting line numbers from statements.
# TODO

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


# Test extract_declarations_from_statement()


def test_find_delcaration_with_custom_type():
    statement = "type_t abcd5 = 0"
    assert extract_declarations_from_statement(statement) == ["abcd5"]


# Test extract_usages_from_statement()
# TODO


# Test identifier detection
def test_all_alphas_is_valid():
    assert is_valid_identifier("name")


def test_alphas_and_underscore_is_valid():
    assert is_valid_identifier("a_name")


def test_starting_with_underscore_is_valid():
    assert is_valid_identifier("_a_name")


def test_starting_with_number_is_invalid():
    assert not is_valid_identifier("1invalidname")


def test_number_not_at_start_is_valid():
    assert is_valid_identifier("name1")


def test_a_single_letter_is_valid():
    assert is_valid_identifier("a")


def test_a_single_number_is_invalid():
    assert not is_valid_identifier("1")