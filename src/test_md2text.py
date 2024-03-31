import unittest

from md2text import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
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

