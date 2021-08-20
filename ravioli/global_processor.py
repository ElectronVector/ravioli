
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    Keyword, Char, SkipTo, nestedExpr,
)


def find_variables(code):

    type_ = Word(alphanums + "_")
    name = Word(alphas, alphanums + "_")
    assignment = Optional(Char("=") + SkipTo(oneOf(", ;")))
    variable_declaration = type_("type")\
        + delimitedList(name("name") + assignment)\
        + ";"
    struct_definition = Keyword("struct") + nestedExpr("{", "}") + name("name")
    variables = []
    for var, start, end in (variable_declaration | struct_definition).scanString(code):
        variables.append(var.name)
    print(variables)
    return variables
