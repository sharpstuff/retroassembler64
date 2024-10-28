import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import parse_assembly

parser = parse_assembly.ParseAssembly()

class Parse6510Tests( unittest.TestCase ):

    # parse6510

    def test_parse6510_parse(self):
        matches = parser.parse( 'LDA #$65\nRTS' )
        self.assertEqual( len(matches), 3 )
        self.assertEqual( matches[0], 'LDA' )


    def test_parse6510_matches_addressing_mode_immediate(self):
        for am in range(1,12):
            val = parser.matches_addressing_mode("#$65", am )
            if ( am == 1 ):
                self.assertTrue(val)
            else:
                self.assertFalse(val)

    def test_parse6510_matches_addressing_mode_absolute(self):

        for am in range(1,12):

            # Absolute X
            val = parser.matches_addressing_mode("$D020,X", am )
            if ( am == 2 ):
                self.assertTrue(val, True)
            else:
                self.assertFalse(val, False)

            # Absolute Y
            val = parser.matches_addressing_mode("$D020,Y", am )
            if ( am == 3 ):
                self.assertTrue(val, True)
            else:
                self.assertFalse(val, False)
            
            # Absolute
            val = parser.matches_addressing_mode("$D020", am )
            if ( am == 4 ):
                self.assertTrue(val, True)
            else:
                self.assertFalse(val, False)


    def test_parse6510_matches_addressing_mode_accumulator(self):
        
        for am in range(1,12):

            val = parser.matches_addressing_mode("A", am )

            if ( am == 5 ):
                self.assertTrue(val, True)
            else:
                self.assertFalse(val, False)

    def test_parse6510_matches_addressing_mode_zero_page(self):

        # Zero Page X
        val = parser.matches_addressing_mode("$20,X", 6 )
        self.assertTrue(val, True)

        # Zero Page Y
        val = parser.matches_addressing_mode("$20,Y", 7 )
        self.assertTrue(val, True)

        # Zero Page
        val = parser.matches_addressing_mode("$20", 8 )
        self.assertTrue(val, True)

    def test_parse6510_matches_addressing_mode_indexed(self):

        # Indirect indexed
        val = parser.matches_addressing_mode("($20),Y", 9 )
        self.assertTrue(val, True)

        # Indirect
        val = parser.matches_addressing_mode("($D020)", 10 )
        self.assertTrue(val, True)

        # Indexed indirect
        val = parser.matches_addressing_mode("($20,X)", 11 )
        self.assertTrue(val, True)

    def test_parse6510_matches_addressing_mode_relative(self):
        val = parser.matches_addressing_mode("$20", 12 )
        self.assertTrue(val, True)



    # PARSING OPERANDS

    def test_parse6510_is_byte(self):
        val = parser.is_byte("$DE")
        self.assertTrue(val)

        val = parser.is_byte("hy")
        self.assertFalse(val)

    def test_parse6510_parse_byte(self):
        bytes = parser.parse_byte("$10")
        self.assertEqual( len(bytes), 1 )
        self.assertEqual( bytes[0], 16 )

    def test_parse6510_is_word(self):
        val = parser.is_word("$DEAD")
        self.assertTrue(val)
        val = parser.is_word("pete")
        self.assertFalse(val)

    def test_parse6510_parse_word_little_endian(self):
        words = parser.parse_word_little_endian("$DEAD")
        self.assertEqual( words[0], 173 )
        self.assertEqual( words[1], 222 )
    
    def test_parse6510_parse_word_big_endian(self):
        words = parser.parse_word_big_endian("$DEAD")
        self.assertEqual( words[0], 222 )
        self.assertEqual( words[1], 173 )

    def test_parse6510_parse_bytestring(self):
        bytes = parser.parse_bytestring("$00 $11 $22 $33 $44 $55 $66 $77")

    def test_parse6510_word_to_int(self):
        val = parser.word_to_int("$D020")
        self.assertEqual(val, 53280)

    # LABELS

    def test_parse6510_is_label_declaration(self):
        
        val = parser.is_label_declaration("isr:")
        self.assertTrue(val) 

        val = parser.is_label_declaration("isr")
        self.assertFalse(val) 

        val = parser.is_label_declaration("<isr")
        self.assertFalse(val)
    
        val = parser.is_label_declaration(">isr")
        self.assertFalse(val)


    def test_parse6510_is_label_reference(self):

        val = parser.is_label_reference("isr")
        self.assertTrue(val)
        
        val = parser.is_label_reference("<isr")
        self.assertTrue(val)
    
        val = parser.is_label_reference(">isr")
        self.assertTrue(val)

        val = parser.is_label_reference("$FE")
        self.assertFalse(val)

        val = parser.is_label_reference("isr:")
        self.assertFalse(val)


    # VARIABLES
    
    def test_parse6510_is_variable_declaration(self):

        val = parser.is_variable_declaration("FOO = ")
        self.assertTrue(val)

        val = parser.is_variable_declaration("FOO")
        self.assertFalse(val)


    def test_parse6510_is_variable_reference(self):

        val = parser.is_variable_reference("FOO")
        self.assertTrue(val)

        val = parser.is_variable_reference("<FOO")
        self.assertTrue(val)

        val = parser.is_variable_reference(">FOO")
        self.assertTrue(val)

        val = parser.is_variable_reference("FOO:")
        self.assertFalse(val)


    def test_parse6510_get_variable_name_from_declaration(self):

        val = parser.get_variable_name_from_declaration("FOO = ")
        self.assertEqual(val, "FOO")

    # DIRECTIVES

    def test_parse6510_is_org_directive(self):
        val = parser.is_org_directive(".org $C000")
        self.assertTrue(val)

    # BYTESTRINGS

    def test_parse6510_is_bytestring_declaration(self):
        val = parser.is_bytestring_declaration(".byte $00 $11 $22 $33")
        self.assertTrue(val)

    def test_parse6510_is_wordstring_declaration(self):
        val = parser.is_wordstring_declaration(".word $DEAD $BEEF")
        self.assertTrue(val)

    # MODIFIERS

    def test_parse6510_is_high_low_byte_extract(self):
        val = parser.is_high_low_byte_extract("<isr")
        self.assertTrue(val)

        val = parser.is_high_low_byte_extract(">isr")
        self.assertTrue(val)

        val = parser.is_high_low_byte_extract("isr")
        self.assertFalse(val)


    def test_parse6510_extract_high_low_byte(self):
        val = parser.extract_high_low_byte("<isr", "$C020")
        self.assertEqual(val, 32)

        val = parser.extract_high_low_byte(">isr", "$C020")
        self.assertEqual(val, 192)

        val = parser.extract_high_low_byte("isr", "$C020")
        self.assertEqual(val, None) 

if __name__ == '__main__':
        unittest.main()