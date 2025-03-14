import unittest

from main import *


class MainFunctionsTest(unittest.TestCase):

	def test_split_code(self):
		node = TextNode("This is a `text` node", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
		test_node1 = TextNode("This is a ", TextType.TEXT)
		test_node2 = TextNode("text", TextType.CODE)
		self.assertEqual(new_nodes[0],test_node1)
		self.assertEqual(new_nodes[1],test_node2)

	def test_split_bold(self):
		node = TextNode("This is a **text** node", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
		test_node1 = TextNode("This is a ", TextType.TEXT)
		test_node2 = TextNode("text", TextType.BOLD)
		self.assertEqual(new_nodes[0],test_node1)
		self.assertEqual(new_nodes[1],test_node2)
	
	def test_split_italic(self):
		node = TextNode("This is a _text_ node", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
		test_node1 = TextNode("This is a ", TextType.TEXT)
		test_node2 = TextNode("text", TextType.ITALIC)
		self.assertEqual(new_nodes[0],test_node1)
		self.assertEqual(new_nodes[1],test_node2)

	def test_total_splitter(self):
		node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
		new_nodes = text_to_textnodes(node.text)
		self.assertEqual(new_nodes,[TextNode("This is ", TextType.TEXT),
    								TextNode("text", TextType.BOLD),
    								TextNode(" with an ", TextType.TEXT),
    								TextNode("italic", TextType.ITALIC),
    								TextNode(" word and a ", TextType.TEXT),
    								TextNode("code block", TextType.CODE),
								    TextNode(" and an ", TextType.TEXT),
    								TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    								TextNode(" and a ", TextType.TEXT),
    								TextNode("link", TextType.LINK, "https://boot.dev"),
									]
						)

if __name__ == "__main__":
	unittest.main()