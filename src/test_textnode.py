import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    #test eq with same text and type
    def test_eq_same_text_and_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    #test eq with different text
    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    #test eq with different type
    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #test eq with same url
    def test_eq_same_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertEqual(node, node2)  

    #test eq with different url
    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://different.com")
        self.assertNotEqual(node, node2)

    #test eq with url and no url
    def test_eq_url_and_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    #test empty string
    def test_eq_empty_string(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node, node2)

    #test text_node_to_html_node with normal text
    def test_text_node_to_html_node_normal(self):
        node = TextNode("This is a normal text", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a normal text")
        self.assertEqual(html_node.props, None)

    #test text_node_to_html_node with bold text
    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        self.assertEqual(html_node.props, None)

    #test text_node_to_html_node with none text type
    def test_text_node_to_html_node_none_type(self):
        node = TextNode("This is a text node", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    #test text_node_to_html_node with italic text
    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")
        self.assertEqual(html_node.props, None)

    #test text_node_to_html_node with link text
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    #test text_node_to_html_node with image text
    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "This is an image"})

    #test text_node_to_html_node with code text
    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code")
        self.assertEqual(html_node.props, None)
    
    #test text_node_to_html_node with non-valid enum in text type
    def test_text_node_to_html_node_invalid_enum(self):
        node = TextNode("This is a text node", "invalid_enum")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()