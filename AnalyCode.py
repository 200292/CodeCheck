from tree_sitter import Language, Parser, Node

C_LANGUAGE = Language('build/my-languages.so', 'c')

def get_node(filepath) -> Node:
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    parser = Parser()
    parser.set_language(C_LANGUAGE)
    tree = parser.parse(bytes(content, 'utf-8'))
    root_node = tree.root_node
    return root_node



