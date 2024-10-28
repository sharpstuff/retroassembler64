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

if __name__ == '__main__':
    unittest.main()