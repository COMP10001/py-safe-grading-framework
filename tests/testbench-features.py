# Feature Testing Testbench for safe testing framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu>
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.1
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from pysafegradingfw import *

STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
FILES_TO_HIDE = ["hidden.txt"] # eg ["abc.txt"]

test_bench = SafeGrading(
    debug_mode=True,
    make_all_tests_visible=False,
    show_all_passed_tests_first=True,
    show_test_reports=False,
)

test_bench.cache_hidden_test_files(FILES_TO_HIDE)

test_bench.register_style_test(
   name = "Style Pass",
    student_file_name="style_pass.py",
)

test_bench.register_style_test(
   name = "Style Fail",
    student_file_name="style_fail.py",
)

test_bench.register_style_test(
   name = "Style Recursive File Check Fail",
    student_file_name="style_recursive_import_test.py",
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Functions Pass",
    student_file_name="astcheck_non_allowed_functions.py",
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Functions Fail",
    student_file_name="astcheck_non_allowed_functions.py",
    non_allowed_functions=["print"],
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Pass",
    student_file_name="astcheck_non_allowed_imports.py",
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Fail",
    student_file_name="astcheck_non_allowed_imports.py",
    non_allowed_imports = ["sys"],
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Recursive Check Pass",
    student_file_name="astcheck_recursive_import_test.py",
    non_allowed_imports = ["signal", "subprocess"],

)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Recursive Check Fail",
    student_file_name="astcheck_recursive_import_test.py",
    non_allowed_imports = ["sys","subprocess"],

)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Pass",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = [ast.While],
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Fail",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = [ast.For],
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Pass",
    student_file_name="astcheck_required_nodes.py",
    required_nodes=[ast.For],
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Fail",
    student_file_name="astcheck_required_nodes.py",
    required_nodes=[ast.For, ast.While],
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Custom Name Pass",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = {ast.While: "while loop"},
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Custom Name Fail",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = {ast.For: "for loop"},
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Custom Name Pass",
    student_file_name="astcheck_required_nodes.py",
    required_nodes={ast.For: "for loop"},
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Custom Name Fail",
    student_file_name="astcheck_required_nodes.py",
    required_nodes={ast.For: "for loop", ast.While: "while loop"},
)


test_bench.register_function_test(
   name = "Function Not Defined Fail",
    student_file_name="function_tests.py",
    function_name="missing_function",
    function_args=["hello"],
    function_expected = "Showing the fail formatting",
    function_timeout_seconds = 1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Missing Body Fail",
    student_file_name="missing_function_body.py",
    function_name="missing_body",
    function_args=[],
    function_expected = "",
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Check 1 Input Arg Fail",
    student_file_name="function_tests.py",
    function_name="check_1_input_arg",
    function_args=("hello",),
    function_expected = "Showing the fail formatting",
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=True,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Check 2 Input Arg Fail",
    student_file_name="function_tests.py",

    function_name="check_2_input_arg",
    function_args=["hello",12345],
    function_expected = "Showing the fail formatting",
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=True,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",

)


