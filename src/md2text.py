import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
)

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = [node.text]
        for match in matches:
            split_text = text[0].split(f"![{match[0]}]({match[1]})", 1)
            new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_image, match[1]))
            if split_text[1:]:
                text = split_text[1:]

        # text must be left with just one element at this point
        if text and text[0] != "":
            new_nodes.append(TextNode(text[0], text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = [node.text]
        for match in matches:
            split_text = text[0].split(f"[{match[0]}]({match[1]})", 1)
            if split_text[0][-1] == "!":
                new_nodes.append(TextNode(split_text[0] + f"[{match[0]}]({match[1]})", 
                                          text_type_text))
                if split_text[1:]:
                    text = split_text[1:]
                continue

            new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_link, match[1]))
            if split_text[1:]:
                text = split_text[1:]

        # text must be left with just one element at this point
        if text and text[0] != "":
            new_nodes.append(TextNode(text[0], text_type_text))
    return new_nodes

