"""
Python Safe Grading Framework for Edstem V0.5.0 pysafegradingfw.py
Updated: April 2026
Author: Kacie Beckett <kacie.beckett@unimelb.edu.au>
Faculty of Engineering and IT - The University of Melbourne
License: MIT
The latest version and documentation can be found at:
https://github.com/COMP10001/py-safe-grading-framework
"""

import os
import subprocess
import ast
import traceback
import json
import filecmp
import sys
import dill
import signal
import resource
import gc

from pydantic import validate_call, PlainValidator
from collections.abc import Callable
from typing import Any, Annotated
from types import TracebackType
if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer

# Disable Printing to STDOUT as this breaks the Ed integration if done accidentally
ORIGINAL_STDOUT = sys.stdout
sys.stdout = open(os.devnull, 'w')

#######################################################################################

OUTPUT_TRUNCATION_MSG = "\n[...] Too much output was produced.\n"
OUTPUT_TRUNCATION_FROM_START_MSG = "Too much output was produced. [...]\n"
FUNCTION_CALLED_MSG = "► Called: {0}\n"
INPUT_FEEDBACK_MSG = "► Input:\n{0}\n"

EXPECTED_RETURN_MSG = "► Expected Return <{0}>:\n{1}\n"
STUDENT_RETURN_MSG = "► Returned <{0}>:\n{1}\n"

UNEXPECTED_EXCEPTION_MSG = "► Your program produced the following Exception when no exception was expected:\n{}({})\n"
STUDENT_EXCEPTION_MSG = "► Your program produced the following Exception:\n{}({})\n"
MISSING_EXCEPTION_MSG = "► Your program produced no exception when one was required.\n"
EXPECTED_EXCEPTION_MSG = "► The expected exception is:\n{}({})\n"

ERROR_RETURN_MSG = "► No value was returned due to errors\n"
WRONG_STDERR_MSG = "► Your program produced the following stderr output:\n{0}\n"
EXPECTED_STDERR_MSG = "► The expected stderr output is:\n{0}\n"

STUDENT_RECURSION_COUNT_MSG = "► Your program produced the following recursive call counts:\n"
EXPECTED_RECURSION_COUNT_MSG = "► The expected number of recursive calls in a called function is {}.\n"

UNEXPECTED_STDOUT_MSG = (
    "► Your program printed the following output when no printing was expected:\n{0}\n"
)
WRONG_STDOUT_MSG = "► Your program printed the following output:\n{0}\n"
EXPECTED_STDOUT_MSG = "► The expected printed output is:\n{0}\n"

PEP8_ERROR_MSG = "► The following style errors were found:\n"
AST_VIOLATION_MSG = "► The following AST violations were found:\n"
FILE_CHECK_ERROR_MSG = "► The following expected file errors were found:\n"

NON_ALLOWED_NODE_MSG = (
    "Your program is not allowed to use a {0}. This occurred on line {1} of {2}.\n"
)
REQUIRED_NODE_MSG = "Your program must use a {0}.\n"

NON_ALLOWED_FUNCTION_MSG = (
    "Your program is not allowed to use the {0} function. "
    "This occurred on line {1} of {2}.\n"
)
REQUIRED_FUNCTION_MSG = "Your program must use the {0} function.\n"
MISSING_FUNC_DEF_MSG = "Your program should define a function named '{0}'\n"

NON_ALLOWED_METHOD_MSG = (
    "Your program is not allowed to use the {0} method. "
    "This occurred on line {1} of {2}.\n"
)
REQUIRED_METHOD_MSG = "Your program must use the {0} method.\n"

NON_ALLOWED_IMPORT_MSG = (
    "Your program is not allowed to import {0}. Occured in file {1}.\n"
)
REQUIRED_IMPORT_MSG = "Your program must use import {0}.\n"

FAIL_ON_MUTATION_MSG = "► Your code should not mutate the function input!\n"
RECIEVED_ARGS_MSG = "► Input Arguments after mutation:\n{0}\n"
EXPECTED_MUTATED_ARGS_MSG = "► Expected Mutated Input Arguments:\n{0}\n"

EXPECTED_FILES_MSG = "► The following file issues were found:\n"

TIMEOUT_ERROR_MSG = (
    "► Your program took too long to run and was terminated after {0} second{1}. "
    "Do you have an infinite loop?\n"
)

MEMORY_ERROR_MSG = (
    "► Your program used too much memory. "
    "Do you have an infinite loop?\n"
)

MAX_FEEDBACK_LEN_EXCEEDED_MSG = (
    "Setup Issue: {0} Reduce the number of test cases or amount of "
    "data in the test input/output.\n"
)

STUDENT_FILE_NOT_FOUND_MSG = (
    "► Program file {0} could not be found. "
    "Did you delete the file, or put it into a folder?\n"
)

#######################################################################################

DEFAULT_STUDENT_FILE_PATH_PREFIX = "/home/"

SUBPROC_FUNC_INPUT_FILENAME = "subproc-func-input"
SUBPROC_FUNC_RETURN_FILENAME = "subproc-func-return"
SUBPROC_FUNC_ARGS_FILENAME = "subproc-func-args"
SUBPROC_EXC_FILENAME = "subproc-exception"
SUBPROC_RECURSION_COUNT_FILENAME = "subproc-recursion-count"
SUBPROC_PICKLE_FAILED_FILENAME = 'pickle-failed'


SUBPROC_STDOUT_FILENAME = "stdout.txt"
SUBPROC_STDERR_FILENAME = "stderr.txt"

VISIBLE_TEST_REPORT_FILENAME = "visible_test_report.txt"
PRIVATE_TEST_REPORT_FILENAME = "private_test_report.txt"
VISIBLE_TEST_EXECUTION_TRANSCRIPT_FILENAME = "visible_test_execution_transcript.txt"
PRIVATE_TEST_EXECUTION_TRANSCRIPT_FILENAME = "private_test_execution_transcript.txt"
RUN_TEST_SUBPROCESS_FILENAME = "runtestsubprocess.py"

#######################################################################################

MAX_SUBPROCESS_STDOUT_CHARS = 10000
DEFAULT_PEP8_TRUNCATION_LENGTH = 1000
DEFAULT_AST_TRUNCATION_LENGTH = 1000

# This is the maximum amount of output that can be printed by test code
# before Edstem crashes and dumps all of stdout to screen.
# Custom grader passes json object over stdout for Ed to parse.
# Note that this limit is imposed by Ed's json parser, and not imposed
# on subprocesses, which will crash  due to exceeding memory availability or disk space
EDSTEM_MAX_GRADER_OUTPUT_CHARS = 200000

# Not presently used for anything, but were found by testing
EDSTEM_TESTING_FILESYSTEM_MAX_SIZE_MB = 100
EDSTEM_STUDENT_DATA_MAX_SIZE_MB = 20

EDSTEM_MAX_MEMORY_FOOTPRINT_MB = 512
# Choose a value underneath the actual maximum.
EDSTEM_SOFTLIMIT_MEMORY_FOOTPRINT_MB = 480

MEGABYTE_TO_BYTES = 1024*1024

#######################################################################################

def validate_exception_instance(v):
    """ Custom validator to enforce exception instance type for pydantic """
    if isinstance(v, type) and issubclass(v, Exception):
        raise TypeError("Expected an exception instance, got an exception class.")
    if not isinstance(v, Exception):
        raise TypeError("Expected an exception instance.")
    return v

# Annotated type for Pydantic
ExceptionInstance = Annotated[Exception, PlainValidator(validate_exception_instance)]

#######################################################################################


class TestData:
    TEST_FUNCTION = "function-test"
    TEST_SCRIPT = "script-test"
    TEST_AST = "ast-test"
    TEST_PEP8 = "pep8-test"

    def __init__(self, name, score, hidden, private, student_file_name, test_type):

        self.test_type: str  = test_type
        self.name: str = name
        self.score: float | int = score
        self.max_score: float | int = score
        self.hidden: bool = hidden
        self.private: bool = private
        self.student_file_name: str = student_file_name
        self.success: bool = False
        self.give_half_marks: bool = False
        self.test_timeout: int = 1

        self.input_data: str
        self.input_echoing: bool
        self.files_to_reveal: list[str]
        self.hidden_file_dict: dict[str, str]

        self.function_name: str
        self.function_fail_on_mutated_args: bool

        self.custom_verification_function: Callable[[TestData], None] | None
        self.custom_verification_data: Any
        self.custom_verification_timeout: int
        self.custom_verification_timeout_msg: str

        self.non_allowed_nodes: list[type] | dict[type, str]
        self.non_allowed_functions: list[str]
        self.non_allowed_methods: list[str]
        self.non_allowed_imports: list[str]

        self.required_nodes: list[type] | dict[type, str]
        self.required_functions: list[str]
        self.required_methods: list[str]
        self.required_imports: list[str]

        self.pep8_ignored_tests: str
        self.pep8_max_line_len: int
        self.msg = self.Messages()
        self.expected = self.Expected()
        self.student = self.Student()

    def run_test(self, hidden_file_dict: dict[str, Buffer], format_test_in_out_data_as_str: bool):
        if not os.path.isfile(self.student_file_name):
            self.msg.student_file_not_found = STUDENT_FILE_NOT_FOUND_MSG.format(self.student_file_name)
            self.success = False
            return

        if self.test_type == self.TEST_FUNCTION:
            run_function_test(self, hidden_file_dict, format_test_in_out_data_as_str)
        elif self.test_type == self.TEST_SCRIPT:
            run_script_test(self, hidden_file_dict, format_test_in_out_data_as_str)
        elif self.test_type == self.TEST_AST:
            run_astcheck_test(self, format_test_in_out_data_as_str)
        elif self.test_type == self.TEST_PEP8:
            run_pep8_test(self)

    class Expected:
        def __init__(self):
            self.stdout: str
            self.stderr: str
            self.returned: Any
            self.exception: ExceptionInstance | None = None
            self.original_args: list[Any] | tuple[Any]
            self.mutated_args: list[Any] | tuple[Any] | None
            self.filenames: list[tuple[str, str]]
            self.recursive_call_counts: list[int]


    class Student:
        def __init__(self):
            self.stdout: str
            self.stderr: str
            # Note that because returned can be Any type, the absence of this
            # variable being assigned at confirms whether the student function
            # finished correctly.
            self.returned: Any
            self.failed_return: str
            self.exception: ExceptionInstance | None = None
            self.final_args: list[Any] | tuple[Any]
            self.recursive_call_count: dict[str, int]
            # self.testproc_ret: subprocess.CompletedProcess

    class Messages:
        def __init__(self):
            self.pep8: str = ""
            self.astcheck: str = ""
            self.function_call: str = ""
            self.input: str = ""
            self.timeout: str = ""
            self.memory_error: str = ""
            self.student_file_not_found: str = ""
            self.custom_verification_hook: str = ""
            self.student_recursion_count: str = ""
            self.expected_recursion_count: str = ""
            self.student_exception: str = ""
            self.expected_exception: str = ""
            self.student_stderr: str = ""
            self.expected_stderr: str = ""
            self.student_stdout: str = ""
            self.expected_stdout: str = ""
            self.student_return: str = ""
            self.expected_return: str = ""
            self.mutation_check: str = ""
            self.student_mutated: str = ""
            self.expected_mutated: str = ""
            self.expected_file: str = ""


