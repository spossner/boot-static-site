from textnode import *

def split_nodes_delimiter(nodes, delimiter, text_type):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            result.append(node)
            continue

        for i in range(len(parts)):
            if not parts[i]:
                continue # skip empty parts

            if i % 2 == 0:
                result.append(TextNode(parts[i], TextType.TEXT))
            else:
                result.append(TextNode(parts[i], text_type))
    return result
