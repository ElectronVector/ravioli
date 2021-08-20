from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    Keyword, Char,
)


def find_variables(code):
    type = Word(alphanums + "_")
    name = Word(alphas, alphanums + "_")
    variable_declaration = type("type") + delimitedList(name("name")) + oneOf("; =")
    variables = []
    for var, start, end in variable_declaration.scanString(code):
        variables.append(var.name)
    return variables
