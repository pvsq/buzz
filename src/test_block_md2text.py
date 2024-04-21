import unittest

from block_md2text import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_orderedlist,
    block_type_unorderedlist,
    markdown_to_html_node
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


    def test_blockToBlockType(self):
        mdtext = """# Heading of The First Level

This is **bolded** paragraph

>Did you know?
>This block of text is a quote
>Every line of this block
>Must start with ">"

>This is not a quote
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

1. An ordered list
2. starting with the list item
3. numbered 1.
4. and ending with
5. list item number
6. 5.

* This is a list
* with items

```
Vapor
wave
Aesthetic
```
"""
        blocks = markdown_to_blocks(mdtext)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        expected = [
            block_type_heading, block_type_paragraph, block_type_quote,
            block_type_paragraph, block_type_orderedlist,
            block_type_unorderedlist, block_type_code
        ]
        self.assertListEqual(block_types, expected)


    def test_blockToBlockType_allHeadingsInput(self):
        mdtext = """# Heading Level 1

normal paragraph at level 1

## Heading Level 2

### Heading Level 3

1. list item at level 3
2. list item 2 at level 3
3. list item 3 at level 3

#### Heading Level 4

##### Heading Level 5

###### Heading Level 6

some more text at the end."""
        blocks = markdown_to_blocks(mdtext)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        expected = [
            block_type_heading, block_type_paragraph, block_type_heading,
            block_type_heading, block_type_orderedlist, block_type_heading,
            block_type_heading, block_type_heading, block_type_paragraph,
        ]
        self.assertListEqual(block_types, expected)


    def test_blockToBlockType_twoDigitOrderedListItemsInput(self):
        mdtext = """1. List item
2. List item
3. List item
4. List item
5. List item
6. List item
7. List item
8. List item
9. List item
10. List item
11. List item
12. List item
13. List item
14. List item
15. List item
16. List item
17. List item
18. List item
19. List item
20. List item
21. List item
"""
        blocks = markdown_to_blocks(mdtext)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        expected = [block_type_orderedlist]
        self.assertListEqual(block_types, expected)


    def test_markdownToHtmlNode_withSimpleMarkdownAsInput(self):
        markdown = """# Heading of The First Level

This is **bolded** paragraph

>Did you know?
>This block of text is a quote
>Every line of this block
>Must start with ">"

>This is not a quote
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

1. An ordered list
2. starting with the list item
3. numbered 1.
4. and ending with
5. list item number
6. 5.

## Heading of the second level

* This is a list
* with items

- Another list with
- an image ![an image](https://i.imgur.com/zjjcJKZ.png)
- and a [link](#)

```
Vapor
wave
Aesthetic
```
"""
        html = markdown_to_html_node(markdown).to_html()

        expected = ""
        with open("./testfiles/mdtohtml_test1_expected.txt", "r") as f:
            expected = f.read()
        expected = expected[:-1]  # remove newline at the end

        self.assertEqual(html, expected)


    def test_markdownToHtmlNode_withComplexMarkdownAsInput(self):
        text = ""
        with open("./testfiles/notes.md", "r") as f:
            text = f.read()

        html = markdown_to_html_node(text).to_html()

        expected = ""
        with open("./testfiles/testhtml_expected.txt", "r") as t:
            expected = t.read()
        expected = expected[:-1]  # remove newline at the end

        self.assertEqual(html, expected)