class SafeTesting:
    DEFAULT_PEP8_IGNORED = (
    "E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225"
    "E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503"
    )
    DEFAULT_PEP8_MAX_LINE_LEN=79
    DEFAULT_NON_ALLOWED_NODES = []
    DEFAULT_NON_ALLOWED_FUNCTIONS = ["exec", "eval"]
    DEFAULT_NON_ALLOWED_METHODS = []
    DEFAULT_NON_ALLOWED_IMPORTS = ["sys", "os", "subprocess", "signal", "importlib", "builtins"]
    def __init__(
        self,
        debug_mode: bool = False,
        format_test_in_out_data_as_str: bool = False,
        make_all_tests_visible: bool = False,
        show_all_passed_tests_first: bool = True,
        show_test_reports: bool = True,
        file_path_prefix: str = os.getcwd()+'/',
        show_flag_manual_intervention_testcase: bool = False,
    ):
        """
        Testing infrastructure for safely testing student code, with easy access to testing specific functions,
        entire script files, performing AST checks, and style checks. Output feedback clearly specifies, what
        function return types should be, if they should or should not print output etc, with output and stderr formatting
        showing hidden chars such as newlines while also preserving line wrapping to make it easier for students to understand
        why their output differs.

        Usage Instructions:
            - create an instance of this class eg: test_bench = SafeTesting(...)
            - cache any test files used in hidden/private tests remembering to set files_to_reveal for
              the given test eg: test_bench.cache_hidden_test_files(["abc.txt"])
            - register any tests eg: test_bench.register_function_test(...)
            - run the tests eg: test_bench.run_tests()

        Parameters:
            debug_mode : Test running exceptions are reraised instead of showing test error and completing the remaining tests
            format_test_in_out_data_as_str : All input/stdout/stderr is printed as string repr() for easy setup copy pasting
            make_all_tests_visible : Override, hidden and private testcases to become visible
            show_all_passed_tests_first : Sort passed tests first, preserving relative order
            show_test_reports : Create the visible/private test report and execution transcript output files
            file_path_prefix : Where files are created and looked for by default.
        """
        self.test_cases: list[TestData] = []
        self.make_all_tests_visible: bool = make_all_tests_visible
        self.debug_mode: bool = debug_mode
        self.show_all_passed_tests_first: bool = show_all_passed_tests_first
        self.show_test_reports = show_test_reports
        self.student_file_path_prefix: str = file_path_prefix
        self.hidden_file_dict = {}
        self.format_test_in_out_data_as_str = format_test_in_out_data_as_str
        self.show_flag_manual_intervention_testcase = show_flag_manual_intervention_testcase

        self.visible_test_count = 0
        self.hidden_test_count = 0
        self.private_test_count = 0

        global STUDENT_FILE_PATH_PREFIX
        STUDENT_FILE_PATH_PREFIX = self.student_file_path_prefix

    def run_tests(self):
        """
        Run all the registered test cases, and produce the execution transcripts,
        test case reports and output the required json test object for Edstem
        """

        memory_limit_bytes = EDSTEM_SOFTLIMIT_MEMORY_FOOTPRINT_MB  * MEGABYTE_TO_BYTES
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

        ed_test_grader_output = EdCustomGraderJson()
        if self.show_test_reports:
            create_test_report_testcases(ed_test_grader_output)

        for test in self.test_cases:
            ok, feedback  = True, ""
            try:
                test.run_test(self.hidden_file_dict, self.format_test_in_out_data_as_str)
            except Exception as e:
                if self.debug_mode:
                    # Allow exceptions to crash testbench, under normal
                    # circumstances there should be no exceptions raised.
                    raise Exception from e
                test.name = "ERROR CONTACT COURSE COORDINATOR " + test.name
                test.success = False
                ok = False  # Test Bench Error.

            if self.debug_mode:
                test.name = "Disable DEBUG_MODE " + test.name

            if self.make_all_tests_visible:
                test.hidden = False
                test.private = False


            if test.success == False:
                if test.give_half_marks:
                    test.score /= 2
                else:
                    test.score = 0

            ed_test_obj = ed_test_grader_output.add_test_case(
                test.name, test.score, test.hidden, test.private, test.success, ok, feedback, test.max_score
            )
            ed_test_obj.test_data = test

        if self.show_all_passed_tests_first:
            ed_test_grader_output.test_cases.sort(key=lambda x: not x.passed)

        if self.show_flag_manual_intervention_testcase:
            flag_manual_intervention_testcase(ed_test_grader_output, self.test_cases)

        set_test_output_files(ed_test_grader_output)

        if self.show_test_reports:
            write_test_report_files(ed_test_grader_output.test_cases)

        for filename, filedata in self.hidden_file_dict.items():
            with open(filename, "wb") as fp:
                fp.write(filedata)

        ed_test_case_json = set_test_feedback_level(ed_test_grader_output)

        # Re-Enable printing to STDOUT
        sys.stdout = ORIGINAL_STDOUT
        # Ed reads the test json from stdout
        print(ed_test_case_json)

    @validate_call
    def cache_hidden_test_files(self, files: list[str]) -> None:
        """
        Create a dictionary of Key, Value = Filename, File Content String
        for each file and remove it from path. The files can then be revealed
        only when running a given test, with HiddenFileManager, or its integration
        into run_function_test or run_script_test, to avoid data leakage.
        """
        for file in files:
            with open(self.student_file_path_prefix + file, "rb") as fp:
                self.hidden_file_dict[file] = fp.read()
            if not self.debug_mode:
                os.remove(file)

    def _set_default_test_name(self, name: str | None, hidden: bool, private: bool):
        self._increment_test_counts(hidden, private)
        if name is None:
            return self._get_default_test_name(hidden, private)
        return name

    def _increment_test_counts(self, hidden: bool, private: bool):
        if private:
            self.private_test_count += 1
        elif hidden:
            self.hidden_test_count += 1
        else:
            self.visible_test_count += 1

    def _get_default_test_name(self, hidden: bool, private: bool):
        if private:
            return f"Private {self.private_test_count}"
        elif hidden:
            return f"Hidden {self.hidden_test_count}"
        else:
            return f"Visible {self.visible_test_count}"

    @validate_call
    def register_function_test(
        self,
        name: str | None = None,
        score: float | int  = 0,
        hidden: bool = False,
        private: bool = False,
        student_file_name: str = "",
        function_name: str = "",
        function_args: list[Any] | tuple[Any] = [],
        function_expected: Any = None,
        function_timeout_seconds: int = 1,
        function_fail_on_mutated_args: bool = False,
        function_expected_mutated_args: list[Any] | tuple[Any] | None = None,
        function_expected_recursive_calls: list[int] = [],
        input_data: str = "",
        input_echoing: bool = True,
        expected_stdout: str = "",
        expected_stderr: str = "",
        expected_exception: ExceptionInstance | None = None,
        expected_files: list[tuple[str, str]] = [],
        files_to_reveal: list[str] = [],
        custom_verification_function: Callable[[TestData],None] | None = None,
        custom_verification_data: Any = None,
        custom_verification_timeout: int = 1,
        custom_verification_timeout_msg: str = "",
        non_allowed_nodes: list[type] | dict[type, str] = DEFAULT_NON_ALLOWED_NODES,
        non_allowed_functions: list[str] = DEFAULT_NON_ALLOWED_FUNCTIONS,
        non_allowed_methods: list[str] = DEFAULT_NON_ALLOWED_METHODS,
        non_allowed_imports: list[str] = DEFAULT_NON_ALLOWED_IMPORTS,
        required_nodes: list[type] | dict[type, str] = [],
        required_functions: list[str] = [],
        required_methods: list[str] = [],
        required_imports: list[str] = [],
    ) -> None:
        """
        Description:
            Test the return value, stdout, stderr etc of a student defined function.
            Includes the ability to check for mutated input. By default OS and other
            imports are blocked to mitigate attempts to bypass testing. Other nodes to
            check for via the abstract syntax tree can be specified to check that students
            use or do not use certain python features.

        Parameters:
            name                           : Test visible name. Default to "Visible/Hidden/Private {n_tests}" if None
            score                          : Points to give testcase pass if Ed's Per-Testcase scoring is enabled
            hidden                         : Hidden tests have pass/fail visible; students cannot see the input/output
            Private                        : Private tests are completely invisible to students
            student_file_name              : Name of the file containing the function to test.
            student_file_path_prefix       : Prefix path to the student file.
            function_name                  : Name of the function to test.
            function_args                  : Args passed to the function eg test()-> [], test(1)->[1].
            function_expected              : Expected return value of the function.
            function_timeout_seconds       : Timeout in seconds for function execution.
            function_fail_on_mutated_args  : Fail if input args are mutated unexpectedly.
            function_expected_mutated_args : Expected post-call state of args. None if not checked.
            function_expected_recursive_calls : A list of acceptable recursive call counts, ignored if empty.
            custom_verification_function   : Function object to run during verify_program_output, that can modify the
                state of the testcase messages etc, and whether the test fails, to patch in extra checks. Takes in TestData instance.
            custom_verification_data       : Arbitrary data to use inside the custom_verification_function as attribute of TestData
            custom_verification_timeout    : Safety Timeout for the custom_verification_function, to prevent testbench crashing.
            custom_verification_timeout_msg: What to assign to test_data.msg.custom_verification_hook on fail
            input_data                     : Input fed into input(); mmultiple lines separated by newline characters
            input_echoing                  : If True, echoes input to stdout like an interactive shell.
            expected_stdout                : Expected string output to stdout.
            expected_stderr                : Expected string output to stderr.
            expected_exception             : Instance of exception class eg ValueError("yourerrormessage")
            expected_files                 : List of (student_file, test_file) tuples for file comp.
            files_to_reveal                : Files hidden with self.cache_hidden_test_files() to add back to path

            For ommited ast related parameters see register_ast_test() docstring.
        """
        if function_fail_on_mutated_args and function_expected_mutated_args is not None:
            assert (
                False
            ), "Setup Issue: can't fail on mutated args, and have expected mutated args."

        name = self._set_default_test_name(name, hidden, private)

        test_data = TestData(name, score, hidden, private, student_file_name, TestData.TEST_FUNCTION)
        test_data.function_name = function_name
        test_data.expected.original_args = function_args
        test_data.expected.returned = function_expected
        test_data.test_timeout = function_timeout_seconds
        test_data.expected.mutated_args = function_expected_mutated_args
        test_data.function_fail_on_mutated_args = function_fail_on_mutated_args
        test_data.input_data = input_data
        test_data.input_echoing = input_echoing
        test_data.expected.stdout = expected_stdout
        test_data.expected.stderr = expected_stderr
        test_data.expected.exception = expected_exception
        test_data.expected.filenames = expected_files
        test_data.files_to_reveal = files_to_reveal
        test_data.expected.recursive_call_counts = function_expected_recursive_calls
        test_data.custom_verification_function = custom_verification_function
        test_data.custom_verification_data = custom_verification_data
        test_data.custom_verification_timeout = custom_verification_timeout
        test_data.custom_verification_timeout_msg = custom_verification_timeout_msg
        test_data.non_allowed_nodes = non_allowed_nodes
        test_data.non_allowed_functions = non_allowed_functions
        test_data.non_allowed_methods = non_allowed_methods
        test_data.non_allowed_imports = non_allowed_imports
        test_data.required_nodes = required_nodes
        test_data.required_functions = required_functions
        test_data.required_methods = required_methods
        test_data.required_imports = required_imports

        # Verify the return object type can be tested, as not all objects can be
        # pickled, but this is a requirement for how the testing occurs.
        try:
            encode_obj_data(function_expected, "validate-pickleable")
            os.remove("validate-pickleable")
        except:
            raise Exception(
                f"Setup Issue: Unsupported Function Expected Object Type, cannot be pickled."
            )

        self.test_cases.append(test_data)

    @validate_call
    def register_script_test(
        self,
        name: str | None = None,
        score: float | int  = 0,
        hidden: bool = False,
        private: bool = False,
        student_file_name: str = "",
        script_timeout_seconds: int = 1,
        input_data: str = "",
        input_echoing: bool = True,
        expected_stdout: str = "",
        expected_stderr: str = "",
        expected_exception: ExceptionInstance | None = None,
        expected_files: list[tuple[str, str]] = [],
        files_to_reveal: list[str] = [],
        custom_verification_function: Callable[[TestData], None] | None = None,
        custom_verification_data: Any = None,
        custom_verification_timeout: int = 1,
        custom_verification_timeout_msg: str = "",
        non_allowed_nodes: list[type] | dict[type, str] = DEFAULT_NON_ALLOWED_NODES,
        non_allowed_functions: list[str] = DEFAULT_NON_ALLOWED_FUNCTIONS,
        non_allowed_methods: list[str] = DEFAULT_NON_ALLOWED_METHODS,
        non_allowed_imports: list[str] = DEFAULT_NON_ALLOWED_IMPORTS,
        required_nodes: list[type] | dict[type, str] = [],
        required_functions: list[str] = [],
        required_methods: list[str] = [],
        required_imports: list[str] = [],
    ) -> None:
        """
        Description:
            Test the stdout, stderr of a student defined python script.
            By default OS and other imports are blocked to mitigate attempts to bypass testing.
            Other nodes to check for via the abstract syntax tree can be specified to check that
            students use or do not use certain python features.

        Parameters:
            name                   : Test visible name. Default to "Visible/Hidden/Private {n_tests}" if None
            score                  : Points to give testcase pass if Ed's Per-Testcase scoring is enabled
            hidden                 : Hidden tests have pass/fail visible; students cannot see the input/output
            Private                : Private tests are completely invisible to students
            student_file_name      : Name of the file containing the script to test.
            script_timeout_seconds : Timeout in seconds for script execution.
            input_data             : Input fed into input(); multiple lines separated by newline characters
            input_echoing          : If True, echoes input to stdout like an interactive shell.
            expected_stdout        : Expected string output to stdout.
            expected_stderr        : Expected string output to stderr.
            expected_exception     : Instance of exception class eg ValueError("yourerrormessage")
            expected_files         : List of (student_file, test_file) tuples for file comp.
            files_to_reveal        : Files hidden with self.cache_hidden_test_files() to add back to path
            custom_verification_function   : Function object to run during verify_program_output, that can modify the
                state of the testcase messages etc, and whether the test fails, to patch in extra checks. Takes in TestData instance.
            custom_verification_data       : Arbitrary data to use inside the custom_verification_function as attribute of TestData
            custom_verification_timeout    : Safety Timeout for the custom_verification_function, to prevent testbench crashing.
            custom_verification_timeout_msg: What to assign to test_data.msg.custom_verification_hook on fail

            For ommited ast related parameters see register_ast_test() docstring
        """
        name = self._set_default_test_name(name, hidden, private)

        test_data = TestData(name, score, hidden, private, student_file_name, TestData.TEST_SCRIPT)
        test_data.test_timeout = script_timeout_seconds
        test_data.input_data = input_data
        test_data.input_echoing = input_echoing
        test_data.expected.stdout = expected_stdout
        test_data.expected.stderr = expected_stderr
        test_data.expected.exception = expected_exception
        test_data.expected.filenames = expected_files
        test_data.files_to_reveal = files_to_reveal
        test_data.custom_verification_function = custom_verification_function
        test_data.custom_verification_data = custom_verification_data
        test_data.custom_verification_timeout = custom_verification_timeout
        test_data.custom_verification_timeout_msg = custom_verification_timeout_msg
        test_data.non_allowed_nodes = non_allowed_nodes
        test_data.non_allowed_functions = non_allowed_functions
        test_data.non_allowed_methods = non_allowed_methods
        test_data.non_allowed_imports = non_allowed_imports
        test_data.required_nodes = required_nodes
        test_data.required_functions = required_functions
        test_data.required_methods = required_methods
        test_data.required_imports = required_imports

        self.test_cases.append(test_data)

    @validate_call
    def register_ast_test(
        self,
        name: str | None = None,
        score: float | int  = 0,
        hidden: bool = False,
        private: bool = False,
        student_file_name="",
        non_allowed_nodes: list[type] | dict[type, str] = [],
        non_allowed_functions: list[str] = [],
        non_allowed_methods: list[str] = [],
        non_allowed_imports: list[str] = [],
        required_nodes: list[type] | dict[type, str] = [],
        required_functions: list[str] = [],
        required_methods: list[str] = [],
        required_imports: list[str] = [],
    ) -> None:
        """
        Description:
            Run abstract syntax tree checks on the student submission file, and any local imports

        Parameters:
            name                   : Test visible name. Default to "Visible/Hidden/Private {n_tests}" if None
            score                  : Points to give testcase pass if Ed's Per-Testcase scoring is enabled
            hidden                 : Hidden tests have pass/fail visible; students cannot see the input/output
            private                : Private tests are completely invisible to students
            student_file_name      : Root file to run astcheck on
            non_allowed_nodes      : Eg [ast.For, ast.While] or {ast.For: "for loop"}
            non_allowed_functions  : Disallowed function call names.
            non_allowed_methods    : Disallowed method names.
            non_allowed_imports    : Disallowed imports in student or imported files.
            required_nodes         : AST nodes required to appear in student's code.
            required_functions     : Function call names required in student code.
            required_methods       : Method names required in student code.
            required_imports       : Imports that must appear in student or local code.

        Known Limitations:
            - AST checking for methods and functions cannot distinguish shadowed function such as `a = exec; a(123)`
              finds the function call name as "a". Runtime or more creative ast checking required for this to be fixed.
        """
        if name is None:
            name = "AST Check"

        test_data = TestData(name, score, hidden, private, student_file_name, TestData.TEST_AST)
        test_data.non_allowed_nodes = non_allowed_nodes
        test_data.non_allowed_functions = non_allowed_functions
        test_data.non_allowed_methods = non_allowed_methods
        test_data.non_allowed_imports = non_allowed_imports
        test_data.required_nodes = required_nodes
        test_data.required_functions = required_functions
        test_data.required_methods = required_methods
        test_data.required_imports = required_imports
        test_data.expected.stderr = ""

        self.test_cases.append(test_data)

    @validate_call
    def register_pep8_test(
        self,
        name: str | None = None,
        score: float | int  = 0,
        hidden: bool = False,
        private: bool = False,
        student_file_name: str = "",
        ignored_tests: str = DEFAULT_PEP8_IGNORED,
        max_line_len: int = DEFAULT_PEP8_MAX_LINE_LEN,
    ) -> None:
        """
        Description:
            Run PEP8 style checks on the student submission file, and any local imports

        Parameters:
            name                : Test visible name. Default to "Visible/Hidden/Private {n_tests}" if None
            score               : Points to give testcase pass if Ed's Per-Testcase scoring is enabled
            hidden              : Hidden tests have pass/fail visible; students cannot see the input/output
            private             : Private tests are completely invisible to students
            student_file_name   : Root file to run pep8 check on
            ignored_tests       : Names of tests to ignore when run with `flake8 --ignore={ignored_tests}`
        """
        if name is None:
            name = "PEP8 Check"

        test_data = TestData(name, score, hidden, private, student_file_name, TestData.TEST_PEP8)
        test_data.success = False
        test_data.pep8_ignored_tests = ignored_tests
        test_data.pep8_max_line_len = max_line_len

        self.test_cases.append(test_data)


