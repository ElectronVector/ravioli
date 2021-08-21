
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

from ravioli.variable import Variable


def find_variables(code):

    type_ = Word(alphanums + "_")
    name = Word(alphas, alphanums + "_")
    assignment = Optional(Char("=") + SkipTo(oneOf(", ;")))
    block = nestedExpr("{", "}")

    variable_declaration = type_("type")\
        + delimitedList(name("name") + assignment)\
        + Optional("[" + Word(alphanums + "_") + "]")\
        + ";"

    struct = Keyword("struct") + Optional(name) + block
    struct_definition = struct + Optional(name("name")) + ";"
    struct_typedef = Keyword("typedef") + struct + Optional(type_) + ";"

    sign = Keyword("unsigned") | Keyword("signed")
    typedef = Keyword("typedef") + Optional(sign) + type_ + name + ";"

    statements = [
        typedef,
        variable_declaration,
        struct_definition,
        struct_typedef
    ]

    variables = []
    for var, start, end in MatchFirst(statements).scanString(code):
        variables.append(Variable(var.name))
    print(variables)
    return variables
