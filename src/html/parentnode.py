import re
from html.htmlnode import HTMLNode

def unwrap(html):
    return re.sub(r"<(\w+)>(.*)</\1>", "\\2", html)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None, slim=False):
        super().__init__(tag, None, children, props)
        self.slim = slim

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        
        if not self.children:
            raise ValueError("missing children")

        if self.slim:
            inner = self.children[0].to_html()
            return self.wrap(unwrap(inner))

        inner = []
        for child in self.children:
            inner.append(child.to_html())
        return self.wrap("".join(inner))
        