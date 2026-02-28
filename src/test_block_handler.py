import unittest

from block_handler import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockHandler(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is one paragraph."
        self.assertEqual(markdown_to_blocks(markdown), ["This is one paragraph."])

    def test_multiple_blocks(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n- item 1\n- item 2"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["# Heading", "This is a paragraph.", "- item 1\n- item 2"],
        )

    def test_strips_block_whitespace(self):
        markdown = "   # Heading   \n\n   Paragraph with spaces.   "
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["# Heading", "Paragraph with spaces."],
        )

    def test_ignores_empty_blocks(self):
        markdown = "\n\n# Heading\n\n\n\nParagraph\n\n"
        self.assertEqual(markdown_to_blocks(markdown), ["# Heading", "Paragraph"])

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_valid(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_block_to_block_type_heading_invalid(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_multiline(self):
        self.assertEqual(
            block_to_block_type("```\nline 1\nline 2\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("```inline```"),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_quote_block_every_line(self):
        self.assertEqual(
            block_to_block_type(">line 1\n> line 2\n>line 3"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("> line 1\nline 2"),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_unordered_list_every_line(self):
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2\n- item 3"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("- item 1\n-item 2"),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_ordered_list_sequential(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. third"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("2. second\n3. third"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
