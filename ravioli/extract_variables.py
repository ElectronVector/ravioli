from pyparsing import (
    Word,
    alphas,
    alphanums,
    Optional,
    delimitedList,
    lineno,
    Keyword, nestedExpr, MatchFirst, printables, ZeroOrMore,
)


class Token:
    def __init__(self, name):
        self.name = name


variables = {
    "declarations": [],
    "usages": [],
    "functions": []
}


def extract_declaration(token):
    variables["declarations"].append(Token(token[1]))
    print(f"extracting declaration: {token}")


def extract_assignment(token):
    variables["usages"].append(Token(token[0]))
    print(f"extracting assignment: {token}")


def extract_function(token):
    variables["functions"].append(Token(token[1]))
    print(f"extracting function: {token}")


def extract_variables(code):
    type_ = Word(alphanums)
    variable_name = Word(alphas, alphanums + "_")
    declaration = type_ + variable_name + ";"
    declaration.setParseAction(extract_declaration)

    assignment = variable_name + "=" + Word(alphanums) + ";"
    assignment.setParseAction(extract_assignment)

    function = type_ + variable_name + "(" + ... + ")" + nestedExpr("{", "}")
    function.setParseAction(extract_function)

    ZeroOrMore(MatchFirst([assignment, declaration, function])).parseString(code)

    return variables
