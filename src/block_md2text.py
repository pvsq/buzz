import re

from leafnode import LeafNode
from parentnode import ParentNode
from md2text import text_to_text_nodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unorderedlist = "unordered_list"
block_type_orderedlist = "ordered_list"

HEADING_RE = r"^#{1,6} "
CODE_BLOCK = r"```"
QUOTE_BLOCK_RE = r"^>"
UNORDERED_LIST_RE = r"^[*-]"
ORDERED_LIST_RE = r"^[1-9][0-9]*?\."

def markdown_to_blocks(mdtext):
    return mdtext.split("\n\n")


def block_to_block_type(mdblock: str):
    if re.match(HEADING_RE, mdblock):
        return block_type_heading
    if __is_block_type(block_type_code, mdblock):
        return block_type_code
    if __is_block_type(block_type_quote, mdblock):
        return block_type_quote
    if __is_block_type(block_type_unorderedlist, mdblock):
        return block_type_unorderedlist
    if __is_block_type(block_type_orderedlist, mdblock):
        return block_type_orderedlist

    return block_type_paragraph


def __is_block_type(block_type, mdblock):
    if (block_type == block_type_heading
            or block_type == block_type_paragraph):
        return False

    lines = mdblock.split("\n")
    if lines[-1] == "":
        lines = lines[:-1]

    if block_type == block_type_code:
        if not (re.match(CODE_BLOCK, lines[0])
            and re.match(CODE_BLOCK, lines[-1])):
            return False

    if block_type == block_type_quote:
        for line in lines:
            if not re.match(QUOTE_BLOCK_RE, line):
                return False

    if block_type == block_type_unorderedlist:
        for line in lines:
            if not re.match(UNORDERED_LIST_RE, line):
                return False

    if block_type == block_type_orderedlist:
        for line in lines:
            if not re.match(ORDERED_LIST_RE, line):
                return False

    return True


def markdown_to_html_node(markdown):
    child_nodes = []

    blocks = markdown_to_blocks(markdown)
    if blocks[-1] == "":
        blocks = blocks[:-1]

    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes.append(__md_block_to_html_node(block, block_type))

    return ParentNode("div", child_nodes)


def __md_block_to_html_node(block: str, block_type: str):
    if block_type == block_type_heading:
        return __md_block_to_html_heading(block)
    if block_type == block_type_quote:
        return __md_block_to_html_quote(block)
    if block_type == block_type_code:
        return __md_block_to_html_code(block)
    if block_type == block_type_unorderedlist:
        return __md_block_to_html_list(block, "ul")
    if block_type == block_type_orderedlist:
        return __md_block_to_html_list(block, "ol")

    return ParentNode("p", __text_nodes_to_html_nodes(
        text_to_text_nodes(block)
    ))


def __md_block_to_html_heading(block: str):
    if block.startswith("# "):
        return ParentNode("h1", __text_nodes_to_html_nodes(
            text_to_text_nodes(block[2:])
        ))
    if block.startswith("## "):
        return ParentNode("h2", __text_nodes_to_html_nodes(
            text_to_text_nodes(block[3:])
        ))
    if block.startswith("### "):
        return ParentNode("h3", __text_nodes_to_html_nodes(
            text_to_text_nodes(block[4:])
        ))
    if block.startswith("#### "):
        return ParentNode("h4", __text_nodes_to_html_nodes(
            text_to_text_nodes(block[5:])
        ))
    if block.startswith("##### "):
        return ParentNode("h5", __text_nodes_to_html_nodes(
            text_to_text_nodes(block[6:])
        ))

    return ParentNode("h6", __text_nodes_to_html_nodes(
        text_to_text_nodes(block[7:])
    ))


def __md_block_to_html_quote(block: str):
    lines = __remove_blank_lines(block.split("\n"))
    lines_without_prefix = []
    for line in lines:
        lines_without_prefix.append(line.removeprefix(">"))

    return ParentNode("blockquote", __text_nodes_to_html_nodes(
        text_to_text_nodes("\n".join(lines_without_prefix))
    ))


def __md_block_to_html_code(block: str):
    lines = __remove_blank_lines(block.split("\n"))

    return ParentNode("code", [
        LeafNode("pre", "\n".join(lines[1:-1]))
    ])


def __md_block_to_html_list(block: str, list_type: str):
    html_list_items = []
    lines = __remove_blank_lines(block.split("\n"))
    pattern = ""

    if list_type == "ol":
        pattern = r"^[1-9][0-9]*?\.(.*)"
    else:
        pattern = r"^[*-](.*)"

    for line in lines:
        text = re.findall(pattern, line)[0].lstrip(" ")
        html_list_items.append(
            ParentNode("li", __text_nodes_to_html_nodes(
                text_to_text_nodes(text)
            ))
        )

    return ParentNode(list_type, html_list_items)


def __remove_blank_lines(lines):
    new_lines = []
    for line in lines:
        if line != "":
            new_lines.append(line)
    return new_lines


def __text_nodes_to_html_nodes(text_nodes):
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

