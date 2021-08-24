
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

    array_index = "[" + Optional(Word(alphanums + "_")) + "]"

    identifier = Word(alphas, alphanums + "_")
    variable_name = identifier("name") + Optional(array_index)
    struct_type = Word(alphas, alphanums + "_")
    typedef_type = Word(alphas, alphanums + "_")

    block = nestedExpr("{", "}")

    assignment_simple = "=" + Word(printables + " ", excludeChars=",;")
    assignment_block = "=" + block

    variable_declaration = variable_name + Optional(assignment_block | assignment_simple)

    variable_declaration_list = type_("type") + delimitedList(variable_declaration) + ";"

    struct_definition = Keyword("struct") + Optional(struct_type) + block + Optional(variable_name) + ";"
    struct_typedef = Keyword("typedef") + Keyword("struct") + Optional(struct_type) + block + typedef_type + ";"

    typedef = Keyword("typedef") + type_ + typedef_type + Optional(array_index) + ";"

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
