# Safe Ed Assignment Unit Testing Framework Example V0.2.0 testbench.py
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from safetestingframework import *

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)
    
STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"

class SimpleTestCase(unittest.TestCase):
    def testVis1(self):
        ''' #name(Test 1)'''
        # Function Input must be wrapped in a tuple
        # Eg for testfunction(1), function_input = (1,)
        run_test(test_file="runtestsubprocess.py", 
                student_file_name=STUDENT_FILE_NAME,
                function_name=STUDENT_FUNCTION, 
                function_input=(1,), 
                function_expected=2, 
                function_timeout_seconds=10
        )
        
    def testHidd1(self):
        ''' #name(Hidden 1) #hidden ''' 
        run_test(test_file="runtestsubprocess.py", 
                student_file_name=STUDENT_FILE_NAME,
                function_name=STUDENT_FUNCTION, 
                function_input=(1,), 
                function_expected=2, 
                function_timeout_seconds=10,
        )

    def testPriv1(self):
        ''' #name(Private 1) #private #score(2)''' 
        run_test_as_script(test_file="program.py", 
                expected_stdout="Hello World\n",
                timeout_seconds=1
        )
        
