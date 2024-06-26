import unittest

from md2text import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestMd2Text(unittest.TestCase):
    IMAGES_TEXT = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
    LINKS_TEXT = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    IMAGES_AND_LINKS_TEXT = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.example.com) and [another](https://www.example.com/another) and ![another](https://i.imgur.com/dfsdkjfd.png)"

    EXPECTED_IMAGES_LIST = [('image', 'https://i.imgur.com/zjjcJKZ.png'), ('another', 'https://i.imgur.com/dfsdkjfd.png')]
    EXPECTED_LINKS_LIST = [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')]

    def test_splitNodesDelimiter_withSingleNode(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected)


    def test_splitNodesDelimiter_withMultiplesNodes(self):
        nodes = [
            TextNode("This is text with an *emphasized block* of words", text_type_text),
            TextNode("Some bold text", text_type_bold),
            TextNode("Welcome to the *jungle*, it gets *worse here everyday*.", text_type_text),
        ]
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("emphasized block", text_type_italic),
            TextNode(" of words", text_type_text),
            TextNode("Some bold text", text_type_bold),
            TextNode("Welcome to the ", text_type_text),
            TextNode("jungle", text_type_italic),
            TextNode(", it gets ", text_type_text),
            TextNode("worse here everyday", text_type_italic),
            TextNode(".", text_type_text),
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
        self.assertListEqual(new_nodes, expected)


    def test_splitNodesDelimiter_withEmptyList(self):
        nodes = []
        expected = []
        new_nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
        self.assertListEqual(new_nodes, expected)


    def test_splitNodesDelimiter_withDelimiterNotClosed(self):
        nodes = [
            TextNode("This text with *italicized text* has *not been closed", text_type_text)
        ]
        self.assertRaises(ValueError, split_nodes_delimiter, nodes, "*", text_type_italic)


    def test_splitNodesDelimiter_withNoTextTypeTextNodes(self):
        nodes = [
            TextNode("Some bold text", text_type_bold),
            TextNode("Some italicized text", text_type_italic),
            TextNode("Text styled inline with a fixed-width font", text_type_code),
            TextNode("Some more italicized text", text_type_italic)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", text_type_code)
        self.assertListEqual(new_nodes, nodes)


    def test_splitNodesDelimiter_withMixedTextTypeTextNodes(self):
        nodes = [
            TextNode("This is text with an *emphasized block* of words", text_type_text),
            TextNode("Some bold text", text_type_bold),
            TextNode("Text styled `inline` with a `fixed-width` font", text_type_text),
            TextNode("Welcome to the **jungle**, it gets **worse here everyday**.", text_type_text),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", text_type_code)
        expected = [
            TextNode("This is text with an *emphasized block* of words", text_type_text),
            TextNode("Some bold text", text_type_bold),
            TextNode("Text styled ", text_type_text),
            TextNode("inline", text_type_code),
            TextNode(" with a ", text_type_text),
            TextNode("fixed-width", text_type_code),
            TextNode(" font", text_type_text),
            TextNode("Welcome to the **jungle**, it gets **worse here everyday**.", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)


    def test_extractMarkdownImages(self):
        text = TestMd2Text.IMAGES_TEXT
        matches = extract_markdown_images(text)
        expected = TestMd2Text.EXPECTED_IMAGES_LIST
        self.assertEqual(matches, expected)


    def test_extractMarkdownLinks(self):
        text = TestMd2Text.LINKS_TEXT
        matches = extract_markdown_links(text)
        expected = TestMd2Text.EXPECTED_LINKS_LIST
        self.assertEqual(matches, expected)


    def test_extractMarkdownImages_withLinksAsInput(self):
        text = TestMd2Text.LINKS_TEXT
        matches = extract_markdown_images(text)
        expected = []
        self.assertEqual(matches, expected)


    def test_extractMarkdownLinks_withImagesAsInput(self):
        text = TestMd2Text.IMAGES_TEXT
        matches = extract_markdown_links(text)
        expected = []
        self.assertEqual(matches, expected)


    def test_extractMarkdownImages_withMixedImagesAndLinksInput(self):
        text = TestMd2Text.IMAGES_AND_LINKS_TEXT
        matches = extract_markdown_images(text)
        expected = TestMd2Text.EXPECTED_IMAGES_LIST
        self.assertEqual(matches, expected)


    def test_extractMarkdownLinks_withMixedImagesAndLinksInput(self):
        text = TestMd2Text.IMAGES_AND_LINKS_TEXT
        matches = extract_markdown_links(text)
        expected = TestMd2Text.EXPECTED_LINKS_LIST
        self.assertEqual(matches, expected)


    def test_splitNodesImage_withSingleNodeInput(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesLink_withSingleNodeInput(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link", text_type_link, "https://www.example.com/another"
            ),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesImage_withLinksInput(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
                "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
                text_type_text,
            ),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesLink_withImagesInput(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                text_type_text,
            ),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesImage_withMultipleNodesInput(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", text_type_text),
            TextNode("This node is just text, no inline styles here.", text_type_text),
            TextNode("This is text with an *emphasized block* of words", text_type_italic),
            TextNode("Some bold text", text_type_bold),
            TextNode(
                "More text with more ![images](https://i.imgur.com/zjjcJKZ.png) and some more ![cool images](https://i.imgur.com/3elNhQu.png)",
                text_type_text,
            ),
            TextNode("Text styled `inline` with a `fixed-width` font", text_type_code),
            TextNode("This is text with a `code block` word", text_type_text),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            TextNode("This node is just text, no inline styles here.", text_type_text),
            TextNode("This is text with an *emphasized block* of words", text_type_italic),
            TextNode("Some bold text", text_type_bold),
            TextNode("More text with more ", text_type_text),
            TextNode("images", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some more ", text_type_text),
            TextNode("cool images", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            TextNode("Text styled `inline` with a `fixed-width` font", text_type_code),
            TextNode("This is text with a `code block` word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesLink_withMultipelNodesInput(self):
        nodes = [
            TextNode("This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)", text_type_text),
            TextNode("This node is just text, no inline styles here.", text_type_text),
            TextNode("This is text with an *emphasized block* of words", text_type_italic),
            TextNode("Some bold text", text_type_bold),
            TextNode(
                "More text with more [links](https://i.imgur.com/zjjcJKZ.png) and some more [cool links](https://i.imgur.com/3elNhQu.png)",
                text_type_text,
            ),
            TextNode("Text styled `inline` with a `fixed-width` font", text_type_code),
            TextNode("This is text with a `code block` word", text_type_text),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://www.example.com/another"),
            TextNode("This node is just text, no inline styles here.", text_type_text),
            TextNode("This is text with an *emphasized block* of words", text_type_italic),
            TextNode("Some bold text", text_type_bold),
            TextNode("More text with more ", text_type_text),
            TextNode("links", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some more ", text_type_text),
            TextNode("cool links", text_type_link, "https://i.imgur.com/3elNhQu.png"),
            TextNode("Text styled `inline` with a `fixed-width` font", text_type_code),
            TextNode("This is text with a `code block` word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesImage_withMixedImageAndLinksInput(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)", text_type_text)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a [link](https://i.imgur.com/3elNhQu.png)", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)


    def test_splitNodesLinks_withMixedImageAndLinksInput(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", text_type_text),
            TextNode("link", text_type_link, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes, expected)


    def test_textToTextNodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)


    def test_textToTextNodes_withBoldTextOnly(self):
        text = "This is **text** that is **bold** and **this is some more bold text** and **some more** and this is the **end** of the text."
        nodes = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" that is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("this is some more bold text", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("some more", text_type_bold),
            TextNode(" and this is the ", text_type_text),
            TextNode("end", text_type_bold),
            TextNode(" of the text.", text_type_text),
        ]
        self.assertEqual(nodes, expected)

