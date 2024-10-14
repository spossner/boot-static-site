import unittest

from textnode import *
from parser import *

class TestParser(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])


    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_long(self):
        node = TextNode("This is text with an *italic* word and also **bold** and `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and also ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ])

    def test_mulit(self):
        node = TextNode("This is text with an *italic* and another *italic* word - finishing *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and another ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word - finishing ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ])

    def test_no_image(self):
        text = "This is text without an image"
        self.assertIsNone(extract_markdown_images(text))


    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more text"
        self.assertListEqual(extract_markdown_images(text), [
            "This is text with a ",
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            " and ",
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            " and more text",
        ])

    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(text), [
            "This is text with a link ",
            ("to boot dev", "https://www.boot.dev"), 
            " and ",
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ])

    def test_split_image(self):
        node = TextNode("This is text with an *italic* and another *italic* word - finishing *italic* and an image: ![logo](https://possner.dev/logo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an *italic* and another *italic* word - finishing *italic* and an image: ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "https://possner.dev/logo.png"),
        ])

    def test_split_image_no_image(self):
        node = TextNode("This is text with an *italic* and another *italic* word - finishing *italic*", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an *italic* and another *italic* word - finishing *italic*", TextType.TEXT),
        ])

    def test_split_links(self):
        node = TextNode("This is text with a link: [possner.dev](https://possner.dev) and an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link: ", TextType.TEXT),
            TextNode("possner.dev", TextType.LINK, "https://possner.dev"),
            TextNode(" and an *italic* word", TextType.TEXT),
        ])

    def test_split_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("", TextType.TEXT),
        ])
