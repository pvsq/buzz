import unittest, re

from md2text import (
    extract_markdown_images,
    extract_markdown_links
)

class TestMd2Text(unittest.TestCase):
    def test_extractMarkdownImages(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        matches = extract_markdown_images(text)
        expected = [('image', 'https://i.imgur.com/zjjcJKZ.png'), ('another', 'https://i.imgur.com/dfsdkjfd.png')]
        self.assertEqual(matches, expected)


    def test_extractMarkdownLinks(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        expected = [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')]
        self.assertEqual(matches, expected)


    def test_extractMarkdownImages_withLinksAsInput(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_images(text)
        expected = []
        self.assertEqual(matches, expected)


    def test_extractMarkdownLinks_withImagesAsInput(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        matches = extract_markdown_links(text)
        expected = []
        self.assertEqual(matches, expected)

