# Practical Python Basics Generate First Row
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.0
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from safetestingframework import *

### ENSURE PER TESTCASE SCORING IS ENABLED!
### ENSURE TIMEOUT (s) IS SET HIGHER THAN THE SUM OF 'function_timeout_seconds' FOR EACH TEST!
### SEE TESTBENCH EXAMPLE FOR MORE EXPLANATION

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

# DANGER: Overrides Hidden and Private Tests so they become visible,
# Need to re-run test cases for all students for it to work
RELEASE_TEST_CASES = False 

STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"

FILES_TO_HIDE = [] # eg ["abc.txt"]
HIDDEN_FILE_DICT = cache_hidden_test_files(FILES_TO_HIDE)

class SafeTesting(unittest.TestCase):

    @setname()
    @score(0)
    def testVisible_1(self):
        run_script_test(
            student_file_name=STUDENT_FILE_NAME,                        
            student_file_path_prefix="/home/",                          
            expected_stdout="|x| | | | \n",                                        
            expected_stderr="",                                          
            non_allowed_nodes = (),                                      
            non_allowed_functions=(),                                   
            non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
            required_nodes=(),                                          
            files_to_reveal = [],                               
            hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