test_bench.register_function_test(
   name = "function fail on mutated args Input Fail",
    student_file_name="function_tests.py",
    function_name="check_mutate_fail",
    function_args=([1,2,3],),
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=True,
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


test_bench.register_function_test(
   name = "Function Return Int Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_int",
    function_args=[],
    function_expected = 1,
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


test_bench.register_function_test(
   name = "Function Return Int Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_int",
    function_args=[],
    function_expected = 4,
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


test_bench.register_function_test(
   name = "Function Str Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_str",
    function_args=[],
    function_expected = "abc\ndefgh\t\r\nhello",
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


test_bench.register_function_test(
   name = "Function Return Str Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_str",
    function_args=[],
    function_expected = "1234\n1234\n1234",
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


test_bench.register_function_test(
   name = "Function Return Float Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_float",
    function_args=[],
    function_expected = 1.0,
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


test_bench.register_function_test(
   name = "Function Return Float Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_float",
    function_args=[],
    function_expected = 1.5,
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


test_bench.register_function_test(
   name = "Function Return List Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_list",
    function_args=[],
    function_expected = [1, 1.0, "abc", ("hi", 123)],
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


test_bench.register_function_test(
   name = "Function Return List Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_list",
    function_args=[],
    function_expected = [1,2,3,"abc"],
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


test_bench.register_function_test(
   name = "Function Return Tuple Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_tuple",
    function_args=[],
    function_expected = (123, "abc", [1,2,3]),
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


test_bench.register_function_test(
   name = "Function Return Tuple Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_tuple",
    function_args=[],
    function_expected = (1,2,3,"abc"),
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


test_bench.register_function_test(
   name = "Function Expected Stdout Pass",
    student_file_name="function_tests.py",
    function_name="expected_stdout",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="Abc\nabc\t\r\nabc\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Stdout Fail",
    student_file_name="function_tests.py",
    function_name="expected_stdout",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="1234\n1234\n\t\r\nasdfsdf",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Stderr Pass",
    student_file_name="function_tests.py",
    function_name="expected_stderr",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="Fake Error has occurred.\n",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Stderr Fail",
    student_file_name="function_tests.py",
    function_name="expected_stderr",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="Error",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Exception Pass",
    student_file_name="function_tests.py",
    function_name="expected_stderr_exception",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_exception=Exception("An error occured"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Exception Type Fail",
    student_file_name="function_tests.py",
    function_name="expected_stderr_exception",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="Error",
    expected_exception=ValueError("An error occured"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)

test_bench.register_function_test(
   name = "Function Expected Exception Message Fail",
    student_file_name="function_tests.py",
    function_name="expected_stderr_exception",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="Error",
    expected_exception=Exception("Wrong Message"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)

test_bench.register_function_test(
   name = "Function Expected Return and Stdout Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_and_stdout",
    function_args=[],
    function_expected = "abc",
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="abc\ndef\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected Return and Stdout Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_and_stdout",
    function_args=[],
    function_expected = "abc1234",
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="abc\ndef\nefgh\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Timeout 1 second Fail",
    student_file_name="function_tests.py",
    function_name="timeout_fail",
    function_args=[],
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


test_bench.register_function_test(
   name = "Function Timeout 2 second Fail",
    student_file_name="function_tests.py",
    function_name="timeout_fail",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 2,
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

test_bench.register_function_test(
   name = "Function Expected Mutated Args Pass",
    student_file_name="expected_mutated_args.py",
    function_name="mutated_args_pass",
    function_args=[[1,2,3]],
    function_expected = [1,2,3,5],
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    function_expected_mutated_args=[[1,2,3,5]],
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

test_bench.register_function_test(
   name = "Function Expected Mutated Args Fail",
    student_file_name="expected_mutated_args.py",
    function_name="mutated_args_fail",
    function_args=[[1,2,3]],
    function_expected = [1,2,3,5],
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    function_expected_mutated_args=[[1,2,3,5]],
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


test_bench.register_function_test(
   name = "Function Hidden File Valid Access Pass",
    student_file_name="function_tests.py",
    function_name="hidden_files_access",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="verysecretfilecontents\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = ["hidden.txt"],
)


test_bench.register_function_test(
   name = "Function Hidden File Invalid Access Fail",
    student_file_name="function_tests.py",
    function_name="hidden_files_access",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="verysecretfilecontents\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Input Pass",
    student_file_name="function_tests.py",
    function_name="input_echoing",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="1\n2\n",
    input_echoing = False,
    expected_stdout="Type in 1:Type in 2:True\nTrue\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = ["hidden.txt"],
)


test_bench.register_function_test(
   name = "Function Input Fail",
    student_file_name="function_tests.py",
    function_name="input_echoing",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="1\n",
    input_echoing = False,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = ["hidden.txt"],
)


test_bench.register_function_test(
   name = "Function Input Echoing Pass",
    student_file_name="function_tests.py",
    function_name="input_echoing",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="1\n2\n",
    input_echoing = True,
    expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Input Echoing Fail",
    student_file_name="function_tests.py",
    function_name="input_echoing",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="1\n",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Spam Print Fail",
    student_file_name="function_tests.py",
    function_name="spam_print",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 10,
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


test_bench.register_function_test(
   name = "Function Spam Print Stdout and Stderr Fail",
    student_file_name="function_tests.py",
    function_name="spam_print_stdout_stderr",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 10,
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


test_bench.register_function_test(
   name = "Function Import With Dashes Pass",
    student_file_name="import-with-dashes.py",
    function_name="func",
    function_args=[],
    function_expected = 123,
    function_timeout_seconds = 10,
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


test_bench.register_function_test(
   name = "Function Expected File Pass",
    student_file_name="function_tests.py",
    function_name="expected_file",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file1.txt")],
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_function_test(
   name = "Function Expected File Fail",
    student_file_name="function_tests.py",
    function_name="expected_file",
    function_args=[],
    function_expected = None,
    function_timeout_seconds = 1,
    function_fail_on_mutated_args=False,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file2.txt")],
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports = [],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Input Pass",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,
    input_data="1\n2\n",
    input_echoing = False,
    expected_stdout="Type in 1:Type in 2:True\nTrue\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Input Fail",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,
    input_data="1\n",
    input_echoing = False,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Input Echoing Pass",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,
    input_data="1\n2\n",
    input_echoing = True,
    expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Input Echoing Fail",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,
    input_data="1\n",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Timeout 1 Second Fail",
    student_file_name="script_timeout_fail.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Timeout 2 Second Fail",
    student_file_name="script_timeout_fail.py",
    script_timeout_seconds=2,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Stdout Pass",
    student_file_name="script_expected_stdout.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="hello\n1234\t\r\nsdfsfds\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Stdout Fail",
    student_file_name="script_expected_stdout.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="1234",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Stderr Pass",
    student_file_name="script_expected_stderr.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="hello\n1234\t\r\nsdfsfds\n",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Stderr Fail",
    student_file_name="script_expected_stderr.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="1234",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Stderr Exception Pass",
    student_file_name="script_expected_stderr_exception.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_exception=Exception("Test exception"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected Exception Type Fail",
    student_file_name="script_expected_stderr_exception.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_exception=ValueError("Test exception"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
    )

test_bench.register_script_test(
   name = "Script Expected Exception Message Fail",
    student_file_name="script_expected_stderr_exception.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_exception=Exception("wrong message"),
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
    )

test_bench.register_script_test(
   name = "Script Hidden File Valid Access Pass",
    student_file_name="script_hidden_files.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="verysecretfilecontents\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = ["hidden.txt"],
)


test_bench.register_script_test(
   name = "Script Hidden File Invalid Access Fail",
    student_file_name="script_hidden_files.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="verysecretfilecontents\n",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Import With Dashes Pass",
    student_file_name="import-with-dashes.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected File Pass",
    student_file_name="script_expected_file.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file1.txt")],
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)


test_bench.register_script_test(
   name = "Script Expected File Fail",
    student_file_name="script_expected_file.py",
    script_timeout_seconds=1,
    input_data="",
    input_echoing = True,
    expected_stdout="",
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file2.txt")],
    non_allowed_nodes = [],
    non_allowed_functions=[],
    non_allowed_imports=[],
    required_nodes=[],
    files_to_reveal = [],
)

if __name__ == "__main__":
    test_bench.run_tests()

