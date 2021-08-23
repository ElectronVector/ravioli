
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    Keyword, Char, SkipTo, nestedExpr, MatchFirst, printables,
)

from ravioli.variable import Variable


def find_variables(code):

    type_ = Word(alphanums + "_")
    indentifier = Word(alphas, alphanums + "_")
    assignment = Char("=") + Word(printables + " ", excludeChars=",;")
    block = nestedExpr("{", "}")
    array = "[" + Word(alphanums + "_") + "]"

    decl_single = indentifier("name") + Optional(assignment)
    decl_array = indentifier("name") + array
    decl_array_with_assignment = indentifier("name") + array + "=" + block

    variable_declaration = type_("type")\
        + delimitedList(decl_array_with_assignment | decl_array | decl_single)\
        + ";"

    struct = Keyword("struct") + Optional(indentifier) + block
    struct_definition = struct + Optional(indentifier("name")) + ";"
    struct_typedef = Keyword("typedef") + struct + Optional(type_) + ";"

    sign = Keyword("unsigned") | Keyword("signed")
    typedef = Keyword("typedef") + Optional(sign) + type_ + indentifier + ";"

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
