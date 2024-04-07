import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unorderedlist = "unordered_list"
block_type_orderedlist = "ordered_list"

HEADING_RE = r"^#{1,6} "
CODE_BLOCK = r"```"
QUOTE_BLOCK = r"^>"
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
            if not re.match(QUOTE_BLOCK, line):
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

