from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import *

import unittest

class TestSplitNodesDelimiter(unittest.TestCase):

    # Test with normal text
    def test_split_nodes_delimiter_normal_text(self):
        old_nodes = [TextNode("This is normal text", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(old_nodes, "", TextType.NORMAL)
        self.assertEqual(new_nodes, old_nodes)

    # Test with bold text
    def test_split_nodes_delimiter_bold_text(self):
        old_nodes = [TextNode("This is bold text", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)
    
    # Test with italic text
    def test_split_nodes_delimiter_italic_text(self):
        old_nodes = [TextNode("This is italic text", TextType.ITALIC)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, old_nodes)

    # Test with code text
    def test_split_nodes_delimiter_code_text(self):
        old_nodes = [TextNode("This is code text", TextType.CODE)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, old_nodes)

    # Test splitting with normal and bold text
    def test_split_nodes_delimiter_normal_and_bold_text(self):
        old_nodes = [TextNode("This is **bold** test", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " test")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    # Test splitting with normal and italic text
    def test_split_nodes_delimiter_normal_and_italic_text(self):
        old_nodes = [TextNode("This is _italic_ test", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " test")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    # Test splitting with normal and code text
    def test_split_nodes_delimiter_normal_and_code_text(self):
        old_nodes = [TextNode("This is `code` test", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " test")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    # Test splitting in two stages with normal, bold and italic text
    def test_split_nodes_delimiter_normal_bold_italic_text(self):
        old_nodes = [TextNode("This is **bold** and _italic_ test", TextType.NORMAL)]
        new_nodes_bold = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes_italic = split_nodes_delimiter(new_nodes_bold, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes_bold), 3)
        self.assertEqual(new_nodes_bold[0].text, "This is ")
        self.assertEqual(new_nodes_bold[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes_bold[1].text, "bold")
        self.assertEqual(new_nodes_bold[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes_bold[2].text, " and _italic_ test")
        self.assertEqual(new_nodes_bold[2].text_type, TextType.NORMAL)
        self.assertEqual(len(new_nodes_italic), 5)
        self.assertEqual(new_nodes_italic[0].text, "This is ")
        self.assertEqual(new_nodes_italic[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes_italic[1].text, "bold")
        self.assertEqual(new_nodes_italic[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes_italic[2].text, " and ")
        self.assertEqual(new_nodes_italic[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes_italic[3].text, "italic")
        self.assertEqual(new_nodes_italic[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes_italic[4].text, " test")
        self.assertEqual(new_nodes_italic[4].text_type, TextType.NORMAL)

    # Test two images split
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    # Test two links split
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example2.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second link", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )
    # Test with no string 
    def test_split_links_no_string(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    # Test with empty string
    def test_split_images_empty_string(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)

    # Test with nested brackets
    def test_split_links_nested_brackets(self):
        node = TextNode(
            "This is some text with a [link [nested]](https://example.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.NORMAL),
                TextNode("link [nested]", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    # Test with sequential links
    def test_split_links_sequential(self):
        node = TextNode(
            "This is some text with a [link1](https://example.com)[link2](https://example2.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.NORMAL),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode("link2", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )
    # Test with plain text
    def test_split_links_plain_text(self):
        node = TextNode("This is some plain text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    # Test with multiple nodes
    def test_split_links_multiple_nodes(self):
        node1 = TextNode("This is some text with a [link1](https://example.com)", TextType.NORMAL)
        node2 = TextNode("This is some text with a [link2](https://example2.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.NORMAL),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode("This is some text with a ", TextType.NORMAL),
                TextNode("link2", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )
    
    #Test input node with different texttype
    def test_split_links_different_texttype(self):
        node = TextNode("Bold text", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])
       
    #Test text_to_textnodes with normal text
    def test_text_to_textnodes_normal(self):
        text = "This is normal text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)

    #Test text_to_textnodes with bold text
    def test_text_to_textnodes_bold(self):
        text = "**This is bold text**"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is bold text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    #Test text_to_textnodes with normal and bold text
    def test_text_to_textnodes_normal_and_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL)

    #Test text_to_textnodes with normal, bold and image
    def test_text_to_textnodes_normal_bold_image(self):
        text = "This is **bold** and ![image](https://i.imgur.com/zjjcJKZ.png) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(nodes[3].text, "image")
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(nodes[4].text, " text")
        self.assertEqual(nodes[4].text_type, TextType.NORMAL)
    