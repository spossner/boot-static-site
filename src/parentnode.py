from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        
        if not self.children:
            raise ValueError("missing children")
        
        inner = []
        for child in self.children:
            inner.append(child.to_html())
        return self.wrap_tag("".join(inner))
        