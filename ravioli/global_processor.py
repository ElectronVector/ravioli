
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

    struct_definition = Keyword("struct") + Optional(identifier) + block + Optional(identifier("name")) + ";"
    struct_typedef = Keyword("typedef") + Keyword("struct") + Optional(identifier) + block + identifier + ";"

    typedef = Keyword("typedef") + type_ + identifier + Optional(array) + ";"

    statements = [
        variable_declaration,
        struct_typedef,
        struct_definition,
        typedef
    ]

    variables = []
    for var, start, end in MatchFirst(statements).scanString(code):
        if var.name:
            variables.append(Variable(var.name, line_number=lineno(end, code)))
    print(variables)
    return variables