#######################################################################################


def run_function_test(
        test_data: TestData,
        hidden_file_dict: dict[str, Buffer],
        format_test_in_out_data_as_str: bool
    ) -> TestData:
    """
    Description:
        Test the return value, stdout, stderr etc of a student defined function.
        Includes the ability to check for mutated input. By default OS and other
        imports are blocked to mitigate attempts to bypass testing. Other nodes to
        check for via the abstract syntax tree can be specified to check that students
        use or do not use certain python features.

    Returns:
        Instance of TestData class.
    """

    test_data.msg.function_call = FUNCTION_CALLED_MSG.format(
        f"{test_data.function_name}{format_as_func_arg_string(test_data.expected.original_args)}"
    )
    test_data.msg.input = (
        INPUT_FEEDBACK_MSG.format(
            format_test_in_out_data(
                test_data.input_data,
                format_test_in_out_data_as_str
            )
        )
        if test_data.input_data != ""
        else ""
    )

    with HiddenFileManager(hidden_file_dict, test_data.files_to_reveal):
        run_astcheck_test(test_data, format_test_in_out_data_as_str)

        # Stops test, before running student code if unallowed features are used.
        if test_data.msg.astcheck:
            test_data.success = False
            return test_data

        encode_obj_data(test_data.expected.original_args, SUBPROC_FUNC_INPUT_FILENAME)
        # This is automatically removed after each function run
        file_path_to_run = STUDENT_FILE_PATH_PREFIX + RUN_TEST_SUBPROCESS_FILENAME
        with open(file_path_to_run, "w") as fp:
            fp.write(RUN_FUNCTION_TEST_SUBPROCESS_FILE)

        # If there is expected recursion counts, call counting should be enabled
        # Disabled by default as it is costly, time, and memory wise.
        enable_call_counting = test_data.expected.recursive_call_counts != []
        command = [
            "python",
            file_path_to_run,
            test_data.student_file_name,
            test_data.function_name,
            str(int(test_data.input_echoing)),
            str(int(enable_call_counting))
        ]

        (
            _,
            test_data.student.stdout,
            test_data.student.stderr,
            test_data.msg.timeout,
        ) = subprocess_run_with_truncated_output(
            command,
            test_data.input_data.encode(),
            MAX_SUBPROCESS_STDOUT_CHARS,
            OUTPUT_TRUNCATION_MSG,
            test_data.test_timeout,
        )

        load_data_object_from_file(
            test_data.student, "failed_return", SUBPROC_PICKLE_FAILED_FILENAME
        )
        if not hasattr(test_data.student, "failed_return"):
            load_data_object_from_file(
                test_data.student, "returned", SUBPROC_FUNC_RETURN_FILENAME
            )
        load_data_object_from_file(
            test_data.student, "final_args", SUBPROC_FUNC_ARGS_FILENAME
        )
        load_data_object_from_file(
            test_data.student, "exception", SUBPROC_EXC_FILENAME
        )
        if enable_call_counting:
            load_data_object_from_file(
                test_data.student, "recursive_call_count", SUBPROC_RECURSION_COUNT_FILENAME
            )

        # This must be inside hidden file manager context for expected file checking
        verify_program_output(test_data, format_test_in_out_data_as_str)

    return test_data


