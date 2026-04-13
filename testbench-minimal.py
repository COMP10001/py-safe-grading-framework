"""
Minimal Testbench Example

Depends on Python Safe Grading Framework for Edstem V0.5.0 pysafegradingfw.py
Updated: April 2026
Author: Kacie Beckett <kacie.beckett@unimelb.edu.au>
Faculty of Engineering and IT - The University of Melbourne
License: MIT
The latest version and documentation can be found at:
https://github.com/COMP10001/py-safe-grading-framework
"""
from pysafegradingfw import *

### ENSURE PER TESTCASE SCORING IS ENABLED!
### ENSURE TIMEOUT (s) IS SET HIGHER THAN THE SUM OF 'function_timeout_seconds' FOR EACH TEST!
### SEE TESTBENCH EXAMPLE FOR MORE EXPLANATION

# Remove the test file after loading by Ed, to prevent ability to print out contents
#os.remove(__file__)

# DANGER: Overrides Hidden and Private Tests so they become visible,
# Need to re-run test cases for all students for it to work
RELEASE_TEST_CASES = False

STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
FILES_TO_HIDE = [] # eg ["abc.txt"]
PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'

test_bench = SafeTesting(
    debug_mode=False,
    make_all_tests_visible=RELEASE_TEST_CASES,
    show_all_passed_tests_first=True,
    show_test_reports=True,
    file_path_prefix='/home/admin/git/safe-testing-framework/',
)

test_bench.cache_hidden_test_files(FILES_TO_HIDE)

test_bench.register_pep8_test(
    student_file_name=STUDENT_FILE_NAME,
    ignored_tests=PEP8_IGNORED,
)

test_bench.register_ast_test(
    student_file_name=STUDENT_FILE_NAME,
    non_allowed_functions=["print"]

)

test_bench.register_function_test(
    name = None,
    score = 0,
    hidden = False,
    private = False,
    student_file_name = STUDENT_FILE_NAME,
    function_name = STUDENT_FUNCTION,
    function_args = [],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args = False,
    function_expected_mutated_args = None,
    function_expected_recursive_calls=[],
    input_data = "",
    input_echoing = True,
    expected_stdout = "",
    expected_stderr = "",
    expected_files = [],
    files_to_reveal = [],
    # custom verification function/feedback injection available
    # ast check options available
)

test_bench.register_script_test(
    name = None,
    score = 0,
    hidden = False,
    private = False,
    student_file_name = STUDENT_FILE_NAME,
    script_timeout_seconds = 1,
    input_data = "",
    input_echoing = True,
    expected_stdout = "",
    expected_stderr = "",
    expected_files = [],
    files_to_reveal = [],
    # custom verification function/feedback injection available
    # ast check options available
)

if __name__ == "__main__":
    test_bench.run_tests()
