# Minimal Example Testbench for safe testing framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu>
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.0
# Last Updated: 2025/06/09
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
STUDENT_FILE_PATH_PREFIX = "/home/"

DEBUG_OUTPUT = True
SHOW_ALL_PASSED_TESTS_FIRST = True

FILES_TO_HIDE = ["hidden.txt"] # eg ["abc.txt"]
HIDDEN_FILE_DICT = cache_hidden_test_files(FILES_TO_HIDE)

class SafeTesting():
    @setname() # Set the student visible testcase name as the function name excluding `test` or `test_` with spaces instead of '_'
    @score(0)
    def test_PEP8_Check(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name=STUDENT_FILE_NAME,                 # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,   # File path prefix, could change by Ed, but otherwise does not need to be touched
            ignored_tests=PEP8_IGNORED                           # Modify as desired, this is the default value set in the framework.
        )
    
    @setname()
    @score(0)
    def testAST_Check(self): 
        run_astcheck_test(
            student_file_name=STUDENT_FILE_NAME,               # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes=(),                              # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports=(),                            # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
        
    @setname("Override student visible name")
    @hidden(RELEASE_TEST_CASES) # Set the test case as hidden, override to become visible by setting RELEASE_TEST_CASES = True
    @score(2) # Set the score given for a testcase >>> ENSURE PERTESTCASE SCORING IS ENABLED!
    def testFunction(self):
        return run_function_test(
            student_file_name=STUDENT_FILE_NAME,                                      # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,                        # File path prefix
            function_name=None,                                                       # Function to test
            function_input=(),                                                        # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected=None,                                                   # Expected value for function
            function_timeout_seconds=1,                                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                                       # Check if the function input was mutated
            input="",                                                                 # Input that can be read by input() seperated by newlines
            input_echoing=True,                                                       # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                                       # Expected value in stdout
            expected_stderr="",                                                       # Expected value in stderr
            non_allowed_nodes=(),                                                     # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=("exec"),                                           # Function names of any specific functions to disallow
            non_allowed_imports=("sys", "os", "subprocess", "signal", "importlib"),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                                        # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal=[],                                                       # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict=HIDDEN_FILE_DICT,                                        # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @private(RELEASE_TEST_CASES) # Set the test case as private, override to become visible by setting RELEASE_TEST_CASES = True
    def testScript(self):
        return run_script_test(
            student_file_name=STUDENT_FILE_NAME,                                      # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,                        # File path prefix
            script_timeout_seconds=1,                                                 # Time in seconds until test fails due to timeout
            input="",                                                                 # Input that can be read by input() seperated by newlines
            input_echoing=True,                                                       # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                                       # Expected value in stdout
            expected_stderr="",                                                       # Expected value in stderr
            non_allowed_nodes=(),                                                     # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=("exec"),                                           # Function names of any specific functions to disallow
            non_allowed_imports=("sys", "os", "subprocess", "signal", "importlib"),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                                        # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal=[],                                                       # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict=HIDDEN_FILE_DICT,                                        # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
if __name__ == "__main__":
    run_tests(SafeTesting, debug_output=DEBUG_OUTPUT, show_all_passed_tests_first=SHOW_ALL_PASSED_TESTS_FIRST)
