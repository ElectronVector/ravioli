
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Combine,
    oneOf,
    Optional,
    delimitedList,
    Group,
    lineno,
    Keyword, Char, SkipTo, nestedExpr, MatchFirst, printables,
)

from ravioli.variable import Variable


def find_variables(code):
    sign = Keyword("unsigned") | Keyword("signed")
    type_ = Optional(sign) + Word(alphanums + "_")
    identifier = Word(alphas, alphanums + "_")
    assignment = Char("=") + Word(printables + " ", excludeChars=",;")
    block = nestedExpr("{", "}")
    array = "[" + Optional(Word(alphanums + "_")) + "]"

    decl_single = identifier("name") + Optional(assignment)
    decl_array = identifier("name") + array + Optional("=" + block)

    variable_declaration = type_("type")\
        + delimitedList(decl_array | decl_single)\
        + ";"

    struct = Keyword("struct") + Optional(identifier) + block
    struct_definition = struct + Optional(identifier("name")) + ";"

    typedef = Keyword("typedef") + (struct | type_) + identifier + Optional(array) + ";"

    statements = [
        typedef,
        variable_declaration,
        struct_definition,
    ]

    variables = []
    for var, start, end in MatchFirst(statements).scanString(code):
        variables.append(Variable(var.name, line_number=lineno(start, code)))
    print(variables)
    return variables
