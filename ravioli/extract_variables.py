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
    "usages": []
}


def extract_declaration(token):
    variables["declarations"].append(Token(token[1]))
    print(f"extracting declaration: {token}")


def extract_assignment(token):
    variables["usages"].append(Token(token[0]))
    print(f"extracting assignment: {token}")


def extract_variables(code):
    type_ = Word(alphanums)
    variable_name = Word(alphas, alphanums + "_")
    declaration = type_ + variable_name + ";"
    declaration.setParseAction(extract_declaration)

    assignment = variable_name + "=" + Word(alphanums) + ";"
    assignment.setParseAction(extract_assignment)

    ZeroOrMore(MatchFirst([assignment, declaration])).parseString(code)

    return variables
