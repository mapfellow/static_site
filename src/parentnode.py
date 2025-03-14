from htmlnode import *
from leafnode import *

class ParentNode(HTMLNode):
	
	def __init__(self, tag, children, value = None, props = None):
		super().__init__(tag, value, children, props= None)
		self.tag = tag
		self.children = children
		self.props = props
		
	def to_html(self):
		if self.tag is None:
			raise ValueError("tag is needed")
		if self.children is None:
			raise ValueError("children is needed")
		html_string = f"<{self.tag}"
		if self.props is not None:
			props = ""
			for item in self.props:
				props += f'{item}="{self.props[item]}" '
			html_string += f"{props.strip()}"
			#print("que haces aqui?")
		html_string += f">"
		#print(f"hijos: {self.children} tamaño: {len(self.children)}")
			#print(f"tipo padre: {type(item)} espera {ParentNode} {isinstance(item, ParentNode)} ")
		if isinstance(self.children, ParentNode):
			#print(f"padreaqui {item.to_html()}")
			html_string+= f"{self.children.to_html()}"		
		else:
			for item in self.children:		
			#if isinstance(item, LeafNode):	
				#print (f"	0 partohtml \n{item}")
				html_string += item.to_html()
				#print (f"a partohtml {html_string}")
		html_string += f"</{self.tag}>"
		#print (f"partohtml {html_string}")
		return html_string
