from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: missing closing delimiter '{delimiter}'")

        split_nodes = []
        for index, part in enumerate(parts):
            if part == "":
                continue
            if index % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    # Create the output list of transformed nodes.
    new_nodes = []
    # Walk through each incoming node.
    for node in old_nodes:
        # Only split plain text nodes; keep all others unchanged.
        if node.text_type != TextType.TEXT:
            # Preserve non-text node exactly as-is.
            new_nodes.append(node)
            # Move to the next node.
            continue

        # Find all markdown image matches in this node's text.
        image_matches = extract_markdown_images(node.text)
        # If there are no images, keep the node unchanged.
        if not image_matches:
            new_nodes.append(node)
            continue
        # Build intermediate pieces in order (text and image segments).
        parts = []
        # Track where the previous match ended.
        last_end = 0
        # Process each image match as (alt_text, image_url).
        for alt, url in image_matches:
            # Find this exact image markdown occurrence after last_end.
            start = node.text.find(f"![{alt}]({url})", last_end)
            # Compute the end index of the matched markdown text.
            end = start + len(f"![{alt}]({url})")
            # Continue only if this match occurrence is found.
            if start != -1:
                # Add preceding plain text segment, if any.
                if last_end < start:
                    parts.append((node.text[last_end:start], TextType.TEXT))
                # Add the image as an IMAGE text node tuple.
                parts.append((alt, TextType.IMAGE, url))
                # Advance cursor to the end of this match.
                last_end = end

        # Add remaining trailing plain text after the final match.
        if last_end < len(node.text):
            parts.append((node.text[last_end:], TextType.TEXT))

        # Convert tuples into TextNode objects and append them.
        new_nodes.extend([TextNode(*part) for part in parts])

    # Return all transformed nodes.
    return new_nodes

def split_nodes_link(old_nodes):
    # Create the output list of transformed nodes.
    new_nodes = []
    # Walk through each incoming node.
    for node in old_nodes:
        # Only split plain text nodes; keep all others unchanged.
        if node.text_type != TextType.TEXT:
            # Preserve non-text node exactly as-is.
            new_nodes.append(node)
            # Move to the next node.
            continue

        # Find all markdown link matches in this node's text.
        link_matches = extract_markdown_links(node.text)
        # If there are no links, keep the node unchanged.
        if not link_matches:
            new_nodes.append(node)
            continue
        # Build intermediate pieces in order (text and link segments).
        parts = []
        # Track where the previous match ended.
        last_end = 0
        # Process each link match as (link_text, link_url).
        for text, url in link_matches:
            # Find this exact link markdown occurrence after last_end.
            start = node.text.find(f"[{text}]({url})", last_end)
            # Compute the end index of the matched markdown text.
            end = start + len(f"[{text}]({url})")
            # Continue only if this match occurrence is found.
            if start != -1:
                # Add preceding plain text segment, if any.
                if last_end < start:
                    parts.append((node.text[last_end:start], TextType.TEXT))
                # Add the link as a LINK text node tuple.
                parts.append((text, TextType.LINK, url))
                # Advance cursor to the end of this match.
                last_end = end

        # Add remaining trailing plain text after the final match.
        if last_end < len(node.text):
            parts.append((node.text[last_end:], TextType.TEXT))

        # Convert tuples into TextNode objects and append them.
        new_nodes.extend([TextNode(*part) for part in parts])

    # Return all transformed nodes.
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes