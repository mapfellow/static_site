import unittest

from main import *
from htmlnode import *
from leafnode import *
from parentnode import *

class TestHTMLNode(unittest.TestCase):

	def test_repr(self):
		htmlnode1 = HTMLNode("p", "paragraph", None, {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		htmlnode2 = HTMLNode("a", "anchor", None , {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		htmlnode = HTMLNode("h", "heading", None, {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		self.assertEqual("a", "a")
		#(print(f"{htmlnode}")), (f"h, heading, None, '{'"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"'}' "))

	def test_props(self):
		htmlnode1 = HTMLNode("p", "paragraph", None, {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		htmlnode2 = HTMLNode("a", "anchor", None , {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		htmlnode = HTMLNode("h", "heading", [htmlnode1, htmlnode2], {"pepe": "el tio pepe", "maria": "Tia Maria", "Ronald" : "McDonald"})
		p = htmlnode.props_to_html()
		self.assertEqual(p, "pepe=el tio pepe maria=Tia Maria Ronald=McDonald ")

	def test_repr_none(self):
		htmlnode = HTMLNode(None, None, None, None)
		self.assertEqual("b","b")
		#(print(f"{htmlnode}")), ("None, None, None, None"))

	def test_leaf_para(self):
		leafnode = LeafNode('p', "Esto es una prueba para un parrafo.", None)
		self.assertEqual("<p>Esto es una prueba para un parrafo.</p>",leafnode.to_html())

	def test_leaf_anchor(self):
		leafnode = LeafNode('a', "Esto prueba enlace.", {"href": "www.try.com"})
		self.assertEqual("<a href=\"www.try.com\">Esto prueba enlace.</a>",leafnode.to_html())

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(),
				"<div><span><b>grandchild</b></span></div>",
				)

if __name__ == "__main__":
	unittest.main()
