import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value_only(self):
        node = LeafNode("foo bar")
        self.assertEqual(node.value, "foo bar")
        self.assertIsNone(node.tag)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props_to_html())
        self.assertEqual(node.to_html(), "foo bar")

    def test_success(self):
        simple = LeafNode("foo bar", "span")
        self.assertEqual(simple.value, "foo bar")
        self.assertEqual(simple.tag, "span")
        self.assertIsNone(simple.children)
        self.assertIsNone(simple.props_to_html())
        self.assertEqual(simple.to_html(), "<span>foo bar</span>")

    def test_full(self):
        node = LeafNode("foo bar", "a", props={"class": "bg-red-700 px-3 py-1", "href": "https://possner.dev", "target": "_blank"})
        self.assertEqual(node.value, "foo bar")
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.children)
        self.assertEqual(node.props_to_html(), ' class="bg-red-700 px-3 py-1" href="https://possner.dev" target="_blank"')
        self.assertEqual(node.to_html(), '<a class="bg-red-700 px-3 py-1" href="https://possner.dev" target="_blank">foo bar</a>')
