
from pyparsing import (
    Word,
    alphas,
    alphanums,
    Optional,
    delimitedList,
    lineno,
    Keyword, Char, nestedExpr, MatchFirst, printables,
)

from ravioli.variable import Variable


def find_variables(code):
    sign = Keyword("unsigned") | Keyword("signed")
    type_ = Optional(sign) + Word(alphanums + "_")
    identifier = Word(alphas, alphanums + "_")
    block = nestedExpr("{", "}")
    array = "[" + Optional(Word(alphanums + "_")) + "]"

    assignment_simple = "=" + Word(printables + " ", excludeChars=",;")
    assignment_block = "=" + block

    variable_declaration = identifier("name") + Optional(array) + Optional(assignment_block | assignment_simple)

    variable_declaration_list = type_("type")\
        + delimitedList(variable_declaration)\
        + ";"

    struct_definition = Keyword("struct") + Optional(identifier) + block + Optional(identifier("name")) + Optional(array) + ";"
    struct_typedef = Keyword("typedef") + Keyword("struct") + Optional(identifier) + block + identifier + ";"

    typedef = Keyword("typedef") + type_ + identifier + Optional(array) + ";"

    statements = [
        variable_declaration_list,
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
