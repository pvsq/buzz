from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag, None, children, props)


    def to_html(self):
        if not self.tag:
            raise ValueError("A tag must be specified for the parent node.")

        if not self.children:
            raise ValueError("A parent node must have at least one child node.")

        start_element = f"<{self.tag}{super().props_to_html()}>"
        end_element = f"</{self.tag}>"
        inner_html = ""

        for node in self.children:
            inner_html += node.to_html()

        return f"{start_element}{inner_html}{end_element}"

