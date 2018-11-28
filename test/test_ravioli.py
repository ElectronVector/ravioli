import pytest
import ravioli


@pytest.fixture
def results():
    return ravioli.run("c/foo.c")


def test_globals_are_counted(results):
    assert (results["global_count"] == 2)


def test_a_function_with_no_decisions_returns_complexity_1(results):
    assert (results["complexity"]["no_decisions"] == 1)


def test_a_function_with_one_decision_returns_complexity_2(results):
    assert (results["complexity"]["if_else"] == 2)


def test_a_function_with_an_else_if_returns_correct_complexity(results):
    assert (3 == results["complexity"]["else_if"])


def test_a_function_with_a_nested_if_returns_correct_complexity(results):
    assert (results["complexity"]["nested_if"] == 3)


def test_a_function_with_a_nested_else_if_returns_correct_complexity(results):
    assert (results["complexity"]["nested_else_if"] == 4)


def test_a_function_with_a_nested_else_if_and_extra_statements_returns_correct_complexity(results):
    assert (results["complexity"]["nested_else_if_with_extra_statements"] == 4)


# This tests for "strict cyclomatic complexity" (SCC), also called CC2.
def test_a_function_with_a_compound_if_statement_includes_it_in_complexity(results):
    assert (results["complexity"]["compound_if"] == 3)


def test_a_function_with_a_compound_if_or_statement_includes_it_in_complexity(results):
    assert (results["complexity"]["compound_if_or"] == 3)


def test_a_function_with_multiple_compound_if_statements_includes_them_in_complexity(results):
    assert (results["complexity"]["multiple_compound_if"] == 4)


def test_a_while_loop_is_counted(results):
    assert (results["complexity"]["while_loop"] == 2)


def test_a_do_while_loop_is_counted(results):
    assert (results["complexity"]["do_while_loop"] == 2)


def test_a_for_loop_is_counted(results):
    assert (results["complexity"]["for_loop"] == 2)


def test_a_while_loop_is_counted_with_a_compound_conditional(results):
    assert (results["complexity"]["compound_while_loop"] == 3)


def test_nested_for_loops(results):
    assert (results["complexity"]["nested_for_loops"] == 3)


def test_nested_loops_with_compound_conditional(results):
        assert (results["complexity"]["nested_loops_with_compound_conditional"] == 4)


def test_a_complicated_example(results):
    assert (11 == results["complexity"]["a_complicated_example"])


def test_a_switch_statement(results):
    assert (3 == results["complexity"]["switch_statement"])
