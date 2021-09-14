from ravioli.globals import extract_statements, extract_undefined_usages


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