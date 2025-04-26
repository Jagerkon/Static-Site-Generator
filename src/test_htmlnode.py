import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    # Test initialization with no parameters
    def test_init_no_params(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    # Test initialization with all parameters
    def test_init_all_params(self):
        node = HTMLNode("div", "Hello, World!", ["child1", "child2"], {"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "my-class"})
    
    # Test props_to_html with no props
    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Hello, World!", ["child1", "child2"], None)
        self.assertEqual(node.props_to_html(), "")

    # Test props_to_html with props
    def test_props_to_html_with_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


    # Test props_to_html with empty props
    def test_props_to_html_empty_props(self):
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), "")

    # Test props_to_html with None props
    def test_props_to_html_none_props(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")

    # Test props_to_html with multiple props
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank", "class": "my-class"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank" class="my-class"')

    # Test __repr__ method
    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", ["child1", "child2"], {"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNODE(div, Hello, World!, ['child1', 'child2'], {'class': 'my-class'})")

    # Test initializaition with HTMLnode as children
    def test_init_htmlnode_children(self):
        child_node = HTMLNode("span", "Child Node", None, {"class": "child-class"})
        node = HTMLNode("div", "Parent Node", [child_node], {"class": "parent-class"})
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.children[0].value, "Child Node")
        self.assertEqual(node.children[0].props, {"class": "child-class"})
    
    # Test to_html 
    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode("div", "Hello, World!", ["child1", "child2"], {"class": "my-class"})
            node.to_html()

    #Test LeafNode initialization
    def test_leaf_node_init(self):
        node = HTMLNode("span", "Leaf Node", None, {"class": "leaf-class"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Leaf Node")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "leaf-class"})

    #Test LeafNode to_html
    def test_leaf_node_to_html(self):
        node = LeafNode("span", "Leaf Node", {"class": "leaf-class"})
        self.assertEqual(node.to_html(), "<span class=\"leaf-class\">Leaf Node</span>")

    #Test LeafNode to_html with no value
    def test_leaf_node_to_html_no_value(self):
        node = LeafNode("span", None, {"class": "leaf-class"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    #Test LeafNode to_html with no tag
    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(None, "Leaf Node", {"class": "leaf-class"})
        self.assertEqual(node.to_html(), "Leaf Node")

    #Test LeafNode with different tag
    def test_leaf_node_different_tag(self):
        node = LeafNode("li", "Item 1", {"class": "leaf-class"})
        self.assertEqual(node.to_html(), '<li class="leaf-class">Item 1</li>')

    #Test ParentNode with one child
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    #Test ParentNode with multiple children
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    #Test ParentNode with no children
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    #Test ParentNode with no tag
    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, ["child"])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    #Test ParentNode with no tag and no children
    def test_to_html_no_tag_and_no_children(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    #Test ParentNode with nested nodes
    def test_deeply_nested_parent_nodes(self):
        # Create the most deeply nested node first
        deep_leaf = LeafNode("em", "very deep")
        # Create a parent for that leaf
        level3 = ParentNode("div", [deep_leaf])
        # Create another level with both a leaf and the previous parent
        level2 = ParentNode("section", [LeafNode("span", "sibling"), level3])
        # Create the top-level parent with multiple children
        root = ParentNode("article", [
            LeafNode("h1", "title"),
            level2,
            LeafNode("footer", "the end")
        ])
    
        # Assert the complete HTML structure
        self.assertEqual(
            root.to_html(),
            "<article><h1>title</h1><section><span>sibling</span><div><em>very deep</em></div></section><footer>the end</footer></article>"
        )

        # Test with props
    def test_deeply_nested_parent_nodes_with_props(self):
        # Create the most deeply nested node first
        deep_leaf = LeafNode("em", "very deep")
        # Create a parent for that leaf
        level3 = ParentNode("div", [deep_leaf], {"class": "level3"})
        # Create another level with both a leaf and the previous parent
        level2 = ParentNode("section", [LeafNode("span", "sibling")], {"class": "level2"})
        # Create the top-level parent with multiple children
        root = ParentNode("article", [
            LeafNode("h1", "title"),
            level2,
            level3,
            LeafNode("footer", "the end")
        ], {"class": "root"})
        
            # Assert the complete HTML structure
        self.assertEqual(
            root.to_html(),
            '<article class="root"><h1>title</h1><section class="level2"><span>sibling</span></section><div class="level3"><em>very deep</em></div><footer>the end</footer></article>'
        )

if __name__ == "__main__":
    unittest.main()