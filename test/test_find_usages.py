from ravioli.global_processor import find_usages


def test_find_an_assignment():
    code = """
            a_variable = 1;
            """
    u = find_usages(code)
    assert ("a_variable" in u)


def test_find_an_assignment_from_variable():
    code = """
            a_variable = another_variable;
            """
    u = find_usages(code)
    assert ("a_variable" and "another_variable" in u)


def test_dont_find_a_declaration():
    code = """
            int a_declaration = another_variable;
            """
    u = find_usages(code)
    assert ("a_declaration" not in u)
    assert ("another_variable" in u)
