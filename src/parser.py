import re
from textnode import *
from block import *

def parse(text):
    root = TextNode(text, TextType.TEXT)
    result = split_nodes_image([root])
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, '**', TextType.BOLD)
    result = split_nodes_delimiter(result, '*', TextType.ITALIC)
    result = split_nodes_delimiter(result, '`', TextType.CODE)
    return result

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

def _split_complex_types(nodes, extractor, text_type):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extractor(node.text)
        if not images:
            result.append(node)
            continue

        for part in images:
            if type(part) is tuple:
                result.append(TextNode(part[0], text_type, part[1]))
                continue
            result.append(TextNode(part))


    return result

def split_nodes_image(nodes):
    return _split_complex_types(nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(nodes):
    return _split_complex_types(nodes, extract_markdown_links, TextType.LINK)

def _extract(text, regexp):
    match = re.search(regexp, text)
    if match is None:
        return None

    result = []
    sub = _extract(match.group(1), regexp)
    if sub:
        result.extend(sub)
    else:
        result.append(match.group(1))
    result.append(match.group(2,3))
    if match.group(4):
        result.append(match.group(4))
    return result

def extract_markdown_images(text):
    return _extract(text, r"(.*)!\[([^\]]*)\]\(([^\)]*)\)(.*)")

def extract_markdown_links(text):
    return _extract(text, r"(.*)\[([^\]]*)\]\(([^\)]*)\)(.*)")

def markdown_to_blocks(text):
    rows = text.split("\n")
    result = []
    block = []
    in_block = False
    for row in rows:
        stripped = row.strip()
        if not stripped: # empty row
            if in_block:
                result.append("\n".join(block))
                block = []
                in_block = False
        else:
            block.append(stripped)
            in_block = True

    if block:
        result.append("\n".join(block)) # add last block as well
    return result

def block_to_block_type(text):
    if re.match(r"#{1,6} .*", text):
        return BlockType.HEADING

    if re.match(r"[`]{3}.*[`]{3}", text, re.DOTALL):
        return BlockType.CODE
    
    # print("\n\n>>>",text,"<<<")
    lines = text.split("\n")
    quote = True
    unordered_list = True
    ordered_list = True

    for i, line in enumerate(lines):
        if quote and not re.match(r">.*", line):
            quote = False
        if unordered_list and not re.match(r"[*-] .*", line):
            unordered_list = False
        if ordered_list:
            match = re.match(r"(\d+)\. .*", line)
            if not match or match.group(1) != f"{i+1}":
                ordered_list = False
        if not quote and not unordered_list and not ordered_list:
            break

    if quote:
        return BlockType.QUOTE
    
    if unordered_list:
        return BlockType.UNORDERED_LIST
    
    if ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