#######################################################################################


def run_script_test(
        test_data: TestData,
        hidden_file_dict: dict[str, Buffer],
        format_test_in_out_data_as_str: bool
    ) -> TestData:
    """
    Description:
        Test the stdout, stderr of a student defined python script.
        By default OS and other imports are blocked to mitigate attempts to bypass testing.
        Other nodes to check for via the abstract syntax tree can be specified to check that
        students use or do not use certain python features.

    Returns:
        Instance of TestData class.
    """

    test_data.msg.input = (
        INPUT_FEEDBACK_MSG.format(
            format_test_in_out_data(
                test_data.input_data,
                format_test_in_out_data_as_str
            )
        )
        if test_data.input_data != ""
        else ""
    )

    with HiddenFileManager(hidden_file_dict, test_data.files_to_reveal):

        run_astcheck_test(test_data, format_test_in_out_data_as_str)

        # Stops test, before running student code if unallowed features are used.
        if test_data.msg.astcheck:
            test_data.success = False
            return test_data

        # This is automatically removed after each function run
        file_path_to_run = STUDENT_FILE_PATH_PREFIX + RUN_TEST_SUBPROCESS_FILENAME
        with open(file_path_to_run, "w") as fp:
            fp.write(RUN_SCRIPT_TEST_SUBPROCESS_FILE)

        command = [
            "python",
            file_path_to_run,
            test_data.student_file_name,
            str(int(test_data.input_echoing)),
        ]

        (
            _,
            test_data.student.stdout,
            test_data.student.stderr,
            test_data.msg.timeout,
        ) = subprocess_run_with_truncated_output(
            command,
            test_data.input_data.encode(),
            MAX_SUBPROCESS_STDOUT_CHARS,
            OUTPUT_TRUNCATION_MSG,
            test_data.test_timeout,
        )

        load_data_object_from_file(
            test_data.student, "exception", SUBPROC_EXC_FILENAME
        )

        # This must be inside hidden file manager context for expected file checking
        verify_program_output(test_data, format_test_in_out_data_as_str)

    return test_data


#######################################################################################


def run_pep8_test(test_data: TestData) -> TestData:
    """
    Description:
        Run PEP8 style checks on the student submission file, and any local imports

    Returns:
        Instance of TestData class.
    """

    test_data.success = True

    filepath = STUDENT_FILE_PATH_PREFIX + test_data.student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)

    pep8_violations = ""
    for file in files_to_check:
        if DEFAULT_PEP8_TRUNCATION_LENGTH - len(pep8_violations) <= 0:
            break

        command = ["flake8", "--jobs=1", "--ignore=" + test_data.pep8_ignored_tests,
                   "--max-line-len=" + str(test_data.pep8_max_line_len),  file]
        _, proc_stdout, _, _ = (
            subprocess_run_with_truncated_output(
                command,
                "".encode(),
                DEFAULT_PEP8_TRUNCATION_LENGTH - len(pep8_violations),
                OUTPUT_TRUNCATION_MSG,
            )
        )

        pep8_violations += proc_stdout.replace(STUDENT_FILE_PATH_PREFIX, "")

    if pep8_violations != "":
        test_data.msg.pep8 = PEP8_ERROR_MSG + pep8_violations
        test_data.success = False

    return test_data


#######################################################################################


def run_astcheck_test(
        test_data: TestData,
        format_test_in_out_data_as_str: bool
    ) -> TestData:
    """
    Description:
        Run abstract syntax tree checks on the student submission file, and any local imports

    Returns:
        Instance of TestData class.
    """

    test_data.success = True

    # node checking allows for both passing an input as a list/tuple of nodes, or a dictionary
    # with node key, and description value. Passing a list uses the node names as the description
    if type(test_data.required_nodes) != dict:
        test_data.required_nodes = {node: node.__name__ for node in test_data.required_nodes}

    if type(test_data.non_allowed_nodes) != dict:
        test_data.non_allowed_nodes = {node: node.__name__ for node in test_data.non_allowed_nodes}

    filepath = STUDENT_FILE_PATH_PREFIX + test_data.student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)

    ast_violations = ""
    test_data.student.stderr = ""
    function_defs = set()

    for student_file in files_to_check:
        tree, ast_exception = create_ast_object(student_file)
        if tree is None:
            if ast_exception is not None:
                test_data.student.stderr += ast_exception
            ast_violations += f"Checking {student_file} caused errors.\n"
            test_data.success = False
            continue

        astchecker = AstChecker(student_file, tree)
        function_defs |= astchecker.defined_functions

        ast_violations += astchecker.astcheck_non_allowed_nodes(
            test_data.non_allowed_nodes,
        )
        ast_violations += astchecker.astcheck_required_nodes(
            test_data.required_nodes
        )
        ast_violations += astchecker.astcheck_non_allowed_functions(
            test_data.non_allowed_functions,
        )
        ast_violations += astchecker.astcheck_required_functions(
            test_data.required_functions
        )
        ast_violations += astchecker.astcheck_non_allowed_methods(
            test_data.non_allowed_methods,
        )
        ast_violations += astchecker.astcheck_required_methods(
            test_data.required_methods
        )
        ast_violations += astchecker.astcheck_non_allowed_imports(
            test_data.non_allowed_imports,
        )
        ast_violations += astchecker.astcheck_required_imports(
            test_data.required_imports
        )

    if test_data.student.stderr:
        verify_expected_stderr(test_data, format_test_in_out_data_as_str)

    if test_data.test_type == TestData.TEST_FUNCTION and test_data.function_name not in function_defs:
        ast_violations += MISSING_FUNC_DEF_MSG.format(test_data.function_name)

    if ast_violations != "":
        ast_violations = AST_VIOLATION_MSG + ast_violations
        test_data.msg.astcheck = truncate_string(
            ast_violations,
            DEFAULT_AST_TRUNCATION_LENGTH,
            OUTPUT_TRUNCATION_MSG
        )
        test_data.success = False

    return test_data


#######################################################################################


def verify_program_output(
        test_data: TestData,
        format_test_in_out_data_as_str: bool = False
    ) -> None:
    """
    Produce the errors displayed to students when a test fails.
    """
    if test_data.msg.timeout:
        test_data.success = False

    if test_data.custom_verification_function is not None:
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(test_data.custom_verification_timeout)  # seconds

        try:
            test_data.custom_verification_function(test_data)
        except TimeoutError:
            test_data.success = False
            test_data.msg.custom_verification_hook = test_data.custom_verification_timeout_msg
        except:
            test_data.success = False

    verify_expected_exception(test_data)

    # Cannot check expected stderr if checking for an exception
    if test_data.expected.exception is None:
        verify_expected_stderr(test_data, format_test_in_out_data_as_str)

        # Cannot check expected return if checking for a non empty stderr
        if test_data.expected.stderr == "":
            verify_function_return(test_data)
            verify_expected_recursive_call_counts(test_data)

    verify_expected_stdout(test_data, format_test_in_out_data_as_str)
    verify_check_mutated_input(test_data)
    verify_expected_mutated_args(test_data)
    verify_expected_files(test_data)

    # If there are no issues with the code except extra printed output, give half marks
    if (test_data.expected.stdout == ""
        and test_data.msg.student_stdout != ""
        and test_data.msg.student_exception == ""
        and test_data.msg.student_return == ""
        and test_data.msg.student_recursion_count == ""
        and test_data.msg.student_stderr == ""
        and test_data.msg.student_mutated == ""

    ):
        test_data.give_half_marks = True


