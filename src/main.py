import re, os, shutil
from enum import Enum 
from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from blocks import *

def main():
	copy_static_files("./static", "./public")
	generate_pages_recursive("./content", "./static/template.html", "./public")
	
	"""print("hello world")
	tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
	print(f"{tn}")
	#copy_static_files("./static", "./public")
	print (f"{extract_title(""Aqui hay cosas
			   si pongo un no titulo aqui
			   ### seguro que estoy jodido
			   si no...
			   # Todo va bien 
			   pero pondremos algo mas""
			   )}")"""

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, log = ""):
	if not os.path.exists(dir_path_content):
		raise Exception("source directory does not exist")
	files = os.listdir(dir_path_content)
	for file in files:
		new_dst = os.path.join(dest_dir_path, file)
		new_src = os.path.join(dir_path_content, file)
		#print(f"file: {new_src} {not os.path.isfile(new_src)}")
		if not os.path.isfile(new_src):
			if not os.path.exists(new_dst):		
				os.mkdir(new_dst)
			#print(f"src file: {src} {not os.path.isfile(src)}")
			#print(f"dir: {new_src}")								
			print(f"{new_dst}\n")
			log += f"mkdir {new_dst}\n"
			log += generate_pages_recursive(new_src, template_path, new_dst, log)
		else:
			if os.path.splitext(new_src)[-1].lower() == '.md':
				new_dst = os.path.join(dest_dir_path, file)
				new_dst = os.path.splitext(new_dst)[:-1][0] + ".html"
				generate_page(new_src, template_path, new_dst)
				css_dir = os.path.dirname(template_path)
				#print(f"css dir {css_dir}")
				css_file = os.path.basename(file)					
				#print(f"css base {css_file}")
				css_file = os.path.splitext(css_file)[:-1][0]
				css_file += ".css"
				#print(f"css file {css_file}")
				src_css = os.path.join(css_dir, css_file)
				#print(f"src file {src_css}")
				#print(f"dst dir {dest_dir_path}")
				dst_css_file = os.path.join(dest_dir_path, css_file)
				print(f"css {css_file}")
				print(f"dst {dst_css_file}")
				shutil.copy(src_css, dst_css_file)
				log += f"generated {new_src}\n"
	print (f"generator: \n{log}")
	return log

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	contents = ""
	template = ""
	new_page = ""
	src = open(from_path, "r")
	#print(f"llegando a {src}")
	#print(f"imprimiendo: \ n {src.read()}")
	contents = src.read()
	#print(f"imprimiendo: \ n {contents}")
	src.close()
	#print(f"contents: {contents}")	
	html_string = markdown_to_html_node(contents).to_html()
	#print(f"html: {html_string}")	
	title = extract_title(contents)
	#print (f"el titulo: {title}")
	tplt = open(template_path, "r")
	template = tplt.read()	
	tplt.close()
	final = template.replace("{{ Content }}",html_string,1)
	final = final.replace("{{ Title }}",title,1)
	#print(f"{final}")
	print(f"dst path {dest_path}")
	dst = open(dest_path, "w")
	dst.write(final)
	dst.close()

def copy_static_files(src, dst, log = ""):
	if not os.path.exists(src):
		raise Exception("source directory does not exist")
	if log == "" and os.path.exists(dst):
		shutil.rmtree(dst)
		log += f"removed {dst}\n"
	if not os.path.exists(dst):		
		os.mkdir(dst)
		#print(f"src file: {src} {not os.path.isfile(src)}")
		files = os.listdir(src)
		for file in files:
			new_src = os.path.join(src, file)
			#print(f"file: {new_src} {not os.path.isfile(new_src)}")
			if not os.path.isfile(new_src):
				#print(f"dir: {new_src}")				
				new_dst = os.path.join(dst, file)
				log += f"{new_dst}\n"
				log += copy_static_files(new_src, new_dst, log)
			else:				
				shutil.copy(new_src,dst)
				#print(f"files: {new_src}")
				log += f"{new_src}\n"
		print (f"copy: \n{log}")
		return log

