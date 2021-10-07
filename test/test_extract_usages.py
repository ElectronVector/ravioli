from ravioli.extract_declarations_and_usages import extract_usages


def test_dont_find_declarations_as_usages():
    statement = "int a"
    assert extract_usages(statement) == []


def test_find_an_assignment():
    statement = "a = 1"
    assert extract_usages(statement) == ["a"]


def test_usages_on_the_right_side_of_an_equals():
    statement = "a = b + c"
    assert extract_usages(statement) == ["a", "b", "c"]


def test_dont_find_invalid_assignment():
    statement = "0 = b + c"
    assert extract_usages(statement) == ["b", "c"]


def test_find_usages_with_no_spaces():
    statement = "a=b+c"
    assert extract_usages(statement) == ["a", "b", "c"]


def test_find_usages_with_no_spaces_and_different_operators():
    statement = "a=b-c"
    assert extract_usages(statement) == ["a", "b", "c"]


def test_find_usages_with_parentheses_in_expresssions():
    statement = "a= (b - c)*d"
    assert extract_usages(statement) == ["a", "b", "c", "d"]


def test_find_an_assignment_with_plus():
    statement = "a += 1"
    assert extract_usages(statement) == ["a"]


def test_find_an_assignment_with_plus_and_no_spaces():
    statement = "a+=1"
    assert extract_usages(statement) == ["a"]


def test_find_an_assignment_with_minus():
    statement = "a -= 1"
    assert extract_usages(statement) == ["a"]


def test_find_an_assignment_with_times():
    statement = "a *= 1"
    assert extract_usages(statement) == ["a"]


def test_find_a_usage_with_a_shift_operator():
    statement = "a = b << 1"
    assert extract_usages(statement) == ["a", "b"]


def test_find_a_usage_with_a_shift_operator_and_no_whitespace():
    statement = "a=b<<1"
    assert extract_usages(statement) == ["a", "b"]


def test_find_a_usages_in_boolean_conditional():
    statement = "x > y"
    assert extract_usages(statement) == ["x", "y"]


def test_find_usages_in_more_complicated_boolean_logic():
    code = "!a||b&&c"
    assert extract_usages(code) == ["a", "b", "c"]


def test_find_a_usage_with_an_increment_operator():
    statement = "a++"
    assert extract_usages(statement) == ["a"]


def test_find_a_usage_with_a_decrement_operator():
    statement = "a = b--"
    assert extract_usages(statement) == ["a", "b"]


def test_dont_find_false_as_usage():
    statement = "a = false"
    assert extract_usages(statement) == ["a"]


def test_dont_find_true_as_usage():
    statement = "a = true"
    assert extract_usages(statement) == ["a"]


def test_dont_find_capital_false_as_usage():
    statement = "a = FALSE"
    assert extract_usages(statement) == ["a"]


def test_find_usages_within_function_call():
    statement = "a_function_call(a,b,c)"
    assert extract_usages(statement) == ["a", "b", "c"]


def test_find_usages_within_function_call_with_some_math():
    code = "a_function_call(a+x,(b%y),c<<z)"
    assert extract_usages(code) == ["a", "x", "b", "y", "c", "z"]


def test_more_conditionals():
    code = "global_variable"
    assert extract_usages(code) == ["global_variable"]


def test_struct_member_access():
    code = "global_struct.value = 5"
    assert extract_usages(code) == ["global_struct"]


def test_struct_member_access_with_multiple_nesting_levels():
    code = "global_struct.nested.value = 5"
    assert extract_usages(code) == ["global_struct"]


def test_dont_extract_floating_point_numbers():
    code = "global_struct.nested.value = 5.5f"
    assert extract_usages(code) == ["global_struct"]


def test_struct_member_access_with_dereference():
    code = "global_struct->value = 5"
    assert extract_usages(code) == ["global_struct"]


def test_extract_array_usage():
    code = "an_array[5] = 0"
    assert extract_usages(code) == ["an_array"]


def test_extract_multiple_array_usages():
    code = "an_array[5] = another_array[0]"
    assert extract_usages(code) == ["an_array", "another_array"]