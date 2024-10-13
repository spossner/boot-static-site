from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("missing value")
        
        if not self.tag:
            return self.value
        
        return self.wrap_tag(self.value)
