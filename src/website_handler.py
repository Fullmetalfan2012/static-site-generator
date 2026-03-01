from textnode import *
from inline_handler import *
from htmlnode import *
from parentnode import *
from leafnode import *
from block_handler import *
import os
import shutil


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        paragraph_text = " ".join(block.split("\n"))
        return ParentNode("p", text_to_children(paragraph_text))

    if block_type == BlockType.HEADING:
        heading_level = 0
        while heading_level < len(block) and block[heading_level] == "#":
            heading_level += 1
        heading_text = block[heading_level + 1 :]
        return ParentNode(f"h{heading_level}", text_to_children(heading_text))

    if block_type == BlockType.QUOTE:
        quote_lines = []
        for line in block.split("\n"):
            if line.startswith("> "):
                quote_lines.append(line[2:])
            else:
                quote_lines.append(line[1:])
        quote_text = " ".join(quote_lines)
        return ParentNode("blockquote", text_to_children(quote_text))

    if block_type == BlockType.UNORDERED_LIST:
        list_items = []
        for line in block.split("\n"):
            item_text = line[2:]
            list_items.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode("ul", list_items)

    if block_type == BlockType.ORDERED_LIST:
        list_items = []
        for index, line in enumerate(block.split("\n"), start=1):
            item_text = line[len(f"{index}. ") :]
            list_items.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode("ol", list_items)

    if block_type == BlockType.CODE:
        code_text = block[4:-3]
        code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
        return ParentNode("pre", [code_node])

    raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def copy_directory_recursive(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    for item_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item_name)
        destination_path = os.path.join(destination_dir, item_name)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_directory_recursive(source_path, destination_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header found in markdown to extract title from")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html = (
        template
        .replace("{{ Content }}", html_string)
        .replace("{{ Title }}", title)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    destination_directory = os.path.dirname(dest_path)
    if destination_directory:
        os.makedirs(destination_directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(content_dir, template_path, destination_dir, basepath):
    for root, _, files in os.walk(content_dir):
        for file_name in files:
            if not file_name.endswith(".md"):
                continue

            source_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(source_path, content_dir)
            destination_relative_path = os.path.splitext(relative_path)[0] + ".html"
            destination_path = os.path.join(destination_dir, destination_relative_path)
            generate_page(source_path, template_path, destination_path, basepath)