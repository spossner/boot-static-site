import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_success(self):
        empty = HTMLNode()
        self.assertIsNone(empty.props_to_html())

    def test_span(self):
        node = HTMLNode("span")
        self.assertIsNone(node.props_to_html())
        self.assertEqual(node.tag, "span")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_simple(self):
        node = HTMLNode(tag="p", value="foo bar", props={"class": "bg-red-700 px-3 py-1"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "foo bar")
        self.assertIsNone(node.children)
        self.assertEqual(node.props_to_html(), ' class="bg-red-700 px-3 py-1"')
        

    def test_multiprops(self):
        node = HTMLNode(tag="a", value="Click me", props={"class": "bg-red-700 px-3 py-1", "href": "https://possner.dev", "target": "_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertIsNone(node.children)
        self.assertEqual(node.props_to_html(), ' class="bg-red-700 px-3 py-1" href="https://possner.dev" target="_blank"')
