import unittest

from parser.textnode import TextNode, TextType
from parser.parser import *

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

    def test_split_from_boot(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ])

    def test_parse_example(self):
        nodes = parse("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_blocks_simple(self):
        blocks = markdown_to_blocks('''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item''')
        self.assertListEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            '''* This is the first list item in a list block
* This is a list item
* This is another list item''',
        ])

    def test_blocks_heavy_newline(self):
        blocks = markdown_to_blocks('''# This is a heading
                                    


    and more text with whatever      
                                    
                
     and empty prefix
                                    



and empty suffix       
                                    
                                    ''')
        self.assertListEqual(blocks, [
            "# This is a heading",
            "and more text with whatever",
            "and empty prefix",
            "and empty suffix",
        ])

    def test_blocks_at_ending(self):
        blocks = markdown_to_blocks('''# This is a heading
                                    
- item 1
- item 2                        

and empty suffix''')
        self.assertListEqual(blocks, [
            "# This is a heading",
            '''- item 1
- item 2''',
            "and empty suffix",
        ])

    def test_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Heading 6"), BlockType.PARAGRAPH)

    def test_block_type_code(self):
        self.assertEqual(block_to_block_type("```print('Hello, world')```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("""```for i := range 10 {
    fmt.Println(i)
}```"""), BlockType.CODE)
        self.assertEqual(block_to_block_type("```weird block..."), BlockType.PARAGRAPH)

    def test_block_type_quote(self):
        self.assertEqual(block_to_block_type("> quoting"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("""> quote 1
> quote 2
> quote 3"""), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("""> quote 1
no quote here
> quote 3"""), BlockType.PARAGRAPH)
        
    def test_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("""- item 1
- item 2
- item 3"""), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("""* item 1
* item 2
* item 3"""), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("""- item 1
* item 2
* item 3"""), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("""- item 1
no item here
- item 3"""), BlockType.PARAGRAPH)
        
    def test_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("0. item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("""1. item 1
2. item 2
3. item 3"""), BlockType.ORDERED_LIST)

    def test_block_type_all_but_nothing(self):
        self.assertEqual(block_to_block_type("""1. item 1
1. no ite, here
2. but again correct numbering
3. last item"""), BlockType.PARAGRAPH)
