import pytest


def calculate_complexity(code):
    return {'a_function': 1}


def test_a_function_can_be_parsed():
    code = """
            int a_function () {
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_two_functions_can_be_parsed():
    code = """
            int a_function () {
            }
            
            int another_function ()
            {
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert ('another_function' in results)

