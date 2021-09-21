from ravioli.extract_statements import extract_statements, Block


# TODO
# Refactor extract_declarations_and_usages.py:
#   - Remove extract_undefined_usages - put this somewhere where we are going to process a real file.
#   - Rename.
# Try actually counting globals in some sample code.
# Parse for and do-while loops.


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


def test_block():
    code = """
    function_def() {
    }
    """
    assert extract_statements(code) == [Block("function_def")]


def test_block_with_a_statement():
    code = """
    function_def() {
        int a;
    }
    """
    assert extract_statements(code) == [Block("function_def", ["int a"])]


def test_block_with_multiple_statements():
    code = """
    function_def() {
        int a;
        a = b + 2;
    }
    """
    assert extract_statements(code) == [Block("function_def", ["int a", "a = b + 2"])]


def test_multiple_nested_blocks():
    code = """
    function_def() {
        int a;
        a = b + 2;
        if() {
            c += 1;
        }
        a++;
    }
    """
    assert extract_statements(code) == [
        Block("function_def", [
            "int a",
            "a = b + 2",
            Block("if", [
                "c += 1"
            ]),
            "a++",
        ])]


def test_parameter_extracted_from_block():
    code = """
    function_def(int x) {
        int a;
    }
    """
    assert extract_statements(code) == [Block("function_def", ["int x", "int a"])]


def test_multiple_parameters_extracted_from_block():
    code = """
    function_def(int x, unsigned int y) {
        int a;
    }
    """
    assert extract_statements(code) == [Block("function_def", ["int x", "unsigned int y", "int a"])]

# TODO: Test getting line numbers from statements.
