from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        self.value = value
        self.tag = tag
        self.props = props
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("A value is required for HTML leaf node")

        if not self.tag:
            return str(self.value)

        html_attrs = super().props_to_html()
        return f"<{self.tag}{html_attrs}>{self.value.strip(' \n\t')}</{self.tag}>"

    def __repr__(self):
        return f"""LeafNode: (
            tag = {self.tag},
            value = {self.value},
            props = {self.props}
        )"""

