# Testbench Template Generator for V.0.4.0 Safe Testing Framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu.au>
# Choose from these options to generate a testbench file template
ASSIGNMENT_DESC = "Assignment 1 Testbench"
INCLUDE_PEP8_CHECK = False
INCLUDE_AST_CHECK = False
NUM_VISIBLE_FUNCTION_TESTS = 1
NUM_VISIBLE_SCRIPT_TESTS = 0
NUM_HIDDEN_FUNCTION_TESTS = 1
NUM_HIDDEN_SCRIPT_TESTS = 0
NUM_PRIVATE_FUNCTION_TESTS = 0
NUM_PRIVATE_SCRIPT_TESTS = 0
STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
STUDENT_FILE_PATH_PREFIX = "/home/" 


############################################################################################

PREAMBLE = \
r'''# {0}
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.4.0
# Last Updated: 2025/07/18
# Author: Kacie Beckett <kacie.beckett@unimelb.edu.au>
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

STUDENT_FUNCTION = "{1}"
STUDENT_FILE_NAME = "{2}"
STUDENT_FILE_PATH_PREFIX = "{3}"

# In setup mode all testcases will fail to ensure it is not left enabled
# Given input and output data will be formatted as a string with no line wrapping for easy copy pasting into testbench
SETUP_MODE = False

SHOW_ALL_PASSED_TESTS_FIRST = True

FILES_TO_HIDE = [] # eg ["abc.txt"]
HIDDEN_FILE_DICT = cache_hidden_test_files(FILES_TO_HIDE)

class SafeTesting():'''.format(ASSIGNMENT_DESC, STUDENT_FUNCTION, STUDENT_FILE_NAME, STUDENT_FILE_PATH_PREFIX)

SUFFIX = \
r'''
if __name__ == "__main__":
    run_tests(SafeTesting, setup_mode=SETUP_MODE, show_all_passed_tests_first=SHOW_ALL_PASSED_TESTS_FIRST)
'''

TEST_PEP8 = \
r'''
    @setname() # Set the student visible testcase name as the function name excluding `test` or `test_` with spaces instead of '_'
    @score(0)
    def test_PEP8_Check(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name=STUDENT_FILE_NAME,                 # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,   # File path prefix, could change by Ed, but otherwise does not need to be touched
            ignored_tests=PEP8_IGNORED                           # Modify as desired, this is the default value set in the framework.
        )
'''

TEST_ASTCHECK = \
r'''
    @setname()
    @score(0)
    def testAST_Check(self): 
        run_astcheck_test(
            student_file_name=STUDENT_FILE_NAME,               # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            required_nodes=[],                                 # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_nodes=[],                              # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_functions=[],                          # Function names of any specific functions to disallow
            non_allowed_imports=[],                            # Imports that are not allowed anywhere in student file or any local imports
        )
'''

RUN_FUNCTION_TEST = \
r'''
        return run_function_test(
            student_file_name=STUDENT_FILE_NAME,                                      # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,                        # File path prefix
            function_name=STUDENT_FUNCTION,                                           # Function to test
            function_args=[],                                                         # Must be wrapped in a tuple/list like test() -> [] or test(1) -> [1]
            function_expected=None,                                                   # Expected value for function
            function_timeout_seconds=1,                                               # Time in seconds until test fails due to timeout
            function_fail_on_mutated_args=False,                                      # Fail if function input was mutated
            function_expected_mutated_args=[],                                        # Required mutated_args
            function_check_expected_mutated_args=False,                               # Check if the function input was mutated to match function_expected_mutated_args, ignored if fail_on_mutated_args
            input_data="",                                                            # Input that can be read by input() seperated by newlines
            input_echoing=True,                                                       # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                                       # Expected value in stdout
            expected_stderr="",                                                       # Expected value in stderr
            required_nodes=[],                                                        # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_nodes=[],                                                     # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_functions=["exec"],                                           # Function names of any specific functions to disallow
            non_allowed_imports=["sys", "os", "subprocess", "signal", "importlib"],   # Imports that are not allowed anywhere in student file or any local imports
            files_to_reveal=[],                                                       # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict=HIDDEN_FILE_DICT,                                        # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )'''

RUN_SCRIPT_TEST = \
r'''
        return run_script_test(
            student_file_name=STUDENT_FILE_NAME,                                      # File to test function from
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,                        # File path prefix
            script_timeout_seconds=1,                                                 # Time in seconds until test fails due to timeout
            input_data="",                                                            # Input that can be read by input() seperated by newlines
            input_echoing=True,                                                       # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                                       # Expected value in stdout
            expected_stderr="",                                                       # Expected value in stderr
            required_nodes=[],                                                        # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_nodes=[],                                                     # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
            non_allowed_functions=["exec"],                                           # Function names of any specific functions to disallow
            non_allowed_imports=["sys", "os", "subprocess", "signal", "importlib"],   # Imports that are not allowed anywhere in student file or any local imports
            files_to_reveal=[],                                                       # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict=HIDDEN_FILE_DICT,                                        # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )'''


TEST_VISIBLE = \
r'''
    @setname()
    @score(0)
    def testVisible_{0}(self):'''

TEST_HIDDEN = \
r'''
    @setname()
    @hidden(RELEASE_TEST_CASES) # Set the test case as hidden, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testHidden_{0}(self):'''

TEST_PRIVATE = \
r'''
    @setname()
    @private(RELEASE_TEST_CASES) # Set the test case as private, override to become visible by setting RELEASE_TEST_CASES = True
    @score(0)
    def testPrivate_{0}(self):'''

# .txt because on ed it wont allow access to the file unless it ends in txt
with open("testbench.txt", "w") as fp:
    fp.write(PREAMBLE)
    if INCLUDE_PEP8_CHECK:
        fp.write(TEST_PEP8 + '\n')
    if INCLUDE_AST_CHECK:
        fp.write(TEST_ASTCHECK+ '\n')
    
    for i in range(NUM_VISIBLE_FUNCTION_TESTS):
        fp.write(TEST_VISIBLE.format(i+1))
        fp.write(RUN_FUNCTION_TEST + '\n')

    for i in range(NUM_VISIBLE_SCRIPT_TESTS):
        fp.write(TEST_VISIBLE.format(i+NUM_VISIBLE_FUNCTION_TESTS+1))
        fp.write(RUN_SCRIPT_TEST + '\n')

    for i in range(NUM_HIDDEN_FUNCTION_TESTS):
        fp.write(TEST_HIDDEN.format(i+1))
        fp.write(RUN_FUNCTION_TEST + '\n')

    for i in range(NUM_HIDDEN_SCRIPT_TESTS):
        fp.write(TEST_HIDDEN.format(i+NUM_HIDDEN_FUNCTION_TESTS+1))
        fp.write(RUN_SCRIPT_TEST + '\n')
        
    for i in range(NUM_PRIVATE_FUNCTION_TESTS):
        fp.write(TEST_PRIVATE.format(i+1))
        fp.write(RUN_FUNCTION_TEST + '\n')

    for i in range(NUM_PRIVATE_SCRIPT_TESTS):
        fp.write(TEST_PRIVATE.format(i+NUM_PRIVATE_FUNCTION_TESTS+1))
        fp.write(RUN_SCRIPT_TEST + '\n')
    
    fp.write(SUFFIX)