from ravioli.extract_declarations_and_usages import is_valid_identifier, extract_declarations_from_statement, \
    extract_usages_from_statement


# Test extract_declarations_from_statement()


def test_find_declaration_with_custom_type():
    statement = "type_t abcd5 = 0"
    assert extract_declarations_from_statement(statement) == ["abcd5"]


def test_find_declaration_with_compound_type():
    statement = "unsigned int a = 0"
    assert extract_declarations_from_statement(statement) == ["a"]


def test_find_declaration_with_assignment_and_no_spaces():
    statement = "unsigned int a=0"
    assert extract_declarations_from_statement(statement) == ["a"]


def test_find_declaration_with_multilple_qualifiers():
    statement = "static unsigned int a = 0"
    assert extract_declarations_from_statement(statement) == ["a"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement():
    statement = "int a , b"
    assert extract_declarations_from_statement(statement) == ["a", "b"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement_with_no_whitespace():
    statement = "int a, b"
    assert extract_declarations_from_statement(statement) == ["a", "b"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement_with_assignment():
    statement = "int a = 0, b = 1"
    assert extract_declarations_from_statement(statement) == ["a", "b"]


def test_find_more_comma_separated_declarations_in_a_single_statement():
    statement = "int a = 0, b, c = 5"
    assert extract_declarations_from_statement(statement) == ["a", "b", "c"]


def test_dont_find_non_declarations_with_commas():
    statement = "a, b"
    assert extract_declarations_from_statement(statement) == []


# Test extract_usages_from_statement()


def test_dont_find_declarations_as_usages():
    statement = "int a"
    assert extract_usages_from_statement(statement) == []


def test_find_an_assignment():
    statement = "a = 1"
    assert extract_usages_from_statement(statement) == ["a"]


def test_usages_on_the_right_side_of_an_equals():
    statement = "a = b + c"
    assert extract_usages_from_statement(statement) == ["a", "b", "c"]


def test_dont_find_invalid_assignment():
    statement = "0 = b + c"
    assert extract_usages_from_statement(statement) == ["b", "c"]


def test_find_usages_with_no_spaces():
    statement = "a=b+c"
    assert extract_usages_from_statement(statement) == ["a", "b", "c"]


def test_find_usages_with_no_spaces_and_different_operators():
    statement = "a=b-c"
    assert extract_usages_from_statement(statement) == ["a", "b", "c"]


def test_find_usages_with_parentheses_in_expresssions():
    statement = "a= (b - c)*d"
    assert extract_usages_from_statement(statement) == ["a", "b", "c", "d"]


# def test_find_usages_within_function_call():
#     statement = "a_function_call(a,b,c)"
#     assert extract_usages_from_statement(statement) == ["a", "b", "c"]


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