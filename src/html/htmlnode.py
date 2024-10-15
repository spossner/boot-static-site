import re


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return None
        result = ""
        for key, value in self.props.items():
            result = f'{result} {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def wrap(self, inner):
        return f'<{self.tag}{"" if self.props is None else self.props_to_html()}>{inner}</{self.tag}>'