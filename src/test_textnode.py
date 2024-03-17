import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_eq_whenDifferentUrl(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8008")
        node2 = TextNode("This is a text node", "bold", "http://localhost:8080")
        self.assertNotEqual(node, node2)

    def test_eq_whenDifferentTextType(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8080")
        node2 = TextNode("This is a text node", "italic", "http://localhost:8080")
        self.assertNotEqual(node, node2)

    def test_eq_whenDifferentText(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8080")
        node2 = TextNode("This is a text mode", "bold", "http://localhost:8080")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        expected = "TextNode(This is a text node, bold, http://localhost:8080)"
        node = TextNode("This is a text node", "bold", "http://localhost:8080")
        self.assertEqual(expected, str(node))


if __name__ == "__main__":
    unittest.main()

