import unittest

from parser.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://possner.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://possner.dev")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://possner.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_normal_node(self):
        node = TextNode("Plain text")
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), "Plain text")

    def test_bold_node(self):
        node = TextNode("the text", TextType.BOLD)
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), "<b>the text</b>")

    def test_italc_node(self):
        node = TextNode("the text", TextType.ITALIC)
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), "<i>the text</i>")

    def test_code_node(self):
        node = TextNode("the text", TextType.CODE)
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), "<code>the text</code>")

    def test_link_node_missing_url(self):
        node = TextNode("the text", TextType.LINK)
        with self.assertRaises(ValueError) as cm:
            node.to_html_node()
        self.assertEqual(str(cm.exception), "missing url in link text node")

    def test_img_node_missing_url(self):
        node = TextNode("the text", TextType.IMAGE)
        with self.assertRaises(ValueError) as cm:
            node.to_html_node()
        self.assertEqual(str(cm.exception), "missing url in image text node")

    def test_link_node(self):
        node = TextNode("the text", TextType.LINK, "https://possner.dev")
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), '<a href="https://possner.dev">the text</a>')

    def test_image_node(self):
        node = TextNode("the text", TextType.IMAGE, "https://possner.dev/bliss.jpg")
        htmlNode = node.to_html_node()
        self.assertEqual(htmlNode.to_html(), '<img src="https://possner.dev/bliss.jpg" alt="the text"></img>')

if __name__ == "__main__":
    unittest.main()