#######################################################################################


def verify_expected_exception(test_data: TestData):
    """
    Check if student has raised the correct exception as expected.

    Note:
        To allow for custom exception checking without needing to import
        student code, only the name and the message are checked. Eg for ValueError('ABC')
        compares the strings 'ValueError' and 'ABC' against the expected.
    """

    if(type(test_data.expected.exception).__name__ != type(test_data.student.exception).__name__
        or str(test_data.expected.exception) != str(test_data.student.exception)
    ):

        test_data.success = False
        if test_data.student.exception is None:
            test_data.msg.student_exception = MISSING_EXCEPTION_MSG
        else:
            if test_data.expected.exception is None:
                test_data.msg.student_exception = UNEXPECTED_EXCEPTION_MSG.format(
                    type(test_data.student.exception).__name__,
                    repr(str(test_data.student.exception))
                )
            else:
                test_data.msg.student_exception = STUDENT_EXCEPTION_MSG.format(
                    type(test_data.student.exception).__name__,
                    repr(str(test_data.student.exception))
                )
    if test_data.expected.exception is not None:
        test_data.msg.expected_exception = EXPECTED_EXCEPTION_MSG.format(
            type(test_data.expected.exception).__name__,
            repr(str(test_data.expected.exception)),
        )



def verify_expected_stderr(
        test_data: TestData,
        format_test_in_out_data_as_str: bool
    ) -> None:
    """
    Check for incorrect stderr content
    Note:
        The presence or absence of test_data msg.student_stderr is used
        to determine whether to show both the received and expected output
        in test feedback. The expected output is always formatted for use in
        the test case report.
    """

    if test_data.expected.stderr == "":
        if format_test_in_out_data_as_str:
             formatted_proc_stderr = format_test_in_out_data(test_data.student.stderr, format_test_in_out_data_as_str)
        else:
            formatted_proc_stderr = test_data.student.stderr
    else:
        formatted_proc_stderr = format_test_in_out_data(test_data.student.stderr, format_test_in_out_data_as_str)
        test_data.msg.expected_stderr = (
            EXPECTED_STDERR_MSG.format(
                format_test_in_out_data(test_data.expected.stderr, format_test_in_out_data_as_str)
            )
        )

    if test_data.student.stderr != test_data.expected.stderr:
        test_data.msg.student_stderr = WRONG_STDERR_MSG.format(formatted_proc_stderr)
        test_data.success = False


def verify_expected_stdout(
        test_data: TestData,
        format_test_in_out_data_as_str: bool
    ) -> None:
    """
    Check for incorrect stdout content
    Note:
        The presence or absence of test_data msg.student_stdout is used
        to determine whether to show both the received and expected output
        in test feedback. The expected output is always formatted for use in
        the test case report.
    """
    if test_data.student.stdout != test_data.expected.stdout:
        if test_data.expected.stdout != "":
            test_data.msg.student_stdout = WRONG_STDOUT_MSG.format(
                format_test_in_out_data(test_data.student.stdout, format_test_in_out_data_as_str)
            )
        else:
            test_data.msg.student_stdout = UNEXPECTED_STDOUT_MSG.format(
                format_test_in_out_data(test_data.student.stdout, format_test_in_out_data_as_str)
            )
        test_data.success = False

    if test_data.expected.stdout != "":
        test_data.msg.expected_stdout = EXPECTED_STDOUT_MSG.format(
            format_test_in_out_data(test_data.expected.stdout, format_test_in_out_data_as_str)
        )



def verify_function_return(test_data: TestData):
    """
    Check for incorrect function return messages
    Note:
        The presence or absence of test_data msg.student_return is used
        to determine whether to show both the received and expected output
        in test feedback. The expected output is always formatted for use in
        the test case report.
    """
    if test_data.test_type == TestData.TEST_FUNCTION:
        if hasattr(test_data.student, "failed_return"):
           data_type, data_str = test_data.student.failed_return.split('\n')
           test_data.msg.student_return = STUDENT_RETURN_MSG.format(
                    data_type, data_str
            )

        elif hasattr(test_data.student, "returned"):
            if test_data.student.returned != test_data.expected.returned:
                test_data.msg.student_return = STUDENT_RETURN_MSG.format(
                    type(test_data.student.returned).__name__,
                    repr(test_data.student.returned),
                )
        else:
            test_data.msg.student_return = ERROR_RETURN_MSG

        test_data.msg.expected_return = EXPECTED_RETURN_MSG.format(
            type(test_data.expected.returned).__name__,
            repr(test_data.expected.returned),
        )

    if test_data.msg.student_return:
        test_data.success = False


def verify_expected_recursive_call_counts(test_data: TestData):
    """
    Check if the called function or any returned function calls in the called function
    (which could be recursive helper functions) have the expected number of recursive calls
    """
    if test_data.test_type == TestData.TEST_FUNCTION:
        if len(test_data.expected.recursive_call_counts) > 0 and hasattr(test_data.student, "recursive_call_count"):
            message = STUDENT_RECURSION_COUNT_MSG
            any_matches = False
            for func_name, call_count in test_data.student.recursive_call_count.items():
                    message += f"{func_name} has {call_count} recursive calls\n"
                    if (call_count in test_data.expected.recursive_call_counts):
                        any_matches = True

            test_data.success = any_matches
            if not any_matches:
                test_data.msg.student_recursion_count = message
            test_data.msg.expected_recursion_count = EXPECTED_RECURSION_COUNT_MSG.format(
                str(test_data.expected.recursive_call_counts)[1:-1].replace(",", " or")
            )


def verify_check_mutated_input(test_data: TestData):
    """ Check for mutated input """
    if (
        test_data.test_type == TestData.TEST_FUNCTION
        and test_data.function_fail_on_mutated_args
        and hasattr(test_data.student, "final_args")
        and test_data.student.final_args != test_data.expected.original_args
    ):
        test_data.msg.mutation_check = FAIL_ON_MUTATION_MSG + RECIEVED_ARGS_MSG.format(
            format_as_func_arg_string(test_data.student.final_args)
        )
        test_data.success = False


def verify_expected_mutated_args(test_data: TestData):
    """
    Check for expected mutated arguments
    Note:
        The presence or absence of test_data msg.final_args is used
        to determine whether to show both the received and expected output
        in test feedback. The expected output is always formatted for use in
        the test case report.
    """
    if (
        test_data.test_type == TestData.TEST_FUNCTION
        and test_data.expected.mutated_args is not None
        and hasattr(test_data.student, "final_args")
    ):
        if list(test_data.student.final_args) != list(test_data.expected.mutated_args):
            test_data.msg.student_mutated = RECIEVED_ARGS_MSG.format(
                format_as_func_arg_string(test_data.student.final_args)
            )
            test_data.success = False

        # Always create expected output string
        test_data.msg.expected_mutated = EXPECTED_MUTATED_ARGS_MSG.format(
            format_as_func_arg_string(test_data.expected.mutated_args)
        )


def check_files_equal(student_file_path, expected_file_path):
    expected_file_feedback = ""
    if not os.path.isfile(student_file_path):
        expected_file_feedback += f"{student_file_path} does not exist!\n"
    elif not os.path.isfile(expected_file_path):
        expected_file_feedback += f"{expected_file_path} does not exist!\n"
    elif not filecmp.cmp(student_file_path, expected_file_path, shallow=False):
        expected_file_feedback += (
            f"{student_file_path} and {expected_file_path} are not equal.\n"
        )
    return expected_file_feedback


def verify_expected_files(test_data: TestData):
    """ Check for files matching the expected files """
    expected_file_feedback = ""
    if len(test_data.expected.filenames) > 0:
        for student_file, expected_file in test_data.expected.filenames:
            student_file_path = STUDENT_FILE_PATH_PREFIX + student_file
            expected_file_path = STUDENT_FILE_PATH_PREFIX  + expected_file
            expected_file_feedback += check_files_equal(
                student_file_path, expected_file_path
            )

    if expected_file_feedback:
        expected_file_feedback = EXPECTED_FILES_MSG + expected_file_feedback
        test_data.success = False

    test_data.msg.expected_file = expected_file_feedback


#######################################################################################


def create_ast_object(file: str) -> tuple[ast.Module | None, str | None]:
    with open(file) as f:
        source = f.read()

    tree = None
    ast_exception = None
    try:
        tree = ast.parse(source, file)
    except Exception:
        ast_exception = traceback.format_exc(limit=0)

    return tree, ast_exception


class AstChecker:
    def __init__(self, file, tree):
        self.file = file
        self.ast_exception = None
        self.tree = tree
        self.visitor = CustomNodeVisitor(tree)
        self.defined_functions = self.visitor.defined_functions

    def astcheck_non_allowed_nodes(self, non_allowed_nodes):
        """
        Check for all non allowed
        See: https://docs.python.org/3/library/ast.html#ast-helpers
        """
        ast_violations = ""

        # Check for all non allowed nodes
        non_allowed_node_visitor = CustomNodeVisitor(
            self.tree, non_allowed_nodes.keys(),
        )
        for node in non_allowed_node_visitor.nodes:
            ast_violations += NON_ALLOWED_NODE_MSG.format(
                non_allowed_nodes[type(node)], node.lineno, self.file
            )
        return ast_violations

    def astcheck_required_nodes(self, required_nodes):
        """
        Check for all required nodes
        See: https://docs.python.org/3/library/ast.html#ast-helpers
        """
        ast_violations = ""

        # Check for all required nodes
        required_node_visitor = CustomNodeVisitor(self.tree, required_nodes.keys())
        required_nodes_found = [type(x) for x in required_node_visitor.nodes]
        for node in required_nodes:
            if node not in required_nodes_found:
                ast_violations += REQUIRED_NODE_MSG.format(required_nodes[node])

        return ast_violations

    def astcheck_non_allowed_functions(self, non_allowed_functions):
        """Check for all non allowed functions"""
        ast_violations = ""

        for name, lineno in self.visitor.function_calls:
            if name in non_allowed_functions:
                ast_violations += NON_ALLOWED_FUNCTION_MSG.format(
                    name, lineno, self.file
                )

        return ast_violations

    def astcheck_required_functions(self, required_functions):
        """Check for all required functions"""
        ast_violations = ""

        functions_found = [name for name, _ in self.visitor.function_calls]
        for function in required_functions:
            if function not in functions_found:
                ast_violations += REQUIRED_FUNCTION_MSG.format(function)

        return ast_violations

    def astcheck_non_allowed_methods(self, non_allowed_methods):
        """Check for all non allowed methods"""
        ast_violations = ""
        for name, lineno in self.visitor.method_calls:
            #print(node.attr)
            if name in non_allowed_methods:
                ast_violations += NON_ALLOWED_METHOD_MSG.format(
                    name, lineno, self.file
                )
        return ast_violations

    def astcheck_required_methods(self, required_methods):
        """ Check for all required methods """
        ast_violations = ""
        for method in required_methods:
            if method not in [name for name, _ in self.visitor.method_calls]:
                ast_violations += REQUIRED_METHOD_MSG.format(method)

        return ast_violations

    def astcheck_non_allowed_imports(self, non_allowed_imports):
        """Check for all non allowed imports"""
        ast_violations = ""
        for lib in self.visitor.imports:
            if lib in non_allowed_imports:
                ast_violations += NON_ALLOWED_IMPORT_MSG.format(lib, self.file)

        return ast_violations

    def astcheck_required_imports(self, required_imports):
        """Check for all required imports"""
        ast_violations = ""
        for lib in required_imports:
            if lib not in self.visitor.imports:
                ast_violations += REQUIRED_IMPORT_MSG.format(lib)

        return ast_violations


