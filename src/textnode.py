from leafnode import LeafNode

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type

        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


    def text_node_to_html_node(self):
        if self.text_type == "text":
            return LeafNode(None, self.text)
        if self.text_type == "bold":
            return LeafNode("b", self.text)
        if self.text_type == "italic":
            return LeafNode("i", self.text)
        if self.text_type == "code":
            return LeafNode("code", self.text)
        if self.text_type == "link":
            return LeafNode("a", self.text, { "href": self.url })
        if self.text_type == "image":
            return LeafNode("img", "", { "src": self.url, "alt": self.text })

        raise ValueError(f"Invalid text type {self.text_type}")

