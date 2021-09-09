from pathlib import Path

from ravioli.extract_variables import extract_variables

def names_of(list_):
    return [x.name for x in list_]

def test_find_declaration():
    code = """int a;
           """
    v = extract_variables(code)
    assert ("a" in names_of(v["declarations"]))


def test_find_multiple_declarations():
    code = """int a;
              int b;
           """
    v = extract_variables(code)
    assert ("a" and "b" in names_of(v["declarations"]))


def test_find_multiple_declarations_on_same_line():
    code = """int a; int b;
           """
    v = extract_variables(code)
    assert ("a" and "b" in names_of(v["declarations"]))


def test_find_usage():
    code = """a = 0;
           """
    v = extract_variables(code)
    assert ("a" in names_of(v["usages"]))


def test_find_function_definition():
    code = """void a_function(int a, int b) {
              }
           """
    v = extract_variables(code)
    assert ("a_function" in names_of(v["functions"]))


def test_dont_find_function_prototype():
    code = """int a_function(int a, int b);
            """
    v = extract_variables(code)
    assert ("a_function" not in names_of(v["functions"]))


def test_find_a_function_and_variable_declarations():
    code = """
    int a; int b;
    void a_function(int a, int b) {
    }
    int c;
    """
    v = extract_variables(code)
    assert ("a_function" in names_of(v["functions"]))
    assert ("a" and "b" and "c" in names_of(v["declarations"]))