def extract_title(markdown):
	lines = markdown.split("\n")
	#print(f"{lines}")
	for line in lines:
		#print(f"{type(line)}  {line}")
		if line.strip().startswith("#") and not line.strip().startswith("##"):
			#print(f"este es {line}")
			return line.strip("#").strip()

def markdown_to_html_node(markdown):
	nodes = []
	count = 0
	blocks = markdown_to_blocks(markdown)
	#print(f"mkd: {markdown}")
	#print(f"all_blocks: {blocks}")
	for block in blocks:
		count += 1
		if len(block) > 0:			
			block_type = block_to_block_type(block)
		else:
			block_type = block_to_block_type("  ")
		#print(f"block_type {block_type}")
		tag = get_tag(block[:5],block_type)
		block=block.strip("#").strip()
		block=block.strip(">").strip()
		#print(f"blocks {block}{tag}")
		if block_type == BlockType.CODE:
			code_node = TextNode(block.strip("`"), TextType.CODE)
			#print(f"coden {code_node}")
			leaf_node = text_node_to_html_node(code_node)
			#print(f"leaf: {leaf_node}")
			nodes.append(ParentNode("pre",[leaf_node]))
			#print(f"a {count}")
			#print(f"nds {nodes}")
		elif block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
			#print(f"block {block}")
			child_nodes = text_to_children_list(block)
			parent = ParentNode(tag, child_nodes)
			nodes.append(parent)
			#print(f"b {count}")
		else:
			#print(f"block {block}")
			child_nodes = text_to_children(block)
			#print(f"a {child_nodes}")
			parent = ParentNode(tag, child_nodes)
			nodes.append(parent)
			#print(f"c {parent} co{count}")
	#print(f"nds G {nodes}")
	parent_node = ParentNode("div", nodes)
	#print(f"nodes_text: {parent_node}")
	#print(f"html_text: {parent_node.to_html()}")
	return parent_node

def text_to_children(text):
	children_nodes = []
	nodes = text_to_textnodes(text)
	#print(f"ttc {nodes}")
	for node in nodes:		
		children_nodes.append(text_node_to_html_node(node))
	return children_nodes

def text_to_children_list(text):
	children_nodes = []
	lines = text.split("\n")
	for line in lines:
		line = line.strip("-").strip()
		matches = re.findall(r"([0-9]*\. )(.*?)", line)
		#print(f"m {matches} {len(matches)}")
		if len(matches) > 0:
			line = line.strip(matches[0][0])
			#print(f"l{line}")
		nodes = text_to_textnodes(line)
		c_nodes = []
		for node in nodes:
			c_nodes.append(text_node_to_html_node(node))
		children_nodes.append(ParentNode("li", c_nodes))
	return children_nodes

def get_tag(tag, block_type):
	match block_type:
		case BlockType.CODE:
			return "code"
		case BlockType.PARAGRAPH:
			return "p"
		case BlockType.HEADING:
			count = 0
			for item in tag:
				if tag[0] == "#":
					count += 1
					tag = tag[1:]
			new_tag = f"h{count}"
			return new_tag
		case BlockType.QUOTE:
			return "blockquote"
		case BlockType.UNORDERED_LIST:
			return "ul"
		case BlockType.ORDERED_LIST:
			return "ol"

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			leaf = LeafNode(None, text_node.text, None)
			return leaf
		case TextType.BOLD:
			leaf = LeafNode("b", text_node.text)
			return leaf
		case TextType.ITALIC:
			leaf = LeafNode("i", text_node.text)
			return leaf
		case TextType.CODE:
			leaf = LeafNode("code", text_node.text)
			return leaf
		case TextType.LINK:
			leaf = LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
			return leaf
		case TextType.IMAGE:
			leaf = LeafNode("img", "", {"src" : text_node.url, "alt": text_node.text})
			#print(f"{leaf}")
			return leaf
		case _:
			raise Exception("incorrect text type")
		
