from enum import Enum
from html.leafnode import LeafNode

# class syntax
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text_type == other.text_type and self.url == other.url and self.text == other.text

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                if not self.url:
                    raise ValueError("missing url in link text node")
                return LeafNode("a", self.text, {"href":self.url})
            case TextType.IMAGE:
                if not self.url:
                    raise ValueError("missing url in image text node")
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("unknwon text_type "+self.text_type)

