import re


def test_a_function_body_is_removed():
    code = """
            void a_function(){
                int a = 0;
                int b = 0;
            }
            """
    expected = """
            void a_function(){}
            """
    stripped = strip_blocks(code)
    assert(stripped == expected)


def strip_blocks(code):
    return re.sub(r'{.*}', '{}', code, flags=re.DOTALL)