class CustomNodeVisitor(ast.NodeVisitor):
    def __init__(self, tree, types=[]):
        self.types = tuple(types)
        self.nodes = []
        self.imports = []
        self.function_calls = set()
        self.method_calls = set()
        self.attributes_called = set()
        self.stack = []
        self.attribute_paths = set()
        self.defined_functions = set()
        self.visit(tree)

        # Seperate out module functions and methods
        for callable_name, line_no in self.attributes_called:
            for path in self.attribute_paths:
                if callable_name == path[-1]:
                    if path[-2] in self.imports:
                        self.function_calls.add((callable_name, line_no))
                    else:
                        self.method_calls.add((callable_name, line_no))

    def visit(self, node) -> None:
        if any(isinstance(node, node_type) for node_type in self.types):
            self.nodes.append(node)
        super().visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Continue to visit Name and Attributes.
        self.visit(node.func)
        if isinstance(node.func, ast.Name):
            # callable name node are always functions
            self.function_calls.add((node.func.id, node.func.lineno))
        elif isinstance(node.func, ast.Attribute):
            # callable attributes are not necessarily methods they
            # can also be module functions, so will do a processing step
            # to filter out anything that has a root name as a module
            self.attributes_called.add((node.func.attr, node.func.lineno))
            self.visit(node.func.value)

    def visit_Name(self, node: ast.Name) -> None:
        if self.stack:
            # This is the root name of an attribute path eg a of a.b.c
            self.attribute_paths.add((node.id, *self.stack[::-1]))
            self.stack = []

    def visit_Attribute(self, node: ast.Attribute) -> None:
        self.stack.append(node.attr)
        # Continue to visit the values until terminating at a ast.Name node
        # Eg for a.b.c, visit c then b (attributes), terminating at a (name)
        self.visit(node.value)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.defined_functions.add(node.name)
        for sub_node in node.body:
            self.visit(sub_node)


#######################################################################################
# In order for safety checks to work properly all local imports from the
# file being tested must be found and checked accordingly for non allowed
# features or libraries, formatting etc.


def find_local_import_paths(filepath: str) -> list[str]:#
    """Create a list of relative local import paths"""
    file_path_components = filepath.rsplit("/", 1)
    path_prefix = ""
    if len(file_path_components) > 1:
        path_prefix = file_path_components[0] + "/"

    local_import_paths = []
    tree, _ = create_ast_object(filepath)
    if tree is None:
        return local_import_paths

    astchecker = AstChecker(filepath, tree)
    imports = astchecker.visitor.imports
    for imported in imports:
        path = imported.split(".")
        path = path_prefix + "/".join(path) + ".py"
        if os.path.isfile(path):
            local_import_paths.append(path)

    return local_import_paths


def recursive_find_local_import_paths(filepath: str) -> list[str]:
    """Create a list of every local import in the import tree"""
    local_imports = find_local_import_paths(filepath)
    files_checked = [filepath]

    while len(local_imports) > 0:
        next_import = local_imports.pop()
        if next_import not in files_checked:
            files_checked.append(next_import)
            local_imports += find_local_import_paths(next_import)

    return files_checked


#######################################################################################

def format_test_in_out_data(data: Any, format_as_string: bool) -> str:
    """Format string so it shows invisible characters and line wrapping when printed"""
    if format_as_string:
        return repr(data)
    return repr(data)[1:-1].replace("\\\\","\\").replace("\\n", "\\n\n").strip("\n").replace("\\'", "'")


def format_as_func_arg_string(data: list[Any] | tuple[Any]) -> str:
    """ Converting to list ensures single element tuple displays correctly """
    return f"({str(list(data))[1:-1]})"


def truncate_string(
        string: str,
        truncation_length: int,
        truncation_message: str,
        from_start: bool = False
    ) -> str:
    """ Trim a string to a specified size and attach a message if trimmed. """
    assert truncation_length >= 0, "Setup Issue: truncate_string: truncation_length <=0"
    if len(string) > truncation_length:
        if from_start:
            return (
                truncation_message
                + string[truncation_length - len(string) : len(string)]
            )
        return string[:truncation_length] + truncation_message
    return string
#

#######################################################################################


class HiddenFileManager:
    """
    Allow easy revealing and automatic removal of files from a hidden file dictionary
    by using the with keyword scope.
    """

    def __init__(self, hidden_file_dict: dict[str, Buffer], files_to_reveal: list[str]):
        self.hidden_file_dict = hidden_file_dict
        self.files_to_reveal = files_to_reveal
        for file in files_to_reveal:
            if file not in hidden_file_dict:
                raise Exception(
                    f"Setup Issue: File to reveal '{file}' not in hidden_file_dict!"
                )
            with open(file, "wb") as fp:
                fp.write(self.hidden_file_dict[file])

    def __enter__(self):
        pass

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        for file in self.files_to_reveal:
            os.remove(file)


#######################################################################################


class MaxFileSizeManager:
    '''
    Automatically truncate the file in this context if it is oversized on exit
    due to being finished with it, or an OSError erorring. A bit of a hacky fix
    as it can use a decent amount of disk space, however it is bounded by having
    a relevant test timeout.
    '''
    def __init__(self, filename: str, open_opt: str, truncation_size: int, truncation_message: str):
        self.filename = filename
        self.open_opt = open_opt
        self.truncation_size = truncation_size
        self.truncation_message = truncation_message

    def __enter__(self):
        self.file_fp  = open(self.filename, self.open_opt)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        ret = False
        self.file_fp.close()
        if (os.path.getsize(self.filename) > self.truncation_size):
            # immediately truncate over sized output file, to avoid a new OSError.
            fp = open(self.filename, "ab")
            fp.truncate(self.truncation_size)
            if exc_type == OSError:
                # Ignore this exception as it is from the file being oversized. (probably...)
                fp.write(self.truncation_message.encode())
                ret = True
            fp.close()
        return ret


def subprocess_run_with_truncated_output(
        command: list[str] | tuple[str],
        input_data: bytes ,
        max_output_size: int,
        truncation_message: str,
        timeout_seconds: int = 1
    ) -> tuple[subprocess.CompletedProcess[bytes] | None, str, str, str]:
    """
    subprocess.run() cannot limit the amount of input received from stdout and
    stederr.  Given the memory and disk constraintson Ed, instead of trying to
    reliably control reading system calls, instead read stdout/stderr to a file
    until an OSError occurs due to running out of disk space, or the process
    finishes, before truncating the file to some predetermined size if necessary
    to recover space, storing it as a string, and then deleting the file.
    Output filesize is also somewhat bounded by the given timeout.
    """
    proc_stdout = ""
    proc_stderr = ""
    timeout_message = ""
    timeout_suffix = "" if timeout_seconds == 1 else "s"
    proc_ret = None
    # Use binary read/write to preserve line endings
    with MaxFileSizeManager(SUBPROC_STDOUT_FILENAME, "wb", max_output_size, truncation_message) as stdout_file:
        with MaxFileSizeManager(SUBPROC_STDERR_FILENAME, "wb", max_output_size, truncation_message) as stderr_file:
            try:
                proc_ret = subprocess.run(
                    command,
                    stdout=stdout_file.file_fp,
                    stderr=stderr_file.file_fp,
                    input=input_data,
                    timeout=timeout_seconds,
                )
            except subprocess.TimeoutExpired:
                timeout_message = TIMEOUT_ERROR_MSG.format(
                    timeout_seconds, timeout_suffix
                )

    gc.collect()

    with open(SUBPROC_STDOUT_FILENAME, "rb") as stdout_fp:
        proc_stdout = stdout_fp.read().decode()
    with open(SUBPROC_STDERR_FILENAME, "rb") as stderr_fp:
        proc_stderr = stderr_fp.read().decode()
    os.remove(SUBPROC_STDOUT_FILENAME)
    os.remove(SUBPROC_STDERR_FILENAME)

    return proc_ret, proc_stdout, proc_stderr, timeout_message


#######################################################################################
# Encode/decode the python objects passed for checking program correctness
# into a object file so it can be passed to a subprocess and loaded directly.
# All testing happens on the subprocess to avoid the main testing code from crashing.


def encode_obj_data(input_data: Any, filename: str):
    """Create a file with python variable as binary data"""
    with open(filename, "wb") as f:
        dill.dump(input_data, f)


def decode_obj_data(filename: str):
    """Load python variable from binary encoded python variable file"""
    with open(filename, "rb") as f:
        data = dill.load(f)
    return data


def load_data_object_from_file(class_obj, attr: str, file: str):
    try:
        setattr(class_obj, attr, decode_obj_data(file))
        os.remove(file)
    except:
        pass


def handle_timeout(signum, frame):
        raise TimeoutError


#######################################################################################


