import unittest

from main import *


class TestTextNode(unittest.TestCase):

	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_eq_url(self):
		node = TextNode("This is a text node", TextType.BOLD, "www.try.com")
		node2 = TextNode("This is a text node", TextType.BOLD, "www.try.com")
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is another text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_eq_None(self):
		node = TextNode("This is a text node", TextType.BOLD, None)
		node2 = TextNode("This is a text node", TextType.BOLD, None)
		self.assertEqual(node, node2)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
	unittest.main()
