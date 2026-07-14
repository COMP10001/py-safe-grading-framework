"""
Testbench Template Generator for
Python Safe Grading Framework for Edstem V0.5.0 pysafegradingfw.py

Updated: April 2026
Author: Kacie Beckett <kacie.beckett@unimelb.edu.au>
Faculty of Engineering and IT - The University of Melbourne
License: MIT
The latest version and documentation can be found at:
https://github.com/COMP10001/py-safe-grading-framework
"""

# Choose from these options to generate a testbench file template
ASSIGNMENT_DESC = "Assignment 1 Testbench"
TESTCASE_AUTHOR = ""
INCLUDE_PEP8_CHECK = True
INCLUDE_AST_CHECK = True
NUM_FUNCTION_TESTS = 1
NUM_SCRIPT_TESTS = 1
STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
SHOW_TEST_REPORTS = False


############################################################################################

PREAMBLE = \
r'''"""
{0}
Testcase Author: {1}

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

# Remove the test file after loading by Ed, to prevent ability to print out content of testcases.
# In your local dev environment run with `python testbench.py --local-dev` to prevent deletion!
if not (len(sys.argv) >= 2 and sys.argv[1] == "--local-dev"):
    os.remove(__file__)

# DANGER: Overrides Hidden and Private Tests so they become visible,
# Need to re-run test cases for all students for it to work.
RELEASE_TEST_CASES = False

STUDENT_FUNCTION = "{2}"
STUDENT_FILE_NAME = "{3}"

test_bench = SafeGrading(
    debug_mode = False,
    format_test_in_out_data_as_str = False,
    make_all_tests_visible = False,
    show_all_passed_tests_first = True,
    show_test_reports = {4},
    # file_path_prefix
)

# Any files required for hidden tests should be removed
# from path except during that specific test
FILES_TO_HIDE = [] # eg ["abc.txt"]
test_bench.cache_hidden_test_files(FILES_TO_HIDE)
'''.format(ASSIGNMENT_DESC, TESTCASE_AUTHOR, STUDENT_FUNCTION, STUDENT_FILE_NAME, SHOW_TEST_REPORTS)


SUFFIX = \
r'''
if __name__ == "__main__":
    test_bench.run_tests()
'''

TEST_PEP8 = \
r'''
test_bench.register_pep8_test(
    name = "PEP8 Check",
    score = 0,
    hidden = False,
    private = False,
    student_file_name = STUDENT_FILE_NAME,
    # ignored_tests,
)'''

TEST_ASTCHECK = \
r'''
# Note function/script tests can also have ast checks
test_bench.register_ast_test(
    name = "AST Check",
    score = 0,
    hidden = False,
    private = False,
    student_file_name = STUDENT_FILE_NAME,
    non_allowed_nodes = [],
    non_allowed_functions = [],
    non_allowed_methods = [],
    non_allowed_imports = [],
    required_nodes = [],
    required_functions = [],
    required_methods = [],
    required_imports = [],
)'''

RUN_FUNCTION_TEST = \
r'''
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
    # see documentation on repo for all options
)'''

RUN_SCRIPT_TEST = \
r'''
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
    # see documentation on repo for all options
)'''

# .txt because on ed it wont allow access to the file unless it ends in txt
with open("testbench.txt", "w") as fp:
    fp.write(PREAMBLE)
    if INCLUDE_PEP8_CHECK:
        fp.write(TEST_PEP8 + '\n')
    if INCLUDE_AST_CHECK:
        fp.write(TEST_ASTCHECK+ '\n')

    for i in range(NUM_FUNCTION_TESTS):
        fp.write(RUN_FUNCTION_TEST + '\n')

    for i in range(NUM_SCRIPT_TESTS):
        fp.write(RUN_SCRIPT_TEST + '\n')


    fp.write(SUFFIX)