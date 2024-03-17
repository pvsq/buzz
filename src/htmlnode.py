class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError()


    def props_to_html(self):
        html_attrs = ""

        if not self.props:
            return html_attrs

        for prop in self.props:
            html_attrs += f' {prop}="{self.props[prop]}"'
        return html_attrs


    def __repr__(self):
        return f"""HTMLNode: (
            tag = {self.tag},
            value = {self.value},
            children = {self.children},
            props = {self.props}
        )"""

