import unittest

from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_neq_url(self):
        node = TextNode("This is a url", TextType.LINK, None)
        node2 = TextNode("This is a url", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a url", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a url", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a url", TextType.LINK, None)
        node2 = TextNode("This is a url", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "image")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "This is an image"})
    

    def test_unknown_text_type(self):
        node = TextNode("This is an unknown text type", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")
    
if __name__ == "__main__":
    unittest.main()