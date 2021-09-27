from ravioli.extract_statements import extract_statements, Block, Statement, extract_name_and_parameters


# TODO
# Refactor extract_declarations_and_usages.py:
#   - Remove extract_undefined_usages - put this somewhere where we are going to process a real file.
#   - Rename.
# Try actually counting globals in some sample code.
# Parse for and do-while loops.


def test_single_statement():
    code = """  int a;
                """
    assert extract_statements(code) == [Statement("int a", 1)]


def test_multiple_statements():
    code = """  int a; int b;
                int c;
                """
    assert extract_statements(code) == [Statement("int a", 1), Statement("int b", 1), Statement("int c", 2)]


def test_multiple_statements_with_extra_whitespace():
    code = """  int   a; int b =   0;
                int
                    c;
                """
    assert extract_statements(code) == [Statement("int a", 1), Statement("int b = 0", 1), Statement("int c", 2)]


def test_block():
    code = """  function_def() {
                }
                """
    assert extract_statements(code) == [Block("function_def", 1)]


def test_block_with_a_statement():
    code = """  function_def() {
                    int a;
                }
                """
    assert extract_statements(code) == [Block("function_def", 1, [Statement("int a", 2)])]


def test_block_with_multiple_statements():
    code = """  function_def() {
                    int a;
                    a = b + 2;
                }
                """
    assert extract_statements(code) == [Block("function_def", 1, [Statement("int a", 2), Statement("a = b + 2", 3)])]


def test_multiple_nested_blocks():
    code = """  function_def() {
                int a;
                a = b + 2;
                if() {
                    c += 1;
                }
                a++;
            }
            """
    assert extract_statements(code) == [
        Block("function_def", 1, [
            Statement("int a", 2),
            Statement("a = b + 2", 3),
            Block("if", 4, [
                Statement("c += 1", 5)
            ]),
            Statement("a++", 7),
        ])]


def test_parameter_extracted_from_block():
    code = """  function_def(int x) {
                    int a;
                }
                """
    assert extract_statements(code) == [Block("function_def", 1, [Statement("int x", 1), Statement("int a", 2)])]


def test_multiple_parameters_extracted_from_block():
    code = """  function_def(int x, unsigned int y) {
                    int a;
                }
                """
    assert extract_statements(code) == [Block("function_def", 1, [Statement("int x", 1), Statement("unsigned int y", 1), Statement("int a", 2)])]


def test_extract_correct_name_from_struct_def():
    code = "struct my_struct"
    assert extract_name_and_parameters(code) == ("struct my_struct", None)


def test_trailing_content_extracted_with_block():
    code = """  struct my_struct {
                    int a;
                    int b;
                } a;
                """
    print(extract_statements(code))
    assert extract_statements(code) == [Block("struct my_struct", 1, [Statement("int a", 2), Statement("int b", 3)], "a")]


# def test_trailing_content_extracted_with_block_inside_function():
#     code = """  function_def() {
#                     struct my_struct {
#                         int a;
#                         int b;
#                     } a;
#                 }
#                 """
#     assert extract_statements(code) == [Block(
#                                             "function_def",
#                                             1,
#                                             [Block("struct my_struct", 2, [Statement("int a", 3), Statement("int b", 4)])],
#                                         )]


# TODO
# - Test line numbers of function parameters split over multiple lines.