class EdCustomGraderJson:
    TESTCASES = "testcases"

    def __init__(self):
        self.test_cases: list[EdTestCase] = []

    def add_test_case(
        self, name: str, score: float | int, hidden: bool, private: bool,
        passed: bool, ok: bool, feedback: str, max_score: float | int | None = None,
    ):
        test_case = EdTestCase(name, score, hidden, private, passed, ok, feedback, max_score)
        self.test_cases.append(test_case)
        return test_case

    def to_dict(self):
        entry = {}
        test_cases_as_dict = []
        for test_case in self.test_cases:
            test_cases_as_dict.append(test_case.to_dict())
        entry[self.TESTCASES] = test_cases_as_dict
        return entry


class EdTestCase:
        NAME = "name"
        SCORE = "score"
        OK = "ok"
        PASSED = "passed"
        HIDDEN = "hidden"
        PRIVATE = "private"
        FEEDBACK = "feedback"
        OUTPUT_FILES = "output_files"
        MAX_SCORE = "max_score"

        def __init__(
            self, name: str, score: float | int, hidden: bool, private: bool,
            passed: bool, ok: bool, feedback: str, max_score: float | int | None = None,
        ):
            self.name = name
            self.score = score
            self.max_score = max_score
            self.hidden = hidden
            self.private = private
            self.passed = passed
            self.ok = ok
            self.feedback = feedback
            self.output_files: list[EdOutputFile] = []
            self.test_data: TestData | None = None

        def add_output_file(self, path: str, title: str, required: bool):
            self.output_files.append(EdOutputFile(path, title, required))

        def to_dict(self):
            entry = {
                self.NAME : self.name,
                self.SCORE : self.score,
                self.HIDDEN : self.hidden,
                self.PRIVATE : self.private,
                self.PASSED : self.passed,
                self.OK : self.ok,
                self.FEEDBACK : self.feedback,
            }

            if self.max_score is not None and self.max_score != self.score:
                entry[self.MAX_SCORE] = self.max_score

            if self.output_files:
                output_files_as_dict = []
                for output_file in self.output_files:
                    output_files_as_dict.append(output_file.to_dict())
                entry[self.OUTPUT_FILES] = output_files_as_dict

            return entry


class EdOutputFile:
    PATH = "path"
    TITLE = "title"
    REQUIRED = "required"
    def __init__(self, path: str, title: str, required: bool):
        self.path = path
        self.title = title
        self.required = required

    def to_dict(self):
        entry = {
            self.PATH : self.path,
            self.TITLE : self.title,
            self.REQUIRED : self.required,
        }
        return entry


#######################################################################################


def generate_feedback_level(test_data: TestData, levels_to_reduce: int = 0, include_function_call: bool = True):
    if levels_to_reduce >= 1:
        pep8_truncation_length = max(
            DEFAULT_PEP8_TRUNCATION_LENGTH // levels_to_reduce, 200
        )
        ast_truncation_length = max(
            DEFAULT_AST_TRUNCATION_LENGTH // levels_to_reduce, 200
        )
        test_data.msg.pep8 = truncate_string(
            test_data.msg.pep8, pep8_truncation_length, OUTPUT_TRUNCATION_MSG
        )
        test_data.msg.astcheck = truncate_string(
            test_data.msg.astcheck, ast_truncation_length, OUTPUT_TRUNCATION_MSG
        )

    feedback_priority_order = [
        test_data.msg.pep8,
        test_data.msg.astcheck]

    if include_function_call:
        feedback_priority_order.append(test_data.msg.function_call)
    feedback_priority_order.extend([
        test_data.msg.input,
        test_data.msg.timeout,
        test_data.msg.memory_error,
        test_data.msg.student_file_not_found,
        test_data.msg.custom_verification_hook,
    ])
    # Only include information about the tests that have failed due to
    # limitations on stdout.
    if test_data.msg.student_exception:
        feedback_priority_order.append(test_data.msg.student_exception)
        feedback_priority_order.append(test_data.msg.expected_exception)
    if test_data.msg.student_stderr:
        feedback_priority_order.append(test_data.msg.student_stderr)
        feedback_priority_order.append(test_data.msg.expected_stderr)
    if test_data.msg.student_stdout:
        feedback_priority_order.append(test_data.msg.student_stdout)
        feedback_priority_order.append(test_data.msg.expected_stdout)
    if test_data.msg.student_return:
        feedback_priority_order.append(test_data.msg.student_return)
        feedback_priority_order.append(test_data.msg.expected_return)
    if test_data.msg.student_recursion_count:
        feedback_priority_order.append(test_data.msg.student_recursion_count)
        feedback_priority_order.append(test_data.msg.expected_recursion_count)
    feedback_priority_order.append(test_data.msg.mutation_check)
    if test_data.msg.student_mutated:
        feedback_priority_order.append(test_data.msg.student_mutated)
        feedback_priority_order.append(test_data.msg.expected_mutated)
    feedback_priority_order.append(test_data.msg.expected_file)

    if levels_to_reduce > len(feedback_priority_order):
        # Upper bound just to prevent infinite loop if something goes wrong
        return ""

    if levels_to_reduce == 1:
        student_stderr_truncation_length = max(len(test_data.msg.expected_stderr), 200)
        test_data.msg.student_stderr = truncate_string(
            test_data.msg.student_stderr,
            student_stderr_truncation_length,
            OUTPUT_TRUNCATION_FROM_START_MSG,
            from_start=True,
        )
        test_data.msg.student_stdout = truncate_string(
            test_data.msg.student_stdout,
            len(test_data.msg.expected_stdout),
            OUTPUT_TRUNCATION_MSG,
        )
        test_data.msg.student_return = truncate_string(
            test_data.msg.student_return,
            len(test_data.msg.expected_return),
            OUTPUT_TRUNCATION_MSG,
        )
        test_data.msg.student_mutated = truncate_string(
            test_data.msg.student_mutated,
            len(test_data.msg.expected_mutated),
            OUTPUT_TRUNCATION_MSG,
        )
    elif levels_to_reduce == 2:
        test_data.msg.custom_verification_hook = ""
        test_data.msg.student_stdout = ""
        test_data.msg.student_return = ""
        test_data.msg.student_mutated = ""

    # remove all empty feedback messages, so they are not considered in the priority ordering
    for i in range(0, len(feedback_priority_order), -1):
        if feedback_priority_order[i] == "":
            feedback_priority_order.pop()

    # for a high enough level, feedback message will end up empty.
    if levels_to_reduce > 2:
        for _ in range(levels_to_reduce - 2):
            if len(feedback_priority_order) > 0:
                feedback_priority_order.pop()
            else:
                break

    return "".join(feedback_priority_order)


def set_test_feedback_level(ed_test_grader_output: EdCustomGraderJson):

    if len(json.dumps(ed_test_grader_output.to_dict())) >= EDSTEM_MAX_GRADER_OUTPUT_CHARS:
        assert False, "Setup Issue: Too many test cases to have any output"

    # Show as much output as possible without exceeding the output limit which would crash grader.
    levels_to_reduce = 0
    while True:
        for ed_test_obj in ed_test_grader_output.test_cases:
            if ed_test_obj.test_data is not None:
                ed_test_obj.feedback = generate_feedback_level(
                    ed_test_obj.test_data, levels_to_reduce
                )
        ed_grader_json = json.dumps(ed_test_grader_output.to_dict())
        if len(ed_grader_json) < EDSTEM_MAX_GRADER_OUTPUT_CHARS:
            return ed_grader_json

        levels_to_reduce += 1


def find_relevant_output_files(test_data: TestData):
    output_files = []
    if (
        test_data.test_type == TestData.TEST_FUNCTION
        or test_data.test_type == TestData.TEST_SCRIPT
    ):
        for student_file, expected_file in test_data.expected.filenames:
            student_file_path = STUDENT_FILE_PATH_PREFIX + student_file
            expected_file_path = STUDENT_FILE_PATH_PREFIX + expected_file

            if check_files_equal(student_file_path, expected_file_path) != "":
                output_files.append(student_file_path)

            output_files.append(expected_file_path)

    return output_files


def write_to_test_log(ed_test_obj: EdTestCase, visible_log_fp, private_log_fp, is_test_report: bool, *msgs: str):
    test_visibility = "Visible"
    if ed_test_obj.hidden:
        test_visibility = "Hidden"
    elif ed_test_obj.private:
        test_visibility = "Private"

    pass_or_fail = "FAILED "
    score_str = f"{ed_test_obj.score} of {ed_test_obj.max_score}"
    if ed_test_obj.passed:
        pass_or_fail = "PASSED "
        score_str = f"{ed_test_obj.score} of {ed_test_obj.score}"

    # only show pass or fail if is execution transcript
    if is_test_report:
        score_str = f"{ed_test_obj.max_score}"
        pass_or_fail = ""

    fp = private_log_fp
    if not ed_test_obj.hidden and not ed_test_obj.private:
        fp = visible_log_fp

    test_type = "unspecified-test"
    if ed_test_obj.test_data is not None:
        test_type = ed_test_obj.test_data.test_type
    seperator = "=" * 100 + "\n"
    fp.write(seperator.encode())
    fp.write(
        f"{pass_or_fail}{test_visibility} <{test_type}> '{ed_test_obj.name}' ({score_str} points):\n".encode()
    )
    fp.write(seperator.encode())
    for msg in msgs:
        fp.write(msg.encode())


def generate_test_report_entry(test_data: TestData):
    messages = [
        test_data.msg.function_call,
        test_data.msg.input,
        test_data.msg.timeout,
        test_data.msg.memory_error,
        test_data.msg.student_file_not_found,
        test_data.msg.custom_verification_hook,
        test_data.msg.expected_exception,
        test_data.msg.expected_stderr,
        test_data.msg.expected_stdout,
        test_data.msg.expected_return,
        test_data.msg.expected_recursion_count,
        test_data.msg.mutation_check,
        test_data.msg.expected_mutated,
        test_data.msg.expected_file,

    ]
    # Ed does not display unicode chars in the file preview correctly.
    messages = [msg.replace("►", ">") for msg in messages]
    return messages


def generate_execution_transcript_entry(test_data: TestData):
    """  """
    # Ed does not display unicode chars in the file preview correctly.
    return [generate_feedback_level(test_data, 0, include_function_call=False).replace("►", ">")]


