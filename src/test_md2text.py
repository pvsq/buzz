import unittest, re

from md2text import (
    extract_markdown_images,
    extract_markdown_links
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

