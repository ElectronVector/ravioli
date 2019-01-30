import re
from pprint import pprint

import pytest


def calculate_complexity(code):
    results = {}
    for line in code.splitlines():
        m = re.search(r'\s+(\w+)\s*\(', line)
        if m:
            results[m.group(1)] = 1
    return results


def test_a_function_can_be_parsed():
    code = """
            int a_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_two_functions_can_be_parsed():
    code = """
            int a_function(){}
            int another_function(){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert ('another_function' in results)


def test_a_function_with_arguments_can_be_parsed():
    code = """
            int a_function(int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)


def test_a_function_with_some_whitespace_can_be_parsed():
    code = """
            int a_function (int a){}
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