def create_test_report_testcases(ed_test_grader_output: EdCustomGraderJson):
    visible_test_report = ed_test_grader_output.add_test_case(
        "Test Case Report", 0, False, False, True, True, ""
    )
    visible_test_report.add_output_file(
        STUDENT_FILE_PATH_PREFIX + VISIBLE_TEST_REPORT_FILENAME,
        "Visible Test Report",
        False,
    )
    visible_test_report.add_output_file(
        STUDENT_FILE_PATH_PREFIX + VISIBLE_TEST_EXECUTION_TRANSCRIPT_FILENAME,
        "Visible Test Execution Transcript",
        False,
    )
    private_test_report = ed_test_grader_output.add_test_case(
        "Private Test Case Report", 0, False, True, True, True, ""
    )
    private_test_report.add_output_file(
        STUDENT_FILE_PATH_PREFIX + PRIVATE_TEST_REPORT_FILENAME,
        "Private Test Report",
        False,
    )
    private_test_report.add_output_file(
        STUDENT_FILE_PATH_PREFIX + PRIVATE_TEST_EXECUTION_TRANSCRIPT_FILENAME,
        "Private Test Execution Transcript",
        False,
    )

def flag_manual_intervention_testcase(ed_test_grader_output: EdCustomGraderJson, test_cases: list[TestData]):
    no_review = True
    for test in test_cases:
        if test.msg.student_file_not_found != "" or test.msg.astcheck != "" or test.msg.memory_error != "":
            no_review = False
    ed_test_grader_output.add_test_case(
        "Flag Manual Intervention", 0, False, True, no_review, True,
        "If this testcase has failed, the automated marks will be reviewed for possible partial marks by senior staff."
    )

def write_test_report_files(ed_test_list: list[EdTestCase]):
    visible_transcript_fp = open(
        STUDENT_FILE_PATH_PREFIX + VISIBLE_TEST_EXECUTION_TRANSCRIPT_FILENAME, "wb",
    )
    private_transcript_fp = open(
        STUDENT_FILE_PATH_PREFIX + PRIVATE_TEST_EXECUTION_TRANSCRIPT_FILENAME, "wb"
    )
    visible_report_fp = open(
        STUDENT_FILE_PATH_PREFIX + VISIBLE_TEST_REPORT_FILENAME, "wb"
    )
    private_report_fp = open(
        STUDENT_FILE_PATH_PREFIX + PRIVATE_TEST_REPORT_FILENAME, "wb"
    )
    for ed_test_obj in ed_test_list:
        if ed_test_obj.test_data is not None:
            write_to_test_log(
                ed_test_obj,
                visible_report_fp,
                private_report_fp,
                True,
                *generate_test_report_entry(ed_test_obj.test_data)
            )
            write_to_test_log(
                ed_test_obj,
                visible_transcript_fp,
                private_transcript_fp,
                False,
                *generate_execution_transcript_entry(ed_test_obj.test_data)
            )
            # Free up space as these are not used again later, only msg fields
            del ed_test_obj.test_data.student
            del ed_test_obj.test_data.expected

    visible_transcript_fp.close()
    private_transcript_fp.close()
    visible_report_fp.close()
    private_report_fp.close()


def set_test_output_files(ed_test_grader_output: EdCustomGraderJson):
    """
    Add output files for every expected file, and also student file if it does not
    match the expected file, show that it can be downloaded from the ed testcase.
    """
    for ed_test_obj in ed_test_grader_output.test_cases:
        if ed_test_obj.test_data is not None:
            if (
                ed_test_obj.test_data.test_type == TestData.TEST_FUNCTION
                or ed_test_obj.test_data.test_type == TestData.TEST_SCRIPT
            ):
                for file_name in find_relevant_output_files(ed_test_obj.test_data):
                    ed_test_obj.add_output_file(file_name, "", False)


#######################################################################################
# The runtestsubprocess files must be removed from path before running student code, so it is
# convient to store it directly in here, to avoid version control inconvenience.
# As runtestsubprocess is a seperate file, it needs to be freshly created after each test run
# to prevent the ability for it to be modified be a preceding testcase. It must have no
# dynamic local imports for this same reason, hence all relevant functions are directly embedded into the file.


# Used to patch the input() function to also print to stdout, when input_echoing is enabled.
# Patching builtins before loading allows the custom version to be used when the code is run
# by the import. Stack trace is cleaned up to make it look  almost the same as if not using input_echoing.

INPUT_WITH_ECHOING_FUNCTION = r"""
def input_with_echoing(prompt):
    try:
        out = input(prompt)
        # echo the input to stdout
        print(out)
    except Exception:
        stack = "Traceback (most recent call last):\n"
        stack += "".join(traceback.format_stack(limit=2)[:1])
        exit(stack+traceback.format_exc(limit=0))
    return out
"""

RECURSION_CHECKER_CLASS = r"""
import functools
import inspect

class RecursionChecker:
    def __init__(self):
        self._count = 0
        self.name = ""

    def __call__(self, fn):
        self.name = fn.__name__
        @functools.wraps(fn)
        def wrapped_fn(*args, **kwargs):
            # Grab the call stack.
            stack = inspect.stack()

            # Check to see if the call to this function is recursive.
            # Find the first call to the original function.
            i = 0
            is_recursive = False
            while i < len(stack) and not is_recursive:
                if stack[i].frame.f_code.co_name == 'wrapped_fn' and stack[i].frame.f_locals.get('self') is self:
                    # Check for a caller also being the original function further down the stack.
                    j = i + 1
                    while j < len(stack):
                        if stack[j].frame.f_code.co_name == 'wrapped_fn' and stack[j].frame.f_locals.get('self') is self:
                            is_recursive = True
                            break
                        j += 1
                i += 1
            if is_recursive:
                self._count += 1

            # Call the original function.
            return fn(*args, **kwargs)
        return wrapped_fn

    @property
    def count(self):
        '''Returns the number of recursive calls to the function'''
        return self._count
"""

ENCODING_FUNCTIONS = r"""
import dill

def encode_obj_data(input_data, filename):
    with open(filename,"wb") as f:
        dill.dump(input_data, f)

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return dill.load(f)
"""


SUBPROC_SCRIPT_FILENAMES = r"""
SUBPROC_EXC_FILENAME = "{0}"
""".format(
    SUBPROC_EXC_FILENAME,
)


RUN_SCRIPT_TEST_SUBPROCESS_FILE = (
    INPUT_WITH_ECHOING_FUNCTION
    + SUBPROC_SCRIPT_FILENAMES
    + ENCODING_FUNCTIONS
    + r"""
import os
import sys
import traceback
import builtins
import importlib.util
from builtins import input


# Remove the test file after loading, so it can be regenerated
# on next iteration, ensuring each test is isolated
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
INPUT_ECHOING = bool(int(sys.argv[2]))

if INPUT_ECHOING == True:
    builtins.input = input_with_echoing

try:
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))
except Exception as e:
    encode_obj_data(e, SUBPROC_EXC_FILENAME)
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1))
"""
)

SUBPROC_FUNC_FILENAMES = r"""
SUBPROC_FUNC_INPUT_FILENAME = "{0}"
SUBPROC_FUNC_RETURN_FILENAME = "{1}"
SUBPROC_FUNC_ARGS_FILENAME = "{2}"
SUBPROC_EXC_FILENAME = "{3}"
SUBPROC_RECURSION_COUNT_FILENAME = "{4}"
SUBPROC_PICKLE_FAILED_FILENAME = "{5}"
""".format(
    SUBPROC_FUNC_INPUT_FILENAME,
    SUBPROC_FUNC_RETURN_FILENAME,
    SUBPROC_FUNC_ARGS_FILENAME,
    SUBPROC_EXC_FILENAME,
    SUBPROC_RECURSION_COUNT_FILENAME,
    SUBPROC_PICKLE_FAILED_FILENAME,
)

RUN_FUNCTION_TEST_SUBPROCESS_FILE = (
    INPUT_WITH_ECHOING_FUNCTION
    + ENCODING_FUNCTIONS
    + RECURSION_CHECKER_CLASS
    + SUBPROC_FUNC_FILENAMES
    + r"""
import sys
import os
import traceback
import importlib
from collections import defaultdict
import resource

memory_limit_bytes = 50 * 1024 * 1024
fsize_limit_bytes = 1 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))
resource.setrlimit(resource.RLIMIT_FSIZE, (fsize_limit_bytes, fsize_limit_bytes))

# Remove the test file after loading, so it can be regenerated
# on next iteration, ensuring each test is isolated
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
INPUT_ECHOING = bool(int(sys.argv[3]))
COUNT_FUNC_CALLS = bool(int(sys.argv[4]))

FUNCTION_INPUT = decode_obj_data(SUBPROC_FUNC_INPUT_FILENAME)
os.remove(SUBPROC_FUNC_INPUT_FILENAME)

# Try import function from student code
# Run the function and check for timeout and mutating input
try:
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))

     # Wrap all functions in the call counting decorator.
    checkers = []
    if COUNT_FUNC_CALLS:
        for attr in dir(student_module):
            obj = getattr(student_module, attr)
            if inspect.isfunction(obj):
                checker = RecursionChecker()
                checkers.append(checker)
                wrapped_func = checker(obj)
                setattr(student_module, attr, wrapped_func)

    if INPUT_ECHOING == True:
        # patch the input function to echo the input to stdout
        student_module.input = input_with_echoing

    student_function = getattr(student_module, FUNCTION_NAME)
    got = student_function(*FUNCTION_INPUT)

    # Verify that the str representation of return value is not so big it will cause crashes.
    # Example would be a = "a"*100000; b = [a for _ in range(10000)]; str(b) much bigger than b
    if type(got) != str:
        val_str = None
        try:
            val_str = repr(got)
        except:
            pass

        if val_str is None or sys.getsizeof(val_str) >= fsize_limit_bytes:
            raise MemoryError("Function return value string representation size exceeded allowed limits.")

    try:
        encode_obj_data(got, SUBPROC_FUNC_RETURN_FILENAME)
    except:
        encode_obj_data(type(got).__name__+'\n'+str(got), SUBPROC_PICKLE_FAILED_FILENAME)

    encode_obj_data(FUNCTION_INPUT, SUBPROC_FUNC_ARGS_FILENAME)
    recursion_counts = defaultdict(int)
    for checker in checkers:
        recursion_counts[checker.name] = checker.count
    encode_obj_data(recursion_counts, SUBPROC_RECURSION_COUNT_FILENAME)

except Exception as e:
    encode_obj_data(e, SUBPROC_EXC_FILENAME)
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1))
"""
)

######################################################################################