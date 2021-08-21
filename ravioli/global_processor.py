
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    Keyword, Char, SkipTo, nestedExpr, MatchFirst,
)


def find_variables(code):

    type_ = Word(alphanums + "_")
    name = Word(alphas, alphanums + "_")
    assignment = Optional(Char("=") + SkipTo(oneOf(", ;")))
    block = nestedExpr("{", "}")

    variable_declaration = type_("type")\
        + delimitedList(name("name") + assignment)\
        + ";"
    struct_definition = Keyword("struct") + Optional(name) + block + Optional(type_) + ";"

    statements = [
        variable_declaration,
        struct_definition
    ]

    variables = []
    for var, start, end in MatchFirst(statements).scanString(code):
        variables.append(var.name)
    print(variables)
    return variables
