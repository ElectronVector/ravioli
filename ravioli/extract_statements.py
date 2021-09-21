
class Block:
    def __init__(self, title, children=None):
        self.title = title
        self.children = children

    def __repr__(self):
        return f"Block({self.title}, {self.children})"

    def __eq__(self, other):
        return self.title == other.title and self.children == other.children

    def append(self, item):
        if not self.children:
            self.children = []
        self.children.append(item)


def extract_name_and_parameters(s):
    """
    Parse a function (block) name and its parameters by parsing before and inside the parentheses.
    :param s: The string to extract the block name and parameters from.
    :return: A tuple containing the 1) name of the block and 2) an array of block parameters.
    """
    param_start = s.find("(")
    param_end = s.rfind(")")
    name = clean_up_whitespace(s[:param_start])
    param_string = s[param_start+1:param_end]
    # Extract comma-separated paramaters separately.
    params = [clean_up_whitespace(p) for p in param_string.split(",") if p]
    return name, params


def extract_statements(code):
    parse_tree = []
    nest_levels = [parse_tree]
    temp = ""
    for c in code:
        if c == ";":
            # Save the current statement.
            nest_levels[-1].append(clean_up_whitespace(temp))
            temp = ""
        elif c == "{":
            title, params = extract_name_and_parameters(temp)
            title = clean_up_whitespace(title)
            new_block = Block(title)
            if params:
                for p in params:
                    new_block.append(p)
            nest_levels[-1].append(new_block)
            nest_levels.append(new_block)
            temp = ""
        elif c == "}":
            # This is the end of a block. Remove this nest level as we aren't going to save anything here any more.
            nest_levels.pop()
            temp = ""
        else:
            temp += c

    return parse_tree


def clean_up_whitespace(s):
    return " ".join(s.strip().split())

