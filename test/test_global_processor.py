from pathlib import Path

from ravioli.global_processor import find_variables
from ravioli.variable import Variable


def test_find_a_variable_declaration():
    code = """
            int a_variable;
            """
    variables = find_variables(code)
    assert (Variable("a_variable") in variables)


def test_find_two_variable_declarations():
    code = """
            int a_variable;
            int another_variable;
            """
    variables = find_variables(code)
    assert (Variable("a_variable") and Variable("another_variable") in variables)


def test_find_a_variable_declaration_with_assignment():
    code = """
            int a_variable = 0;
            """
    variables = find_variables(code)
    assert (Variable("a_variable") in variables)


def test_find_a_const_variable():
    code = """
            const int const_variable = 0;
            """
    variables = find_variables(code)
    assert (Variable("const_variable") in variables)


def test_find_a_static_variable():
    code = """
            static int static_variable = 0;
            """
    variables = find_variables(code)
    assert (Variable("static_variable") in variables)


def test_find_a_variable_with_assignement_math():
    code = """
            int a_variable = another_variable + 1;
            """
    variables = find_variables(code)
    assert (Variable("a_variable") in variables)


def test_find_a_compound_type_variable_declaration():
    code = """
            unsigned int a_variable;
            """
    variables = find_variables(code)
    assert (Variable("a_variable") in variables)

def test_find_multiple_variables_in_the_same_line():
    code = """
                int a, b;
                """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") in variables)


def test_find_multiple_variables_with_assignments_in_the_same_line():
    code = """
                int a = 0, b = 0;
                """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") in variables)


def test_do_not_find_nondeclaration_assignment():
    code = """
            a = 0;
            """
    variables = find_variables(code)
    assert (Variable("a") not in variables)


def test_do_not_find_nondeclaration_assignment_with_math():
    code = """
            a = b + 6;
            """
    variables = find_variables(code)
    assert (Variable("a") not in variables)


def test_find_multiple_declaration_statements_on_same_line():
    code = """
            int a; int b;
            """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") in variables)


def test_find_multiple_declaration_statements_with_assignments_on_same_line():
    code = """
            int a = 0; int b = 0;
            """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") in variables)


def test_do_not_find_nondeclaration_assignment_from_function_call():
    code = """
            a = function_call(var);
            """
    variables = find_variables(code)
    assert (Variable("a") not in variables)


# Structs

def test_do_not_find_struct_members():
    code = """
            struct my_struct {
                int a;
                int b;
                int c;
            };
            """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") and Variable("c") not in variables)


def test_do_not_find_anonymous_struct_members():
    code = """
            struct {
                int a;
                int b;
                int c;
            } my_struct;
            """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") and Variable("c") not in variables)


def test_find_anonymous_struct_declaration():
    code = """
            struct {
                int a;
                int b;
                int c;
            } my_struct;
            """
    variables = find_variables(code)
    assert (Variable("my_struct") in variables)


def test_do_not_find_typedef_struct_members():
    code = """
            typedef struct {
                int a;
                int b;
                int c;
            } my_struct_t;
            """
    variables = find_variables(code)
    assert (Variable("a") and Variable("b") and Variable("c") not in variables)


def test_do_not_find_struct_typedef_name():
    code = """
            typedef struct {
                int a;
                int b;
                int c;
            } my_struct_t;
            """
    variables = find_variables(code)
    assert (Variable("my_struct_t") not in variables)


def test_do_not_find_named_struct_with_typedef_name():
    code = """
            typedef struct my_struct {
                int a;
                int b;
                int c;
            } my_struct_t;
            """
    variables = find_variables(code)
    assert (Variable("my_struct") and Variable("my_struct_t") not in variables)


def test_find_struct_delcared_with_defintion():
    code = """
            struct my_struct {
                int a;
                int b;
                int c;
            } a;
            """
    variables = find_variables(code)
    assert (variables == [Variable("a")])


def test_find_struct_delcared_without_defintion():
    code = """
            struct my_struct_t a;
            """
    variables = find_variables(code)
    assert (variables == [Variable("a")])

# Typedefs

def test_typedefs_not_found():
    code = """
            typedef int my_int_t;
            """
    found = find_variables(code)
    assert (Variable("my_int_t") not in found)


def test_unsigned_typedefs_not_found():
    code = """
            typedef unsigned int my_int_t;
            """
    found = find_variables(code)
    assert (Variable("my_int_t") not in found)


def test_signed_typedefs_not_found():
    code = """
            typedef signed int my_int_t;
            """
    found = find_variables(code)
    assert (Variable("my_int_t") not in found)


def test_typedef_array_not_found():
    code = """
            typedef int my_array_t[10];
            """
    found = find_variables(code)
    assert (Variable("my_array_t") not in found)

# Arrays

def test_array_found():
    code = """
            char a[10];
            """
    found = find_variables(code)
    assert (Variable("a") in found)


def test_array_with_non_numeric_size_arg_found():
    code = """
            char a[MAX_SIZE];
            """
    found = find_variables(code)
    assert (Variable("a") in found)


def test_array_with_initializer_found():
    code = """
            char a[MAX_SIZE] = {1, 2, 3};
            """
    found = find_variables(code)
    assert (Variable("a") in found)


def test_unsized_array_with_initializer_found():
    code = """
            char a[] = {1, 2, 3};
            """
    found = find_variables(code)
    assert (Variable("a") in found)


def test_mutliple_arrays_at_once():
    code = """
            char a[3], b[10];
            """
    found = find_variables(code)
    assert (Variable("a") and Variable("b") in found)


def test_mutliple_arrays_at_once_with_initializer():
    code = """
            char a[3] = {1, 2, 3}, b[10];
            """
    found = find_variables(code)
    assert (Variable("a") and Variable("b") in found)

def test_find_line_number():
    code = """
              int a;
              int b;
            """
    found = find_variables(code)
    assert (next(i for i in found if i == Variable("a")).line_number == 2)
    assert (next(i for i in found if i == Variable("b")).line_number == 3)

# def test_file():
#     code = Path('c/sample.c').read_text()
#     print(code)
#     print(find_variables(code))

# Todo:
#   pointers
#   unions
#   enum
#   capture type, line number
