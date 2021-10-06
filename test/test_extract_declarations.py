from ravioli.extract_declarations_and_usages import extract_declarations


def test_find_declaration_with_custom_type():
    statement = "type_t abcd5 = 0"
    assert extract_declarations(statement) == ["abcd5"]


def test_find_declaration_with_compound_type():
    statement = "unsigned int a = 0"
    assert extract_declarations(statement) == ["a"]


def test_find_declaration_with_assignment_and_no_spaces():
    statement = "unsigned int a=0"
    assert extract_declarations(statement) == ["a"]


def test_find_declaration_with_multilple_qualifiers():
    statement = "static unsigned int a = 0"
    assert extract_declarations(statement) == ["a"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement():
    statement = "int a , b"
    assert extract_declarations(statement) == ["a", "b"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement_with_no_whitespace():
    statement = "int a, b"
    assert extract_declarations(statement) == ["a", "b"]


def test_find_multiple_comma_separated_declarations_in_a_single_statement_with_assignment():
    statement = "int a = 0, b = 1"
    assert extract_declarations(statement) == ["a", "b"]


def test_find_more_comma_separated_declarations_in_a_single_statement():
    statement = "int a = 0, b, c = 5"
    assert extract_declarations(statement) == ["a", "b", "c"]


def test_dont_find_non_declarations_with_commas():
    statement = "a, b"
    assert extract_declarations(statement) == []


def test_dont_find_non_declarations_with_boolean_operators():
    statement = "a > b"
    assert extract_declarations(statement) == []


def test_dont_find_non_declarations_with_other_boolean_operators():
    statement = "a < b"
    assert extract_declarations(statement) == []


def test_dont_find_non_declarations_with_two_char_boolean_operators():
    statement = "a <= b"
    assert extract_declarations(statement) == []


def test_extract_struct_declaration_with_definition():
    statement = """ struct my_struct {
                        int a;
                        int b;
                    } c"""
    assert extract_declarations(statement) == ["c"]


def test_extract_multiple_struct_declarations_with_definition():
    statement = """ struct my_struct {
                        int a;
                        int b;
                    } c, d"""
    assert extract_declarations(statement) == ["c", "d"]


def test_extract_array_definition():
    code = "int my_array[5];"
    assert extract_declarations(code) == ["my_array"]


