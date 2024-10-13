class HTMLNode:
    def __init__(self, value = None, tag = None, children = None, props = None):
        self.value = value
        self.tag = tag
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
        return f"HTMLNode({self.value}, {self.tag}, [{self.children}], {self.props})"
