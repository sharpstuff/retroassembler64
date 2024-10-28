import unittest
import assembler
import parse6510

class AssemblerTests( unittest.TestCase ):

# PENDING TEST COVERAGE
#
# def matches_addressing_mode( token, addressing_mode ): - cover all modes

    # PARSING

    def test_parse6510_parse(self):
        matches = parse6510.parse( 'LDA' )
        self.assertEqual( len(matches), 1 )
        self.assertEqual( matches[0], 'LDA' )

    def test_parse6510_matches_addressing_mode(self):
        # Immediate
        val = parse6510.matches_addressing_mode("#$65", 1 )
        self.assertTrue(val, True)

        # Absolute X
        val = parse6510.matches_addressing_mode("$D020,X", 2 )
        self.assertTrue(val, True)

        # Absolute Y
        val = parse6510.matches_addressing_mode("$D020,Y", 3 )
        self.assertTrue(val, True)
        
        # Absolute
        val = parse6510.matches_addressing_mode("$D020", 4 )
        self.assertTrue(val, True)

        # Accumulator
        val = parse6510.matches_addressing_mode("A", 5 )
        self.assertTrue(val, True)

        # Zero Page X
        val = parse6510.matches_addressing_mode("$20,X", 6 )
        self.assertTrue(val, True)

        # Zero Page Y
        val = parse6510.matches_addressing_mode("$20,Y", 7 )
        self.assertTrue(val, True)

        # Zero Page
        val = parse6510.matches_addressing_mode("$20", 8 )
        self.assertTrue(val, True)

        # Indirect indexed
        val = parse6510.matches_addressing_mode("($20),Y", 9 )
        self.assertTrue(val, True)

        # Indirect
        val = parse6510.matches_addressing_mode("($D020)", 10 )
        self.assertTrue(val, True)

        # Indexed indirect
        val = parse6510.matches_addressing_mode("($20,X)", 11 )
        self.assertTrue(val, True)

        val = parse6510.matches_addressing_mode("$20", 12 )
        self.assertTrue(val, True)



    # PARSING OPERANDS

    def test_parse6510_is_byte(self):
        val = parse6510.is_byte("$DE")
        self.assertTrue(val)

        val = parse6510.is_byte("hy")
        self.assertFalse(val)

    def test_parse6510_parse_byte(self):
        bytes = parse6510.parse_byte("$10")
        self.assertEqual( len(bytes), 1 )
        self.assertEqual( bytes[0], 16 )

    def test_parse6510_is_word(self):
        val = parse6510.is_word("$DEAD")
        self.assertTrue(val)
        val = parse6510.is_word("pete")
        self.assertFalse(val)

    def test_parse6510_parse_word_little_endian(self):
        words = parse6510.parse_word_little_endian("$DEAD")
        self.assertEqual( words[0], 173 )
        self.assertEqual( words[1], 222 )
    
    def test_parse6510_parse_word_big_endian(self):
        words = parse6510.parse_word_big_endian("$DEAD")
        self.assertEqual( words[0], 222 )
        self.assertEqual( words[1], 173 )

    def test_parse6510_parse_bytestring(self):
        bytes = parse6510.parse_bytestring("$00 $11 $22 $33 $44 $55 $66 $77")

    def test_parse6510_word_to_int(self):
        val = parse6510.word_to_int("$D020")
        self.assertEqual(val, 53280)

    # LABELS

    def test_parse6510_is_label_declaration(self):
        
        val = parse6510.is_label_declaration("isr:")
        self.assertTrue(val) 

        val = parse6510.is_label_declaration("isr")
        self.assertFalse(val) 

        val = parse6510.is_label_declaration("<isr")
        self.assertFalse(val)
    
        val = parse6510.is_label_declaration(">isr")
        self.assertFalse(val)


    def test_parse6510_is_label_reference(self):

        val = parse6510.is_label_reference("isr")
        self.assertTrue(val)
        
        val = parse6510.is_label_reference("<isr")
        self.assertTrue(val)
    
        val = parse6510.is_label_reference(">isr")
        self.assertTrue(val)

        val = parse6510.is_label_reference("$FE")
        self.assertFalse(val)

        val = parse6510.is_label_reference("isr:")
        self.assertFalse(val)


    # VARIABLES
    
    def test_parse6510_is_variable_declaration(self):

        val = parse6510.is_variable_declaration("FOO = ")
        self.assertTrue(val)

        val = parse6510.is_variable_declaration("FOO")
        self.assertFalse(val)


    def test_parse6510_is_variable_reference(self):

        val = parse6510.is_variable_reference("FOO")
        self.assertTrue(val)

        val = parse6510.is_variable_reference("<FOO")
        self.assertTrue(val)

        val = parse6510.is_variable_reference(">FOO")
        self.assertTrue(val)

        val = parse6510.is_variable_reference("FOO:")
        self.assertFalse(val)


    def test_parse6510_get_variable_name_from_declaration(self):

        val = parse6510.get_variable_name_from_declaration("FOO = ")
        self.assertEqual(val, "FOO")

    # DIRECTIVES

    def test_parse6510_is_org_directive(self):
        val = parse6510.is_org_directive(".org $C000")
        self.assertTrue(val)

    # BYTESTRINGS

    def test_parse6510_is_bytestring_declaration(self):
        val = parse6510.is_bytestring_declaration(".byte $00 $11 $22 $33")
        self.assertTrue(val)

    def test_parse6510_is_wordstring_declaration(self):
        val = parse6510.is_wordstring_declaration(".word $DEAD $BEEF")
        self.assertTrue(val)

    # MODIFIERS

    def test_parse6510_is_high_low_byte_extract(self):
        val = parse6510.is_high_low_byte_extract("<isr")
        self.assertTrue(val)

        val = parse6510.is_high_low_byte_extract(">isr")
        self.assertTrue(val)

        val = parse6510.is_high_low_byte_extract("isr")
        self.assertFalse(val)


    def test_parse6510_extract_high_low_byte(self):
        val = parse6510.extract_high_low_byte("<isr", "$C020")
        self.assertEqual(val, 32)

        val = parse6510.extract_high_low_byte(">isr", "$C020")
        self.assertEqual(val, 192)

        val = parse6510.extract_high_low_byte("isr", "$C020")
        self.assertEqual(val, None)

    # ASSEMBLER

    def test_assembler_output(self):
        
        with open("fixtures/border.asm", "r") as f:
            expected = bytearray([0xa2, 0x00, 0x8e, 0x20, 0xd0, 0xe8, 0xe0, 0x10, 0xd0, 0xf8, 0xa2, 0x00, 0x4c, 0x02, 0xc0, 0x60  ])
            source = f.read()
            actual = assembler.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")
            
        with open("fixtures/labels.asm", "r") as f:
            expected = bytearray([0xad, 0x00, 0xc0, 0xa2, 0xf8, 0xa9, 0x15, 0xa9, 0xc0, 0x8e, 0x00, 0xc0, 
                                  0xe8, 0xe0, 0x10, 0xd0, 0x01, 0x60, 0x4c, 0x05, 0xc0, 0xa9, 0x65, 0x8d, 
                                  0x20, 0xd0, 0x60, 0xaa, 0xde, 0xad, 0xbe, 0xef, 0xaa, 0x55, 0xaa, 0x55, 
                                  0x4c, 0x05, 0xc0])
            source = f.read()
            actual = assembler.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")

        with open("fixtures/hires.asm", "r") as f:
            expected = bytearray([0xa9, 0x00, 0x85, 0xfb, 0xa9, 0x20, 0x85, 0xfc, 0xa9, 0x08, 0x0d, 0x18, 0xd0, 0x8d, 0x18, 0xd0, 
                                  0xa9, 0x20, 0x0d, 0x11, 0xd0, 0x8d, 0x11, 0xd0, 0xa9, 0x00, 0xa0, 0x00, 0x91, 0xfb, 0xe6, 0xfb, 
                                  0xa6, 0xfb, 0xe0, 0xff, 0xd0, 0xf6, 0x91, 0xfb, 0x85, 0xfb, 0xe6, 0xfc, 0xa6, 0xfc, 0xe0, 0x3f, 
                                  0xd0, 0xea, 0x60])
            source = f.read()
            actual = assembler.run(source, 0xC000 )
            
            self.assertEqual(len(expected), len(actual), "Expected byte array length not same as fixture")
            self.assertEqual(expected, actual, "Expected byte array does not match fixture")        

    def test_calculate_relative_offset(self):
        offset = assembler.calculate_relative_offset(0xC010, 0xC020)
        self.assertEqual(offset, 14)
        offset = assembler.calculate_relative_offset(0xC020, 0xC010)
        self.assertEqual(offset, 238)

if __name__ == '__main__':
        unittest.main()