# Feature Testing Testbench for safe testing framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu>
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.1
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from pysafegradingfw import *

import random

STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
FILES_TO_HIDE = [] # eg ["abc.txt"]

test_bench = SafeGrading(
    debug_mode=False,
    make_all_tests_visible=False,
    show_all_passed_tests_first=True,
    show_test_reports=False,
)

test_bench.cache_hidden_test_files(FILES_TO_HIDE)

# Verify that inbuilt random module is not shadowed
print("TESTBENCH", random.randint(1,1), file=ORIGINAL_STDOUT)

# Verify that the testbench *is* shadowing on the subprocess, to ensure
# consistent behaviour when running code directly with python.
test_bench.register_function_test(
   name = "Builtin Library Shadowing Pass",
    student_file_name="libshadowing.py",
    function_name="shadowing_test",
    function_args=[15],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)



if __name__ == "__main__":
    test_bench.run_tests()

