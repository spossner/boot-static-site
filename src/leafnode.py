from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(value, tag, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("missing value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{"" if self.props is None else self.props_to_html()}>{self.value}</{self.tag}>"
