import unittest

from inline_handler import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineHandler(unittest.TestCase):
    def test_split_one_delimited_section(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_delimited_sections(self):
        node = TextNode("A **bold** and **strong** line", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
                TextNode(" line", TextType.TEXT),
            ],
        )

    def test_split_code_delimiter(self):
        node = TextNode("Use `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            result,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_are_not_split(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        italic_node = TextNode("already italic", TextType.ITALIC)
        result = split_nodes_delimiter([bold_node, italic_node], "**", TextType.BOLD)

        self.assertEqual(result, [bold_node, italic_node])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("left", TextType.BOLD),
            TextNode("start *italic* end", TextType.TEXT),
            TextNode("right", TextType.CODE),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

        self.assertEqual(
            result,
            [
                TextNode("left", TextType.BOLD),
                TextNode("start ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
                TextNode("right", TextType.CODE),
            ],
        )

    def test_no_delimiter_returns_text_node(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [TextNode("plain text only", TextType.TEXT)])

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_consecutive_delimiters_skip_empty_sections(self):
        node = TextNode("a **** b", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("a ", TextType.TEXT),
                TextNode(" b", TextType.TEXT),
            ],
        )

    def test_raises_on_missing_closing_delimiter(self):
        node = TextNode("This has **unclosed bold", TextType.TEXT)

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertIn("Invalid Markdown syntax", str(context.exception))
        self.assertIn("**", str(context.exception))

    def test_raises_when_one_of_many_nodes_is_invalid(self):
        nodes = [
            TextNode("good *italic*", TextType.TEXT),
            TextNode("bad *italic", TextType.TEXT),
        ]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_does_not_match_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_does_not_match_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_with_exclamation_mark_in_text(self):
        matches = extract_markdown_links(
            "This is text with a [link with ! in text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("link with ! in text", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_with_exclamation_mark_in_text(self):
        matches = extract_markdown_images(
            "This is text with an ![image with ! in text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image with ! in text", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_links_with_exclamation_mark_in_url(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png?query=with!exclamation)"
        )
        self.assertListEqual(
            [("link", "https://i.imgur.com/zjjcJKZ.png?query=with!exclamation")],
            matches,
        )

    def test_extract_markdown_images_with_exclamation_mark_in_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png?query=with!exclamation)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png?query=with!exclamation")],
            matches,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://example.com) in text", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text", TextType.TEXT),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png) in text", TextType.TEXT
        )
        result = split_nodes_image([node])

        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" in text", TextType.TEXT),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_and_image(self):
        node = TextNode(
            "This is a [link](https://example.com) and an ![image](https://example.com/image.png) in text",
            TextType.TEXT,
        )
        result = split_nodes_link(split_nodes_image([node]))

        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" in text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_plain_text(self):
        result = text_to_textnodes("just plain text")
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_text_to_textnodes_all_supported_markdown(self):
        text = (
            "start **bold** *italic* `code` "
            "[link](https://example.com) ![img](https://example.com/img.png) end"
        )
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_raises_on_invalid_markdown(self):
        with self.assertRaises(Exception):
            text_to_textnodes("broken **bold")


if __name__ == "__main__":
    unittest.main()
