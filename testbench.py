
# Testbench for: 
#
# Safe Ed Assignment Unit Testing Framework V0.3.0 testbench.py
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

    @setname() # Set the student visible testcase name as the function name excluding `test` or `test_` with spaces instead of '_'
    @score(0)
    def test_PEP8_Check(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name=STUDENT_FILE_NAME, 
            student_file_path_prefix="/home/",   
            ignored_tests=PEP8_IGNORED          
        )


    @setname()
    @score(0)
    def testAST_Check(self): 
        run_astcheck_test(
            student_file_name=STUDENT_FILE_NAME,    # File to test function from
            student_file_path_prefix="/home/",      # File path prefix, could change by Ed
            non_allowed_nodes = (ast.And, ast.For), # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),               # Function names of any specific functions to disallow
            non_allowed_imports = (),               # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                      # Eg ast.Name, see ast library
        )


    @setname()
    @score(0)
    def testVisible_0(self):

        run_function_test(
                    student_file_name=STUDENT_FILE_NAME,                        
                    function_name=STUDENT_FUNCTION,                              
                    function_input=(),                                           
                    function_expected = None,                                   
                    function_timeout_seconds = 1,                                
                    check_mutate=False,                                          
                    expected_stdout="",                                          
                    expected_stderr="",                                          
                    non_allowed_nodes = (),                                      
                    non_allowed_functions=(),                                    
                    non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
                    required_nodes=(),                                           
                    files_to_reveal = [],                                        
                    hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


    @setname()
    @score(0)
    def testVisible_1(self):

        run_script_test(
            student_file_name=STUDENT_FILE_NAME,                        
            student_file_path_prefix="/home/",                          
            expected_stdout="",                                        
            expected_stderr="",                                          
            non_allowed_nodes = (),                                      
            non_allowed_functions=(),                                   
            non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
            required_nodes=(),                                          
            files_to_reveal = [],                               
            hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


    @setname()
    @hidden(RELEASE_TEST_CASES) # Set the test case as hidden, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testHidden_0(self):

        run_function_test(
                    student_file_name=STUDENT_FILE_NAME,                        
                    function_name=STUDENT_FUNCTION,                              
                    function_input=(),                                           
                    function_expected = None,                                   
                    function_timeout_seconds = 1,                                
                    check_mutate=False,                                          
                    expected_stdout="",                                          
                    expected_stderr="",                                          
                    non_allowed_nodes = (),                                      
                    non_allowed_functions=(),                                    
                    non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
                    required_nodes=(),                                           
                    files_to_reveal = [],                                        
                    hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


    @setname()
    @hidden(RELEASE_TEST_CASES) # Set the test case as hidden, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testHidden_1(self):

        run_script_test(
            student_file_name=STUDENT_FILE_NAME,                        
            student_file_path_prefix="/home/",                          
            expected_stdout="",                                        
            expected_stderr="",                                          
            non_allowed_nodes = (),                                      
            non_allowed_functions=(),                                   
            non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
            required_nodes=(),                                          
            files_to_reveal = [],                               
            hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


    @setname()
    @private(RELEASE_TEST_CASES) # Set the test case as private, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testPrivate_0(self):

        run_function_test(
                    student_file_name=STUDENT_FILE_NAME,                        
                    function_name=STUDENT_FUNCTION,                              
                    function_input=(),                                           
                    function_expected = None,                                   
                    function_timeout_seconds = 1,                                
                    check_mutate=False,                                          
                    expected_stdout="",                                          
                    expected_stderr="",                                          
                    non_allowed_nodes = (),                                      
                    non_allowed_functions=(),                                    
                    non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
                    required_nodes=(),                                           
                    files_to_reveal = [],                                        
                    hidden_file_dict = HIDDEN_FILE_DICT,                         
        )


    @setname()
    @private(RELEASE_TEST_CASES) # Set the test case as private, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testPrivate_1(self):

        run_script_test(
            student_file_name=STUDENT_FILE_NAME,                        
            student_file_path_prefix="/home/",                          
            expected_stdout="",                                        
            expected_stderr="",                                          
            non_allowed_nodes = (),                                      
            non_allowed_functions=(),                                   
            non_allowed_imports = ("sys", "os", "subprocess", "signal"), 
            required_nodes=(),                                          
            files_to_reveal = [],                               
            hidden_file_dict = HIDDEN_FILE_DICT,                         
        )

