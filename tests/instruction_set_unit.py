import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import main modules
import instruction_set

instruction_set = instruction_set.InstructionSet()

class MnemonicsTests( unittest.TestCase ):
    
    def test_mnemonics_initialise(self):
        instruction_set.initialise()
        self.assertTrue( len(instruction_set._instructions) == 0 )

    
    def test_mnemonics_addInstruction(self):
        val = instruction_set.addInstruction('LDA', 'Load to the accumulator')
        self.assertTrue(val)

        val = instruction_set.addInstruction('LDA', 'Load to the accumulator')
        self.assertFalse(val)
        
        instruction_set.initialise()


    def test_mnemonics_isInstruction( self ):
        val = instruction_set.addInstruction('LDA', 'Load to the accumulator')
        self.assertTrue(val)

        val = instruction_set.isInstruction( "LDA" )
        self.assertTrue(val)

        val = instruction_set.isInstruction( "BOO" )
        self.assertFalse(val)

        instruction_set.initialise()


    def test_mnemonics_getInstruction( self ):
        
        val = instruction_set.addInstruction('LDA', 'Load to the accumulator')
        self.assertTrue(val)

        val = instruction_set.getInstruction( "LDA" )
        self.assertIsNotNone(val)

        val = instruction_set.getInstruction( "BOO" )
        self.assertTrue(val == None)

        instruction_set.initialise()


    def test_mnemonics_addOpcode( self ):
        val = instruction_set.addInstruction('LDA', 'Load to the accumulator')
        self.assertTrue(val)

        val = instruction_set.addOpcode( "LDA", instruction_set.addressing_mode_Immediate, 169 )
        self.assertTrue(val, "Instruction was correctly added")

        val = instruction_set.getInstruction( "LDA" )
        self.assertIsNotNone(val, "Correctly reloaded the instruction")

        self.assertTrue( instruction_set.addressing_mode_Immediate in val["addressing_modes"] )

        self.assertTrue( val["addressing_modes"][instruction_set.addressing_mode_Immediate] == 169 )
        
        instruction_set.initialise()


    def test_mnemonics_get_instruction_length(self):
        # Implied
        val = instruction_set.get_instruction_length(0)
        self.assertEqual(val, 1)

        # Immediate
        val = instruction_set.get_instruction_length(1)
        self.assertEqual(val, 2)

        # Absolute X
        val = instruction_set.get_instruction_length(2)
        self.assertEqual(val, 3)

        # Absolute Y
        val = instruction_set.get_instruction_length(3)
        self.assertEqual(val, 3)
        
        # Absolute
        val = instruction_set.get_instruction_length(4)
        self.assertEqual(val, 3)

        # Accumulator
        val = instruction_set.get_instruction_length(5)
        self.assertEqual(val, 1)

        # Zero Page X
        val = instruction_set.get_instruction_length(6)
        self.assertEqual(val, 2)
        
        # Zero Page Y
        val = instruction_set.get_instruction_length(7)
        self.assertEqual(val, 2)
        
        # Zero Page
        val = instruction_set.get_instruction_length(8)
        self.assertEqual(val, 2)

        # Indirect Indexed Y
        val = instruction_set.get_instruction_length(9)
        self.assertEqual(val, 2)

        # Indirect
        val = instruction_set.get_instruction_length(10)
        self.assertEqual(val, 3)

        # Indexed Indirect X
        val = instruction_set.get_instruction_length(11)
        self.assertEqual(val, 2)

        # Relative
        val = instruction_set.get_instruction_length(12)
        self.assertEqual(val, 2)


    def test_mnemonics_loadInstructions(self):
        instruction_set.loadInstructions()

        self.assertEqual( len( instruction_set._instructions ), 56 )

        instruction_set.initialise()

if __name__ == '__main__':
    unittest.main()