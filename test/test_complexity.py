import re
from pprint import pprint

import pytest


def calculate_complexity(code):
    results = {}
    for line in code.splitlines():
        m = re.search(r'\s+(\w+)\s*\(.*\)\s*{', line)
        if m:
            name = m.group(1)
            if name != 'if':
                results[name] = 1
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


def test_a_function_with_an_if_can_be_parsed():
    code = """
            int a_function (int a){
                if (a > 5) {
                    return 0;
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)


def test_a_function_which_calls_another_function_can_be_parsed():
    code = """
            int a_function (int a){
                if (a > 5) {
                    call_another_function(a + 1);
                }
                return 1;
            }
            """
    results = calculate_complexity(code)
    assert ('a_function' in results)
    assert (len(results) == 1)
