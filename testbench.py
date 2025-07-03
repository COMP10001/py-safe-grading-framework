# Safe Ed Assignment Unit Testing Framework Example V0.2.0 testbench.py
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from safetestingframework import *

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

RELEASE_TEST_CASES = False

TEST_FILE = "runtestsubprocess.py"
STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"

# IMPORTANT: Check Time limit (s) is higher than the sum of all testcase function timeouts
# AND that Per-testcase Scores is selected
class SafeTesting(unittest.TestCase):
    def testPEP8(self):
        run_pep8_test(STUDENT_FILE_NAME)
        
    def testVis1(self):
        ''' #name(Test 1) '''
        # Function Input must be wrapped in a tuple
        # Eg for testfunction(1), function_input = (1,)
        run_function_test(test_file=TEST_FILE, 
                student_file_name=STUDENT_FILE_NAME,
                function_name=STUDENT_FUNCTION, 
                function_input=([1,2,3],), 
                function_expected=2, 
                function_timeout_seconds=10,
                check_mutate=True,
        )
        
    @hidden(RELEASE_TEST_CASES)
    @score(2)
    def testHid1(self):
        ''' #name(Hidden 1) '''
        # Function Input must be wrapped in a tuple
        # Eg for testfunction(1), function_input = (1,)
        run_function_test(test_file=TEST_FILE, 
                student_file_name=STUDENT_FILE_NAME,
                function_name=STUDENT_FUNCTION, 
                function_input=([1,2,3],), 
                function_expected=2, 
                function_timeout_seconds=10,
                check_mutate=True,
        )