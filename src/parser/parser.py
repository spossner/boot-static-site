import re
from parser.textnode import TextNode, TextType
from html.parentnode import ParentNode
from html.leafnode import LeafNode
from md.block import BlockType

def textnode2htmlnode(data):
    if type(data) is list:
        return map(lambda n: n.to_html_node(), data)
    return data.to_html_node()

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = list(textnode2htmlnode(parse(block)))
                nodes.append(ParentNode(f"p", children))
            case BlockType.HEADING:
                sub_heading = block.split("\n")
                for b in sub_heading:
                    prefix, inner = b.split(" ", 1)
                    children = textnode2htmlnode(parse(inner))
                    nodes.append(ParentNode(f"h{len(prefix)}", children))
            case BlockType.CODE:
                nodes.append(ParentNode("pre", [LeafNode(f"code", block[3:-3].strip())]))
            case BlockType.QUOTE:
                rows = map(lambda row: row[1:].strip(), block.split("\n"))
                children = list(map(lambda row: ParentNode("p", textnode2htmlnode(parse(row))), rows))
                nodes.append(ParentNode("blockquote", children, slim=True))
            case BlockType.UNORDERED_LIST:
                rows = map(lambda row: row.split(" ",1)[1].strip(), block.split("\n"))
                children = list(map(lambda row: ParentNode("li", textnode2htmlnode(parse(row))), rows))
                nodes.append(ParentNode("ul", children))
            case BlockType.ORDERED_LIST:
                rows = map(lambda row: row.split(" ",1)[1].strip(), block.split("\n"))
                children = list(map(lambda row: ParentNode("li", textnode2htmlnode(parse(row))), rows))
                nodes.append(ParentNode("ol", children))
            case _:
                print("huch", block_type)
    return ParentNode("div", nodes)



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
    in_code = False
    for row in rows:
        stripped = row.strip()
        if not stripped: # empty row
            if in_code:
                block.append(row)
            elif in_block:
                result.append("\n".join(block))
                block = []
                in_block = False
        else:
            block.append(row if in_code else stripped)
            in_block = True
            if in_code:
                if stripped.endswith("```"):
                    result.append("\n".join(block))
                    block = []
                    in_block = False
                    in_code = False
            else:
                if stripped.startswith("```"):
                    in_code = True

    if block:
        result.append("\n".join(block)) # add last block as well
    return result

def block_to_block_type(text):
    if re.match(r"#{1,6} .*", text):
        return BlockType.HEADING

    if re.match(r"```.*```", text, re.DOTALL):
        return BlockType.CODE
    
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

def extract_title(markdown):
    match = re.search(r"^\s*#\s+(.*)", markdown, re.MULTILINE)
    if not match:
        raise Exception("no title found (# <title>)")
    return match.group(1).strip()