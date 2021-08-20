from pathlib import Path

from ravioli.global_processor import find_variables


def test_find_a_variable_declaration():
    code = """
            int a_variable;
            """
    variables = find_variables(code)
    assert ("a_variable" in variables)


def test_find_two_variable_declarations():
    code = """
            int a_variable;
            int another_variable;
            """
    variables = find_variables(code)
    assert ("a_variable" and "another_variable" in variables)


def test_find_a_variable_declaration_with_assignment():
    code = """
            int a_variable = 0;
            """
    variables = find_variables(code)
    assert ("a_variable" in variables)


def test_find_a_const_variable():
    code = """
            const int const_variable = 0;
            """
    variables = find_variables(code)
    assert("const_variable" in variables)


def test_find_a_static_variable():
    code = """
            static int static_variable = 0;
            """
    variables = find_variables(code)
    assert("static_variable" in variables)


def test_find_a_variable_with_assignement_math():
    code = """
            int a_variable = another_variable + 1;
            """
    variables = find_variables(code)
    assert("a_variable" in variables)


def test_find_multiple_variables_in_the_same_line():
    code = """
                int a, b;
                """
    variables = find_variables(code)
    assert ("a" and "b" in variables)


def test_find_multiple_variables_with_assignments_in_the_same_line():
    code = """
                int a = 0, b = 0;
                """
    variables = find_variables(code)
    assert ("a" and "b" in variables)


def test_do_not_find_nondeclaration_assignment():
    code = """
            a = 0;
            """
    variables = find_variables(code)
    assert ("a" not in variables)


def test_do_not_find_nondeclaration_assignment_with_math():
    code = """
            a = b + 6;
            """
    variables = find_variables(code)
    assert ("a" not in variables)


def test_find_multiple_declaration_statements_on_same_line():
    code = """
            int a; int b;
            """
    variables = find_variables(code)
    assert ("a" and "b" in variables)


def test_find_multiple_declaration_statements_with_assignments_on_same_line():
    code = """
            int a = 0; int b = 0;
            """
    variables = find_variables(code)
    assert ("a" and "b" in variables)


def test_do_not_find_nondeclaration_assignment_from_function_call():
    code = """
            a = function_call(var);
            """
    variables = find_variables(code)
    assert ("a" not in variables)


# def test_file():
#     code = Path('c/sample.c').read_text()
#     print(code)
#     print(find_variables(code))

# pointers, arrays, structs, unions
