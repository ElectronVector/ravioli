from ravioli.extract_statements import extract_statements

# TODO
# Update statement extractor to extract blocks.
# Parse block names.
# Parse block arguments as statements that belong to the block.


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