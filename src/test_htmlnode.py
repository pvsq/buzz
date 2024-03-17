import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_propsToHtml(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode('a', "Link", props=props)

        expected = ' href="https://www.google.com" target="_blank"'
        attrs = node.props_to_html()

        self.assertEqual(expected, attrs)

    def test_propsToHtml_whenNoProps(self):
        node = HTMLNode('a', "Link")

        expected = ""
        attrs = node.props_to_html()

        self.assertEqual(expected, attrs)

