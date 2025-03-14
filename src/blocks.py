from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "p"
	HEADING = "h"
	CODE = "`"
	QUOTE = "q"
	UNORDERED_LIST = "ul"
	ORDERED_LIST = "ol"
	
def block_to_block_type(block):
	match (block[0]):
		case "#":
			return BlockType.HEADING
		case "`":
			return BlockType.CODE
		case ">":
			return BlockType.QUOTE
		case "-":
			return BlockType.UNORDERED_LIST
		case "1":
			return BlockType.ORDERED_LIST
		case _:
			return BlockType.PARAGRAPH