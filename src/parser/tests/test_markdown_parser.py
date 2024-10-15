import unittest
import os

from parser.parser import *

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestMarkdownParser(unittest.TestCase):
    def test_simple_paragraphs(self):
        node = markdown_to_html_node('''This is a simple paragraph of text.
Multiline but pure text''')
        self.assertEqual(node.to_html(), '''<div><p>This is a simple paragraph of text.
Multiline but pure text</p></div>''')

    def test_multiple_simple_blocks(self):
        node = markdown_to_html_node('''This is a simple first paragraph.\n\nAnd a second paragraph.''')
        self.assertEqual(node.to_html(), '''<div><p>This is a simple first paragraph.</p><p>And a second paragraph.</p></div>''')

    def test_monster_simple_blocks(self):
        node = markdown_to_html_node('''This is a simple first paragraph.\n\nAnd a second paragraph.\n\nAnd third paragraph.\n\nAnd number four.''')
        self.assertEqual(node.to_html(), '''<div><p>This is a simple first paragraph.</p><p>And a second paragraph.</p><p>And third paragraph.</p><p>And number four.</p></div>''')

    def test_heading(self):
        node = markdown_to_html_node('''# Heading\n\nAnd a paragraph''')
        self.assertEqual(node.to_html(), '''<div><h1>Heading</h1><p>And a paragraph</p></div>''')

    def test_headings(self):
        node = markdown_to_html_node('''# Heading\n## Heading 2''')
        self.assertEqual(node.to_html(), '''<div><h1>Heading</h1><h2>Heading 2</h2></div>''')

    def test_code(self):
        node = markdown_to_html_node('''```fmt.Println("Hello, world!")```''')
        self.assertEqual(node.to_html(), '''<div><code>fmt.Println("Hello, world!")</code></div>''')

    def test_multiline_code(self):
        node = markdown_to_html_node("""```
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```""")
        self.assertEqual(node.to_html(), '''<div><code>
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
</code></div>''')

    def test_quote(self):
        node = markdown_to_html_node('''> Cite 1
> Cite 2''')
        self.assertEqual(node.to_html(), '''<div><blockquote><p>Cite 1</p><p>Cite 2</p></blockquote></div>''')

    def test_unordered_list(self):
        node = markdown_to_html_node('''* Item 1
* Item 2''')
        self.assertEqual(node.to_html(), '''<div><ul><li>Item 1</li><li>Item 2</li></ul></div>''')

    def test_ordered_list(self):
        node = markdown_to_html_node('''1. Item 1
2. Item 2''')
        self.assertEqual(node.to_html(), '''<div><ol><li>Item 1</li><li>Item 2</li></ol></div>''')

    def test_complex(self):
        with open(os.path.join(__location__, "complex.md")) as f:
            md = f.read()
            node = markdown_to_html_node(md)
            self.assertEqual(node.to_html(),'''<div><h1>Welcome to Markdown</h1><p>Markdown is a lightweight markup language that you can use to add formatting elements to plaintext text documents.</p><h2>How to use this?</h2><ol><li>Write markdown in the markdown editor window</li><li>See the rendered markdown in the preview window</li></ol><h3>Features</h3><ul><li>Create headings, paragraphs, links, blockquotes, inline-code, code blocks, and lists</li><li>Name and save the document to access again later</li><li>Choose between Light or Dark mode depending on your preference</li></ul><blockquote><p>This is an example of a blockquote. If you would like to learn more about markdown syntax, you can visit this <a href="https://www.markdownguide.org/cheat-sheet/">markdown cheatsheet</a>.</p></blockquote><h4>Headings</h4><p>To create a heading, add the hash sign (#) before the heading. The number of number signs you use should correspond to the heading level. You'll see in this guide that we've used all six heading levels (not necessarily in the correct way you should use headings!) to illustrate how they should look.</p><h5>Lists</h5><p>You can see examples of ordered and unordered lists above.</p><h6>Code Blocks</h6><p>This markdown editor allows for inline-code snippets, like this: <code>I'm inline</code>. It also allows for larger code blocks like this</p><code>
<main>
  <h1>This is a larger code block</h1>
</main>
</code></div>''')
