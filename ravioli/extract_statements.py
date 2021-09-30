
class Block:
    def __init__(self, title, line_number, children=None, trailing_content=None):
        self.title = title
        self.line_number = line_number
        self.children = children
        self.trailing_content = trailing_content

    def __repr__(self):
        r = f"Block({self.title}, {self.line_number}, {self.children}"
        if self.trailing_content:
            r += f", {self.trailing_content}"
        r += ")"
        return r

    def __eq__(self, other):
        return (self.title == other.title
                and self.line_number == other.line_number
                and self.children == other.children)

    def append(self, item):
        if not self.children:
            self.children = []
        self.children.append(item)


class Statement:
    def __init__(self, text, line_number):
        self.text = text
        self.line_number = line_number

    def __repr__(self):
        return f"Statement({self.text}, {self.line_number})"

    def __eq__(self, other):
        return (self.text == other.text
                and self.line_number == other.line_number)


def extract_name_and_parameters(s):
    """
    Parse a function (block) name and its parameters by parsing before and inside the parentheses.
    :param s: The string to extract the block name and parameters from.
    :return: A tuple containing the 1) name of the block and 2) an array of block parameters.
    """
    params = None
    param_start = s.find("(")
    param_end = s.rfind(")")
    if param_start == -1 or param_end == -1:
        # We didn't find both parentheses here -- thus there are no parameters.
        name = clean_up_whitespace(s)
    else:
        name = clean_up_whitespace(s[:param_start])
        param_string = s[param_start + 1:param_end]
        # Extract comma-separated parameters separately.
        params = [clean_up_whitespace(p) for p in param_string.split(",") if p]

    return name, params


def extract_statements(code):
    line_number = 1
    parse_tree = []
    nest_levels = [parse_tree]
    temp = ""
    last_block = None
    for c in code:
        if c == ";":
            # Save the current statement.
            text = clean_up_whitespace(temp)
            newlines_in_text = temp.count("\n")
            # If we just finished parsing a struct block, add the next semi-colon delimited statement as trailing
            # content to the previous block.
            if last_block and "struct" in last_block.title:
                last_block.trailing_context = text
            else:
                nest_levels[-1].append(Statement(text, line_number - newlines_in_text))
            temp = ""
            last_block = None
        elif c == "{":
            title, params = extract_name_and_parameters(temp)
            title = clean_up_whitespace(title)
            new_block = Block(title, line_number)
            if params:
                for p in params:
                    new_block.append(Statement(p, line_number))
            nest_levels[-1].append(new_block)
            nest_levels.append(new_block)
            temp = ""
        elif c == "}":
            last_block = nest_levels[-1]
            # This is the end of a block. Remove this nest level as we aren't going to save anything here any more.
            nest_levels.pop()
            temp = ""
        elif c == "\n":
            line_number += 1
            if temp:
                # Only capture the new line if we haven't just completed a statement.
                temp += c
        else:
            temp += c

    return parse_tree


def clean_up_whitespace(s):
    return " ".join(s.strip().split())
