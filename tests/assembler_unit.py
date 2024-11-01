import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import main modules
import assembler
import instruction_set

asm64 = assembler.Assembler()

class AssemblerTests( unittest.TestCase ):

    _instruction_set = instruction_set.InstructionSet()

    # ASSEMBLER


    def test_parse_implied_instruction(self):
        
        asm64.reset()

        self._instruction_set.loadInstructions()

        current_instruction = self._instruction_set.getInstruction("RTS")
        self.assertIsNotNone(current_instruction)
        
        asm64.parse_implied_instruction( current_instruction )

        self.assertTrue( len(asm64._assembly_output) == 1 )
        self.assertEqual( asm64._assembly_output[0], 96 )
        
        # Teardown
        self._instruction_set.initialise()
        asm64.reset()


    def test_parse_label_declaration(self):
        self._address = "$c000"
        asm64.reset()

        asm64.parse_label_declaration("loop:")

        self.assertTrue( "loop:" in asm64._labels )
        
        self.assertTrue( asm64._labels["loop:" ] != None )
        self.assertTrue( asm64._labels["loop:" ] == "$c000" )

        asm64.reset()


    def test_parse_variable_declaration(self):

        asm64.reset()

        asm64.parse_variable_declaration( "foo", "5" )

        self.assertTrue( "foo" in asm64._labels )
        self.assertTrue( asm64._labels["foo" ] == "5" )

        asm64.reset()


    def test_parse_label_reference(self):

        self._address = "$c000"
        asm64.reset()

        asm64.parse_label_declaration("loop:")

        val = asm64.parse_label_reference("loop", asm64.MODE_PRESCAN )


    def test_parse_org_directive(self):

        matches = ['.org', '$d000']

        idx = asm64.parse_org_directive(matches, 0)

        self.assertEqual(asm64._base_address, 0xD000)


    def test_parse_relative_address(self):

        val = asm64.parse_relative_address( "$C010", 0xC000, asm64.MODE_ASSEMBLE )

        self.assertEqual(val, '$0e')


    def test_parse_wordstring(self):

        matches = [".word", "$DEAD", "$beef", "RTS" ]
        
        self._address = "$c000"
        asm64.reset()
        
        val = asm64.parse_wordstring(0xC000, matches, 0, asm64.MODE_ASSEMBLE )

        expected = bytearray([0xDE, 0xAD, 0xBE, 0xEF])

        self.assertEqual(len(expected), len(asm64._assembly_output) )
        self.assertEqual(expected, asm64._assembly_output )

        asm64.reset()


    def test_parse_bytestring(self):

        matches = [".byte", "$DE", "$AD", "$be", "$ef", "RTS" ]
        
        self._address = "$c000"
        asm64.reset()
        
        val = asm64.parse_bytestring(0xC000, matches, 0, asm64.MODE_ASSEMBLE )

        expected = bytearray([0xDE, 0xAD, 0xBE, 0xEF])

        self.assertEqual(len(expected), len(asm64._assembly_output) )
        self.assertEqual(expected, asm64._assembly_output )
        
        asm64.reset()


    def test_parse_string(self):
        matches = [".string",  "\"Dead Beef\"", "LDA"]
        
        self._address = "$c000"
        asm64.reset()

        val = asm64.parse_string(0xC000, matches, 0, asm64.MODE_ASSEMBLE )

        expected = bytearray([68, 101, 97, 100, 32, 66, 101, 101, 102, 0])
        
        self.assertEqual(len(expected), len(asm64._assembly_output) )
        self.assertEqual(expected, asm64._assembly_output )


    def test_set_base_address(self):

        asm64.set_base_address(0xD000)

        self.assertEqual(asm64._base_address, 0xD000)


    # INTEGRATION

    def test_assembler_output_BORDER(self):
        
        asm64.reset()

        with open("fixtures/border.asm", "r") as f:
            expected = bytearray([0x00, 0xc0, 0xa2, 0x00, 0x8e, 0x20, 0xd0, 0xe8, 0xe0, 0x10, 0xd0, 0xf8, 0xa2, 0x00, 0x4c, 0x02, 0xc0, 0x60 ])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "BORDER.ASM: Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "BORDER.ASM: Expected byte array does not match fixture")

        asm64.reset()


    def test_assembler_output_LABELS(self):
        
        asm64.reset()

        with open("fixtures/labels.asm", "r") as f:
            expected = bytearray([0x00, 0xc0, 0xad, 0x00, 0xc0, 0xa2, 0xf8, 0xa9, 0x15, 0xa9, 0xc0, 0x8e, 0x00, 0xc0, 
                                  0xe8, 0xe0, 0x10, 0xd0, 0x01, 0x60, 0x4c, 0x05, 0xc0, 0xa9, 0x65, 0x8d, 
                                  0x20, 0xd0, 0x60, 0xaa, 0xde, 0xad, 0xbe, 0xef, 0xaa, 0x55, 0xaa, 0x55, 
                                  0x4c, 0x05, 0xc0])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "LABELS.ASM: Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "LABELS.ASM: Expected byte array does not match fixture")
        
        asm64.reset()


    def test_assembler_output_HIRES(self):
        
        asm64.reset()

        with open("fixtures/hires.asm", "r") as f:

            expected = bytearray([0x00, 0xc0, 0xa9, 0x00, 0x85, 0xfb, 0xa9, 0x20, 0x85, 0xfc, 0xa9, 0x08, 0x0d, 0x18, 0xd0, 0x8d, 0x18, 0xd0, 
                                  0xa9, 0x20, 0x0d, 0x11, 0xd0, 0x8d, 0x11, 0xd0, 0xa9, 0x00, 0xa0, 0x00, 0x91, 0xfb, 0xe6, 0xfb, 
                                  0xa6, 0xfb, 0xe0, 0xff, 0xd0, 0xf6, 0x91, 0xfb, 0x85, 0xfb, 0xe6, 0xfc, 0xa6, 0xfc, 0xe0, 0x3f, 
                                  0xd0, 0xea, 0x60])
            source = f.read()
            actual = asm64.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "HIRES.ASM: Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "HIRES.ASM: Expected byte array does not match fixture")       

        asm64.reset()



    def test_calculate_relative_offset(self):
        offset = asm64.calculate_relative_offset(0xC010, 0xC020)
        self.assertEqual(offset, 14, "Testing forward relative offset")
        offset = asm64.calculate_relative_offset(0xC020, 0xC010)
        self.assertEqual(offset, 238, "Testing backward relative offset")

if __name__ == '__main__':
        unittest.main()