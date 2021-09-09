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


def test_find_usage():
    code = """a = 0;
           """
    v = extract_variables(code)
    usage_names = [u.name for u in v["usages"]]
    assert ("a" in usage_names)

