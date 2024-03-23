import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html_node
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)


    def test_eq_whenDifferentUrl(self):
        node = TextNode("This is a text node", text_type_bold, "http://localhost:8008")
        node2 = TextNode("This is a text node", text_type_bold, "http://localhost:8080")
        self.assertNotEqual(node, node2)


    def test_eq_whenDifferentTextType(self):
        node = TextNode("This is a text node", text_type_bold, "http://localhost:8080")
        node2 = TextNode("This is a text node", text_type_italic, "http://localhost:8080")
        self.assertNotEqual(node, node2)


    def test_eq_whenDifferentText(self):
        node = TextNode("This is a text node", text_type_bold, "http://localhost:8080")
        node2 = TextNode("This is a text mode", text_type_bold, "http://localhost:8080")
        self.assertNotEqual(node, node2)


    def test_repr(self):
        expected = "TextNode(This is a text node, bold, http://localhost:8080)"
        node = TextNode("This is a text node", text_type_bold, "http://localhost:8080")
        self.assertEqual(expected, str(node))


    def test_textNodeToHTMLNode_whenTextTypeIsInvalid(self):
        node = TextNode("This text glows.", "glow", "http://localhost:8000")
        self.assertRaises(ValueError, text_node_to_html_node, node)


    def test_textNodeToHTMLNode_whenTextTypeIsText(self):
        text = "Raw text. No need to mark up this paragraph."
        node = TextNode(text, text_type_text)
        expected = text
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsTextAndHasUrl(self):
        text = "Raw text. No need to mark up this paragraph."
        node = TextNode(text, text_type_text, "https://www.example.com")
        expected = text
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsBold(self):
        text = "This line makes some bold claims"
        node = TextNode(text, text_type_bold)
        expected = f"<b>{text}</b>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsItalic(self):
        text = "The information contained in this document is strictly confidential."
        node = TextNode(text, text_type_italic)
        expected = f"<i>{text}</i>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsCode(self):
        text = 'title = "why html development sucks"; print(doc[::-1])'
        node = TextNode(text, text_type_code)
        expected = f"<code>{text}</code>"
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsImage(self):
        alt = "Picture of a valley with a river flowing in the foreground and snow-capped mountains in the distance."
        src = "https://example.com/valley.jpg"
        node = TextNode(alt, text_type_image, src)
        expected = f'<img src="{src}" alt="{alt}"></img>'
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


    def test_textNodeToHTMLNode_whenTextTypeIsLink(self):
        anchortext = "Click here to learn more."
        href_link = "https://www.example.com/about"
        node = TextNode(anchortext, text_type_link, href_link)
        expected = f'<a href="{href_link}">{anchortext}</a>'
        self.assertEqual(expected, text_node_to_html_node(node).to_html())


if __name__ == "__main__":
    unittest.main()

