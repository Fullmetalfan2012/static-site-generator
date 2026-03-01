import unittest
import os
import tempfile

from website_handler import extract_title, markdown_to_html_node, generate_page


class TestWebsiteHandler(unittest.TestCase):
    def test_markdown_to_html_node_wraps_in_div(self):
        markdown = "# Heading\n\nA paragraph"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><h1>Heading</h1><p>A paragraph</p></div>")

    def test_unordered_and_ordered_lists(self):
        markdown = "- first\n- second\n\n1. one\n2. two"
        node = markdown_to_html_node(markdown)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first</li><li>second</li></ul><ol><li>one</li><li>two</li></ol></div>",
        )

    def test_quote_block(self):
        markdown = "> quote line\n> with *style*"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><blockquote>quote line with <i>style</i></blockquote></div>")

    def test_code_block_does_not_parse_inline(self):
        markdown = "```\n`literal` **not bold**\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><pre><code>`literal` **not bold**\n</code></pre></div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title_returns_h1_text(self):
        markdown = "# My Page Title\n\nSome paragraph text"
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_extract_title_returns_first_h1(self):
        markdown = "## Subtitle\n# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_extract_title_raises_without_h1(self):
        markdown = "## Subtitle\n\nParagraph text"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_generate_page_rewrites_root_relative_links_with_basepath(self):
        markdown = "# Test Page\n\n[Home](/)\n\n![Pic](/images/pic.png)"
        template = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"

        with tempfile.TemporaryDirectory() as tmpdir:
            from_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "out", "index.html")

            with open(from_path, "w") as f:
                f.write(markdown)
            with open(template_path, "w") as f:
                f.write(template)

            generate_page(from_path, template_path, dest_path, "/docs/")

            with open(dest_path, "r") as f:
                html = f.read()

        self.assertIn('href="/docs/"', html)
        self.assertIn('src="/docs/images/pic.png"', html)


if __name__ == "__main__":
    unittest.main()
