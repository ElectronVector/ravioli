
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    Keyword, Char, SkipTo,
)


def find_variables(code):
    type_ = Word(alphanums + "_")
    name = Word(alphas, alphanums + "_")
    variable_declaration = type_("type")\
        + delimitedList(name("name") + Optional(Char("=") + SkipTo(oneOf(", ;"))))\
        + oneOf("; =")
    variables = []
    for var, start, end in variable_declaration.scanString(code):
        variables.append(var.name)
    return variables
