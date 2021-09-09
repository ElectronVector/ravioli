from pathlib import Path

from ravioli.extract_variables import extract_variables


def test_find_declaration():
    code = """int a;
           """
    v = extract_variables(code)
    decl_names = [d.name for d in v["declarations"]]
    assert ("a" in decl_names)


def test_find_multiple_declarations():
    code = """int a;
              int b;
           """
    v = extract_variables(code)
    decl_names = [d.name for d in v["declarations"]]
    assert ("a" and "b" in decl_names)


def test_find_multiple_declarations_on_same_line():
    code = """int a; int b;
           """
    v = extract_variables(code)
    decl_names = [d.name for d in v["declarations"]]
    assert ("a" and "b" in decl_names)


def test_find_usage():
    code = """a = 0;
           """
    v = extract_variables(code)
    usage_names = [u.name for u in v["usages"]]
    assert ("a" in usage_names)


def test_find_function_definition():
    code = """void a_function(int a, int b) {
              }
           """
    v = extract_variables(code)
    function_names = [f.name for f in v["functions"]]
    assert ("a_function" in function_names)


def test_dont_find_function_prototype():
    code = """int a_function(int a, int b);
            """
    v = extract_variables(code)
    function_names = [f.name for f in v["functions"]]
    assert ("a_function" not in function_names)
