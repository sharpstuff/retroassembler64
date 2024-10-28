import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import main modules
import assembler

asm64 = assembler.Assembler()

class AssemblerTests( unittest.TestCase ):

    # ASSEMBLER

    def test_assembler_output(self):
        
        with open("fixtures/border.asm", "r") as f:
            expected = bytearray([0xa2, 0x00, 0x8e, 0x20, 0xd0, 0xe8, 0xe0, 0x10, 0xd0, 0xf8, 0xa2, 0x00, 0x4c, 0x02, 0xc0, 0x60  ])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")
            
        with open("fixtures/labels.asm", "r") as f:
            expected = bytearray([0xad, 0x00, 0xc0, 0xa2, 0xf8, 0xa9, 0x15, 0xa9, 0xc0, 0x8e, 0x00, 0xc0, 
                                  0xe8, 0xe0, 0x10, 0xd0, 0x01, 0x60, 0x4c, 0x05, 0xc0, 0xa9, 0x65, 0x8d, 
                                  0x20, 0xd0, 0x60, 0xaa, 0xde, 0xad, 0xbe, 0xef, 0xaa, 0x55, 0xaa, 0x55, 
                                  0x4c, 0x05, 0xc0])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")

        with open("fixtures/hires.asm", "r") as f:
            expected = bytearray([0xa9, 0x00, 0x85, 0xfb, 0xa9, 0x20, 0x85, 0xfc, 0xa9, 0x08, 0x0d, 0x18, 0xd0, 0x8d, 0x18, 0xd0, 
                                  0xa9, 0x20, 0x0d, 0x11, 0xd0, 0x8d, 0x11, 0xd0, 0xa9, 0x00, 0xa0, 0x00, 0x91, 0xfb, 0xe6, 0xfb, 
                                  0xa6, 0xfb, 0xe0, 0xff, 0xd0, 0xf6, 0x91, 0xfb, 0x85, 0xfb, 0xe6, 0xfc, 0xa6, 0xfc, 0xe0, 0x3f, 
                                  0xd0, 0xea, 0x60])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")       

    def test_calculate_relative_offset(self):
        offset = asm64.calculate_relative_offset(0xC010, 0xC020)
        self.assertEqual(offset, 14)
        offset = asm64.calculate_relative_offset(0xC020, 0xC010)
        self.assertEqual(offset, 238)

if __name__ == '__main__':
        unittest.main()