import unittest

from block_md2text import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_orderedlist,
    block_type_unorderedlist
)

class TestBlockMd2Text(unittest.TestCase):
    def test_markdownToBlocks(self):
        mdtext = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        blocks = markdown_to_blocks(mdtext)
        expected = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
            """* This is a list
* with items""",
        ]
        self.assertEqual(blocks, expected)


    def test_markdownToBlocks_withSingleLineInput(self):
        mdtext = """# One-liner heading with *inline* styling"""
        blocks = markdown_to_blocks(mdtext)
        expected = ["# One-liner heading with *inline* styling"]
        self.assertEqual(blocks, expected)


    def test_markdownToBlocks_withNoBlankLinesInput(self):
        mdtext = """This is **bolded** paragraph
This is the same paragraph with *italic* text and `code` here
This is the same paragraph on a new line
* This is a list
* with items"""
        blocks = markdown_to_blocks(mdtext)
        expected = ["""This is **bolded** paragraph
This is the same paragraph with *italic* text and `code` here
This is the same paragraph on a new line
* This is a list
* with items"""]
        self.assertEqual(blocks, expected)

