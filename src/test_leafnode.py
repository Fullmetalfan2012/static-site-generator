import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "Hello World", {"class": "my-paragraph"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "my-paragraph"})
    
    def test_to_html(self):
        node = LeafNode("p", "Hello World", {"class": "my-paragraph"})
        self.assertEqual(node.to_html(), '<p class="my-paragraph">Hello World</p>')
    
    def test_to_html_no_tag(self):
        node = LeafNode("", "Hello World", {"class": "my-paragraph"})
        self.assertEqual(node.to_html(), 'Hello World')
    
    def test_to_html_none_value(self):
        node = LeafNode("p", None, {"class": "my-paragraph"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_repr(self):
        node = LeafNode("p", "Hello World", {"class": "my-paragraph"})
        self.assertEqual(repr(node), "LeafNode(p, Hello World, {'class': 'my-paragraph'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()