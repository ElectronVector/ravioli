from pathlib import Path

from ravioli.global_processor import find_variables
from ravioli.variable import Variable


def find_variable_in_list(name, list_):
    return next(i for i in list_ if i == Variable(name))


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


class TestStucts:

    def test_do_not_find_struct_members(self):
        code = """
                struct my_struct {
                    int a;
                    int b;
                    int c;
                };
                """
        variables = find_variables(code)
        assert (Variable("a") and Variable("b") and Variable("c") not in variables)

    def test_do_not_find_anonymous_struct_members(self):
        code = """
                struct {
                    int a;
                    int b;
                    int c;
                } my_struct;
                """
        variables = find_variables(code)
        assert (Variable("a") and Variable("b") and Variable("c") not in variables)

    def test_find_anonymous_struct_declaration(self):
        code = """
                struct {
                    int a;
                    int b;
                    int c;
                } my_struct;
                """
        variables = find_variables(code)
        assert (Variable("my_struct") in variables)

    def test_find_anonymous_struct_array_declaration(self):
        code = """
                struct {
                    int a;
                    int b;
                    int c;
                } my_struct[10];
                """
        variables = find_variables(code)
        assert (Variable("my_struct") in variables)

    def test_find_named_struct_array_declaration(self):
        code = """
                struct a_struct {
                    int a;
                    int b;
                    int c;
                } my_struct[10];
                """
        variables = find_variables(code)
        assert (Variable("my_struct") in variables)

    def test_do_not_find_typedef_struct_members(self):
        code = """
                typedef struct {
                    int a;
                    int b;
                    int c;
                } my_struct_t;
                """
        variables = find_variables(code)
        assert (Variable("a") and Variable("b") and Variable("c") not in variables)

    def test_do_not_find_struct_typedef_name(self):
        code = """
                typedef struct {
                    int a;
                    int b;
                    int c;
                } my_struct_t;
                """
        variables = find_variables(code)
        assert (not variables)

    def test_do_not_find_named_struct_with_typedef_name(self):
        code = """
                typedef struct my_struct {
                    int a;
                    int b;
                    int c;
                } my_struct_t;
                """
        variables = find_variables(code)
        assert (not variables)

    def test_find_struct_delcared_with_defintion(self):
        code = """
                struct my_struct {
                    int a;
                    int b;
                    int c;
                } a;
                """
        variables = find_variables(code)
        assert (variables == [Variable("a")])

    def test_find_struct_delcared_without_defintion(self):
        code = """
                struct my_struct_t a;
                """
        variables = find_variables(code)
        assert (variables == [Variable("a")])

    def test_find_struct_with_assignment(self):
        code = """
        struct my_struct {
            int a;
            int b;
            int c;
        } my_struct_var = {1,2,3};
        """
        variables = find_variables(code)
        assert (variables == [Variable("my_struct_var")])

    def test_find_anonymous_struct_with_assignment(self):
        code = """
        struct {
            int a;
            int b;
            int c;
        } my_struct_var = {1,2,3};
        """
        variables = find_variables(code)
        assert (variables == [Variable("my_struct_var")])

    def test_find_typedef_struct_with_assignment(self):
        code = """
        typedef struct {
            int a;
            int b;
            int c;
        } my_struct_t;
        my_struct_t my_struct_var = {1,2,3};
        """
        variables = find_variables(code)
        assert (variables == [Variable("my_struct_var")])

    def test_find_struct_with_assignment(self):
        code = """
        struct my_struct my_struct_var = {1,2,3};
        """
        variables = find_variables(code)
        assert (variables == [Variable("my_struct_var")])


class TestTypedefs:

    def test_typedefs_not_found(self):
        code = """
                typedef int my_int_t;
                """
        found = find_variables(code)
        assert (Variable("my_int_t") not in found)

    def test_unsigned_typedefs_not_found(self):
        code = """
                typedef unsigned int my_int_t;
                """
        found = find_variables(code)
        assert (Variable("my_int_t") not in found)

    def test_signed_typedefs_not_found(self):
        code = """
                typedef signed int my_int_t;
                """
        found = find_variables(code)
        assert (Variable("my_int_t") not in found)

    def test_typedef_array_not_found(self):
        code = """
                typedef int my_array_t[10];
                """
        found = find_variables(code)
        assert (Variable("my_array_t") not in found)


class TestArrays:

    def test_array_found(self):
        code = """
                char a[10];
                """
        found = find_variables(code)
        assert (Variable("a") in found)

    def test_array_with_non_numeric_size_arg_found(self):
        code = """
                char a[MAX_SIZE];
                """
        found = find_variables(code)
        assert (Variable("a") in found)

    def test_array_with_initializer_found(self):
        code = """
                char a[MAX_SIZE] = {1, 2, 3};
                """
        found = find_variables(code)
        assert (Variable("a") in found)

    def test_unsized_array_with_initializer_found(self):
        code = """
                char a[] = {1, 2, 3};
                """
        found = find_variables(code)
        assert (Variable("a") in found)

    def test_mutliple_arrays_at_once(self):
        code = """
                char a[3], b[10];
                """
        found = find_variables(code)
        assert (Variable("a") and Variable("b") in found)

    def test_mutliple_arrays_at_once_with_initializer(self):
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
    variables = find_variables(code)
    assert (find_variable_in_list("a", variables).line_number == 2)
    assert (find_variable_in_list("b", variables).line_number == 3)


def test_file():
    code = Path('c/sample.c').read_text()
    print(code)
    print(find_variables(code))


# Next:
#   pointers
#   unions
#   enum
#   multi-dimension arrays
#   for loop
#   capture type
