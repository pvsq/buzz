import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_toHTML_whenValueIsNone(self):
        node = LeafNode("a")
        self.assertRaises(ValueError, node.to_html)

    def test_toHTML_whenValueIsEmptyString(self):
        node = LeafNode("a", "")
        self.assertEqual("<a></a>", node.to_html())

    def test_toHTML_whenTagIsNoneOrEmptyString(self):
        node = LeafNode(value="This is just raw text.")
        expected = "This is just raw text."
        self.assertEqual(expected, node.to_html())

    def test_toHTML_whenOnlyPropsIsNone(self):
        ptext = "This is a paragraph of text."
        node = LeafNode("p", ptext)
        expected = f"<p>{ptext}</p>"
        self.assertEqual(expected, node.to_html())

    def test_toHTML_withProps(self):
        atext = "Click here to learn more."
        alink = "https://www.example.com/about.html"
        aprops = {
            "href": alink
        }
        node = LeafNode("a", atext, aprops)
        expected = f'<a href="{alink}">{atext}</a>'
        self.assertEqual(expected, node.to_html())

