import unittest

from html.parentnode import ParentNode
from html.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_basic(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_deep(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p", 
                    [
                        LeafNode(None, "foo bar")
                    ],
                    {"class": "bg-color-red px-2"}),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),'<p><b>Bold text</b><p class="bg-color-red px-2">foo bar</p><i>italic text</i>Normal text</p>')

    def test_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "missing children")

    def test_empty_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "missing children")

    def test_no_tag(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "missing tag")