def markdown_to_blocks(markdown):
	new_blocks = []
	new_blocks = markdown.split("\n\n")
	for block in new_blocks:
		block = block.strip()
	return new_blocks

def text_to_textnodes(text):
	new_nodes = []
	#print(f"tttnd: {text}")
	node = TextNode(text, TextType.TEXT)
	new_nodes = split_nodes_delimiter(
					split_nodes_delimiter(
						split_nodes_delimiter(
							split_nodes_delimiter(
								split_nodes_link(
									split_nodes_image([node])
								)		
							, "`", TextType.CODE)
						, "_", TextType.ITALIC)
					, "**", TextType.BOLD)
				, ">", TextType.TEXT)
	#print(f"nodes tttnd: {new_nodes}")
	return new_nodes

def extract_markdown_images(text):
	matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
	#print(f"mat: {matches}" 	)
	return matches

def extract_markdown_link(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	#print(matches)
	return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	final_nodes = []
	for item in old_nodes:
		new_nodes = []
		#item.text = item.text.strip("\n")
		if item.text_type != TextType.TEXT:
			new_nodes.append(item)
		else:
			strings = item.text.split(delimiter)
			counter = 1
			d = check_delimiter(delimiter)
			for item in strings:
				if counter % 2 == 1:
					node = TextNode(item, TextType.TEXT)
				if counter % 2 == 0:
					node = TextNode(item, text_type)	
				new_nodes.append(node)
				counter += 1
		final_nodes.extend(new_nodes)
	#print (f"m {final_nodes}")
	return final_nodes

def split_nodes_image(old_nodes):
	new_nodes = []
	#print("a")
	for node in old_nodes:
		#print("b")
		if node.text_type != TextType.TEXT:
			#print("c")
			new_nodes.append(node)
		else:
			#print("d")
			text = node.text
			matches = extract_markdown_images(text)
			for match in matches:
				match_text =(f"![{match[0]}]({match[1]})")
				"""print(f"e   {node}")
				print(f"e   {match}")
				print(f"e   {match_text}")
				print(f"e   {node.text}")
				print(f"e   {text.split("!")}")
				print(f"e   {text.split("!")[0]}")"""
				new_nodes.append(TextNode((text.split(match_text)[0]),TextType.TEXT))
				#print("f")
				new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
				#print(f"g  {text}")
				if len(text.split(match_text)) > 1:
					#print(f"h  {text}")
					text = text.split(match_text)[1]
				else:
					text = ""
			if text != "":
				new_nodes.append(TextNode(text, TextType.TEXT))
	#print(f"k {new_nodes}")
	return new_nodes
	
def split_nodes_link(old_nodes):
	new_nodes = []
	#print("a")
	for node in old_nodes:
		#print("b")
		if node.text_type != TextType.TEXT:
			#print("c")
			new_nodes.append(node)
		else:
			#print("d")
			text = node.text
			matches = extract_markdown_link(text)
			for match in matches:
				match_text =(f"[{match[0]}]({match[1]})")
				"""print(f"e   {node}")
				print(f"e   {match}")
				print(f"e   {match_text}")
				print(f"e   {node.text}")
				print(f"e   {text.split("!")}")
				print(f"e   {text.split("!")[0]}")"""
				new_nodes.append(TextNode((text.split(match_text)[0]),TextType.TEXT))
				#print("f")
				new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
				#print(f"g  {text}")
				if len(text.split(match_text)) > 1:
					#print(f"h  {text}")
					text = text.split(match_text)[1]
				else:
					text = ""
			if text != "":
				new_nodes.append(TextNode(text, TextType.TEXT))
	#print(f"k {new_nodes}")
	return new_nodes

def check_delimiter(delimiter):
	match(delimiter):
		case "`":
			return TextType.CODE
		case "**":
			return TextType.BOLD
		case "_":
			return TextType.ITALIC
		case ">":
			return TextType.TEXT
		case _:
			raise Exception("Invalid Markdown syntax")
		
main()
 