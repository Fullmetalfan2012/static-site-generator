import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello World", None, {"class": "my-div"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "my-div"})
    
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello World", None, {"class": "my-div", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-div" id="my-id"')
    
    def test_props_to_html_none(self):
        node = HTMLNode("div", "Hello World", None, None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode("div", "Hello World", None, {"class": "my-div"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello World, None, {'class': 'my-div'})")
    



if __name__ == "__main__":
    unittest.main()