
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
    struct_typedef = Keyword("typedef") + Keyword("struct") + Optional(name) + block + Optional(type_) + ";"
    struct_definition = Keyword("struct") + Optional(name) + block + Optional(name("name")) + ";"

    statements = [
        variable_declaration,
        struct_definition,
        struct_typedef
    ]

    variables = []
    for var, start, end in MatchFirst(statements).scanString(code):
        variables.append(var.name)
    print(variables)
    return variables
