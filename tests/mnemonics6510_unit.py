import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import main modules
import mnemonics6510

class MnemonicsTests( unittest.TestCase ):
    
    def test_mnemonics_addInstruction(self):
        #val = mnemonics6510.addInstruction('LDA', 'Load to the accumulator')
        self.assertTrue(True)


    def test_mnemonics_get_instruction_length(self):
        # Implied
        val = mnemonics6510.get_instruction_length(0)
        self.assertEqual(val, 1)

        # Immediate
        val = mnemonics6510.get_instruction_length(1)
        self.assertEqual(val, 2)

        # Absolute X
        val = mnemonics6510.get_instruction_length(2)
        self.assertEqual(val, 3)

        # Absolute Y
        val = mnemonics6510.get_instruction_length(3)
        self.assertEqual(val, 3)
        
        # Absolute
        val = mnemonics6510.get_instruction_length(4)
        self.assertEqual(val, 3)

        # Accumulator
        val = mnemonics6510.get_instruction_length(5)
        self.assertEqual(val, 1)

        # Zero Page X
        val = mnemonics6510.get_instruction_length(6)
        self.assertEqual(val, 2)
        
        # Zero Page Y
        val = mnemonics6510.get_instruction_length(7)
        self.assertEqual(val, 2)
        
        # Zero Page
        val = mnemonics6510.get_instruction_length(8)
        self.assertEqual(val, 2)

        # Indirect Indexed Y
        val = mnemonics6510.get_instruction_length(9)
        self.assertEqual(val, 2)

        # Indirect
        val = mnemonics6510.get_instruction_length(10)
        self.assertEqual(val, 3)

        # Indexed Indirect X
        val = mnemonics6510.get_instruction_length(11)
        self.assertEqual(val, 2)

        # Relative
        val = mnemonics6510.get_instruction_length(12)
        self.assertEqual(val, 2)



if __name__ == '__main__':
    unittest.main()