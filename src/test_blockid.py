import unittest

from main import *
from blocks import *

class Block_Id_Test(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "###This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "´´´This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = ">This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.QUOTE)
    
    def test_block_to_block_type_code(self):
        block = "-This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_code(self):
        block = "1. This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()