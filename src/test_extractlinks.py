import unittest

from extractlinks import extract_markdown_images, extract_markdown_links

class TestExtract(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is some text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_with_escaped_parentheses(self):
        matches = extract_markdown_links(
            "This is some text with a [link](https://example.com\\(escaped\\))"
        )
        self.assertListEqual([("link", "https://example.com\\(escaped\\)")], matches)

    def test_extract_markdown_images_with_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/2zjjcJKZ.png)")
        self.assertListEqual(
            [
                ("image1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/2zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is some text with a [link1](https://example.com) and [link2](https://example2.com)")
        self.assertListEqual(
            [
                ("link1", "https://example.com"),
                ("link2", "https://example2.com")], matches)
    
    def test_extract_markdown_links_with_no_links(self):
        matches = extract_markdown_links(
            "This is some text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_no_images(self):
        matches = extract_markdown_images(
            "This is some text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_incorrect_argument(self):
        with self.assertRaises(ValueError):
            extract_markdown_images(12345)
        
    def test_extract_markdown_links_with_incorrect_argument(self):
        with self.assertRaises(ValueError):
            extract_markdown_links(12345)

    def test_extract_markdown_links_with_nested_brackets(self):
        matches = extract_markdown_links(
            "This is some text with a [link [nested]](https://example.com)")
        self.assertListEqual([("link [nested]", "https://example.com")], matches)
    
    def test_extract_markdown_links_with_empty_link_text(self):
        matches = extract_markdown_links(
            "This is some text with a [](example.com)")
        self.assertListEqual([("", "example.com")], matches)
    
    def test_extract_markdown_images_with_spaces_and_special_charactesr(self):
        matches = extract_markdown_images(
            "This is text with an ![image with spaces](https://i.imgur.com/z jjcJK@^Z. png)")
        self.assertListEqual([("image with spaces", "https://i.imgur.com/z jjcJK@^Z. png")], matches)

    def test_extract_markdown_images_with_link_in_text(self):
        matches = extract_markdown_images(
            "This is text with a ![coolpage.com/image](https://i.imgur.com/coolestpicever.png)")
        self.assertListEqual([("coolpage.com/image", "https://i.imgur.com/coolestpicever.png")], matches)