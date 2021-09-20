
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
            title = clean_up_whitespace(temp)
            title = title.replace("(", "")
            title = title.replace(")", "")
            new_block = Block(title)
            nest_levels.append(new_block)
            parse_tree.append(new_block)
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

