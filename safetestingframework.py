# Safe Ed Assignment Testing Library V0.4.0 safetestingframework.py 
# Last Updated: 2025/07/18
# Author: Kacie Beckett <kacie.beckett@unimelb.edu.au> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20912/lessons/79913/slides/539891

import os
import subprocess
import pickle
import ast
import traceback
import json
import re
import filecmp

# DANGER: Be careful if developing locally, as importing this code will cause it to be 
# irreplaceably removed, unlike on Ed.

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

DEFAULT_PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
DEFAULT_STUDENT_FILE_PATH_PREFIX = "/home/"
DEFAULT_NON_ALLOWED_NODES = []
DEFAULT_NON_ALLOWED_FUNCTIONS = ["exec"]
DEFAULT_NON_ALLOWED_METHODS = ["exec"]
DEFAULT_NON_ALLOWED_IMPORTS = ["sys", "os", "subprocess", "signal", "importlib"]

# This is set dynamically depending on the number of test cases in the testbench see run_test()
# MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION

OUTPUT_TRUNCATION_MESSAGE = "\n[...] Too much output was produced.\n"
OUTPUT_TRUNCATION_FROM_START_MSG = "Too much output was produced. [...]\n"
# This is the maximum amount of output that can be printed by test code
# before Edstem crashes and dumps all of stdout to screen.
# Custom grader passes json object over stdout for Ed to parse.
# Note that this limit is imposed by Ed's json parser, and not imposed 
# on subprocesses, which will crash  due to exceeding memory availability or disk space 
EDSTEM_MAX_GRADER_OUTPUT_CHARS = 200000

# Not presently used for anything, but were found by testing
EDSTEM_TESTING_FILESYSTEM_MAX_SIZE_MB = 100
EDSTEM_STUDENT_DATA_MAX_SIZE_MB = 20

# Enabled in setup mode so that expected stdout/stderr can be easily copy pasted
# directly into the testbench variable for setup
FORMAT_TEST_IN_OUT_DATA_AS_STRING = False

FUNCTION_CALLED_MSG = "► Called: {0}\n"
INPUT_FEEDBACK_MSG = "► Input:\n{0}\n"

EXPECTED_RETURN_MSG = "► Expected <{0}>:\n{1}\n"
STUDENT_RETURN_MSG = "► Returned <{0}>:\n{1}\n"

ERROR_RETURN_MSG = "► No value was returned due to errors\n"
WRONG_STDERR_MSG = "► Your program produced the following stderr output:\n{0}\n"
EXPECTED_STDERR_MSG = "► The expected stderr output is:\n{0}\n"

UNEXPECTED_STDOUT_MSG = "► Your program printed the following output when no printing was expected:\n{0}\n"
WRONG_STDOUT_MSG = "► Your program printed the following output:\n{0}\n"
EXPECTED_STDOUT_MSG = "► The expected printed output is:\n{0}"

PEP8_ERROR_MSG = "► The following style errors were found:\n"
AST_VIOLATION_MSG = "► The following AST violations were found:\n"
FILE_CHECK_ERROR_MSG = "► The following expected file errors were found:\n"

NON_ALLOWED_NODE_MSG = "Your program is not allowed to use a {0}. This occurred on line {1} of {2}.\n"
REQUIRED_NODE_MSG = "Your program must use a {0}.\n"

NON_ALLOWED_FUNCTION_MSG = 'Your program is not allowed to use the {0} function. This occurred on line {1} of {2}.\n'
REQUIRED_FUNCTION_MSG = 'Your program must use the {0} function.\n'

NON_ALLOWED_METHOD_MSG = 'Your program is not allowed to use the {0} method. This occurred on line {1} of {2}.\n'
REQUIRED_METHOD_MSG = 'Your program must use the {0} method.\n'

NON_ALLOWED_IMPORT_MSG = 'Your program is not allowed to import {0}. Occured in file {1}.\n'
REQUIRED_IMPORT_MSG = 'Your program must use import {0}.\n'

FAIL_ON_MUTATION_MSG = "► Your code should not mutate the function input!\n"
RECIEVED_ARGS_MSG = "► Input Arguments after mutation:\n{0}\n"
EXPECTED_MUTATED_ARGS_MSG = "► Expected Mutated Input Arguments:\n{0}\n"

TIMEOUT_ERROR_MSG = "► Your program took too long to run and was terminated after {0} second{1}. Do you have an infinite loop?\n"
MAX_FEEDBACK_LEN_EXCEEDED_MSG = "Setup Issue: {0} Reduce the number of test cases or amount of data in the test input/output.\n"

SUBPROC_FUNC_INPUT_FILENAME = "subproc-func-input"
SUBPROC_FUNC_RETURN_FILENAME = "subproc-func-return"
SUBPROC_FUNC_ARGS_FILENAME = "subproc-func-args"

MAX_SUBPROCESS_STDOUT_CHARS = 20000
DEFAULT_PEP8_TRUNCATION_LENGTH = 1000
DEFAULT_AST_TRUNCATION_LENGTH = 1000

####################################################################

class TestData:
    TEST_FUNCTION = "function"
    TEST_SCRIPT = "script"
    TEST_AST = "ast"
    TEST_PEP8 = "pep8"
    
    def __init__(self, test_type):
        self.test_type = test_type
        self.success = False
        self.student_file_path_prefix: str
        self.function_check_expected_mutated_args: bool
        self.function_fail_on_mutated_args: bool
    
        self.msg = self.Messages()
        self.expected = self.Expected()
        self.student = self.Student()
        
    class Expected:
        def __init__(self):
            self.stdout: str
            self.stderr: str
            self.returned: any
            self.original_args: list | tuple
            self.mutated_args: list | tuple
            self.filenames: list[tuple[str, str]]
    
    class Student:
        def __init__(self):
            self.stdout: str
            self.stderr: str
            self.returned: any
            self.final_args: list | tuple
            #self.testproc_ret: subprocess.CompletedProcess
    
    class Messages:
        def __init__(self):
            self.pep8 = ""
            self.astcheck = ""
            
            self.function_call = ""
            self.input = ""
            self.timeout = ""
            
            self.student_stderr = ""
            self.expected_stderr = ""
            
            self.student_stdout = ""
            self.expected_stdout = ""
            
            self.student_return = ""
            self.expected_return = ""
            
            self.mutation_check = ""
            
            self.student_mutated = ""
            self.expected_mutated = ""
            
            self.expected_file = ""
            
def run_function_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        function_name="",                                            # Function to test
        function_args=[],                                            # Must be wrapped in a tuple/list like test() -> [] or test(1) -> [1]
        function_expected=None,                                      # Expected return value for function
        function_timeout_seconds=1,                                  # Time in seconds until test fails due to timeout
        function_fail_on_mutated_args=False,                         # Fail if function input was mutated
        function_expected_mutated_args=[],                           # Required mutated_args
        function_check_expected_mutated_args=False,                  # Check if the function input was mutated to match function_expected_mutated_args, ignored if fail_on_mutated_args
        input_data="",                                               # Input that can be read by input() seperated by newlines
        input_echoing=True,                                          # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        non_allowed_nodes=DEFAULT_NON_ALLOWED_NODES,                 # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_methods=DEFAULT_NON_ALLOWED_METHODS,             # Method name strings of any specific methods to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        required_functions=[],                                       # Function name strings of any specific functions to require
        required_methods=[],                                         # Method name strings of any specific methods to require
        required_imports=[],                                         # Imports that must be somewhere in student file or any local imports
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        files_to_reveal=[],                                          # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict={},                                         # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ) -> TestData:
    '''
    Test the return value, stdout, stderr of a student defined function. Includes the ability to check for mutated input. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    check_arg_type([str], student_file_name=student_file_name, function_name=function_name)
    check_arg_type([str], input_data=input_data, expected_stdout=expected_stdout, expected_stderr=expected_stderr)
    check_arg_type([list, tuple], function_args=function_args, function_expected_mutated_args=function_expected_mutated_args)
    check_arg_type([list, tuple], expected_files=expected_files, files_to_reveal=files_to_reveal)
    check_arg_type([int], function_timeout_seconds=function_timeout_seconds)
    check_arg_type([bool], function_fail_on_mutated_args=function_fail_on_mutated_args, function_check_expected_mutated_args=function_check_expected_mutated_args)
    check_arg_type([bool], input_echoing=input_echoing)
    check_arg_type([dict], hidden_file_dict=hidden_file_dict)
    
    if function_fail_on_mutated_args:
        function_check_expected_mutated_args = False
    
    test_data = TestData(TestData.TEST_FUNCTION)
    test_data.success = False
    test_data.student_file_path_prefix = student_file_path_prefix
    test_data.expected.stdout = expected_stdout
    test_data.expected.stderr = expected_stderr
    test_data.expected.files = expected_files
    test_data.expected.returned = function_expected
    test_data.expected.original_args = function_args
    test_data.expected.mutated_args = function_expected_mutated_args
    test_data.function_fail_on_mutated_args = function_fail_on_mutated_args
    
    test_data.msg.function_call = FUNCTION_CALLED_MSG.format(f"{function_name}({str(list(function_args))[1:-1]})")
    test_data.msg.input = INPUT_FEEDBACK_MSG.format(format_test_in_out_data(input_data)) if input_data != "" else ""

    test_data.astcheck_msg = run_astcheck_test(
        student_file_name=student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes,
        non_allowed_functions=non_allowed_functions,
        non_allowed_methods=non_allowed_methods,
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes,
        required_functions=required_functions,
        required_methods=required_methods,
        required_imports=required_imports,
    )
    
    # Stops test, before running student code if unallowed features are used.
    if test_data.msg.astcheck:
        return test_data
    
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        encode_obj_data(function_args, SUBPROC_FUNC_INPUT_FILENAME)
        # This is automatically removed after each function run
        file_path_to_run = student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME
        with open(file_path_to_run, "w") as fp:
            fp.write(RUN_SCRIPT_TEST_SUBPROCESS_FILE)
            
        command = ["python", file_path_to_run, student_file_name, function_name, str(int(input_echoing))]
        
        _proc_ret, test_data.student.stdout, test_data.student.stderr, test_data.msg.timeout \
            = subprocess_run_with_truncated_output(
            command, 
            input_data.encode(), 
            MAX_SUBPROCESS_STDOUT_CHARS , 
            OUTPUT_TRUNCATION_MESSAGE, 
            function_timeout_seconds
        )
        
        load_data_object_from_file(test_data, "student.returned", SUBPROC_FUNC_RETURN_FILENAME)
        load_data_object_from_file(test_data, "student.final_args", SUBPROC_FUNC_ARGS_FILENAME)
        
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(test_data)
        
    return test_data

####################################################################

def run_script_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
        input_data="",                                               # Input that can be read by input() seperated by newlines
        input_echoing=True,                                          # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        non_allowed_nodes=DEFAULT_NON_ALLOWED_NODES,                 # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_methods=DEFAULT_NON_ALLOWED_METHODS,             # Method name strings of any specific methods to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        required_functions=[],                                       # Function name strings of any specific functions to require
        required_methods=[],                                         # Method name strings of any specific methods to require
        required_imports=[],                                         # Imports that must be somewhere in student file or any local imports
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        files_to_reveal=[],                                          # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict={},                                         # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ) -> TestData:
    '''
    Test the stdout, stderr of a student defined python script. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    
    check_arg_type([str], student_file_name=student_file_name, input_data=input_data, expected_stdout=expected_stdout, expected_stderr=expected_stderr)
    check_arg_type([list, tuple], expected_files=expected_files, files_to_reveal=files_to_reveal)
    check_arg_type([int], script_timeout_seconds=script_timeout_seconds)
    check_arg_type([bool], input_echoing=input_echoing)
    check_arg_type([dict], hidden_file_dict=hidden_file_dict)
    
    test_data = TestData(TestData.TEST_SCRIPT)
    test_data.student_file_path_prefix = student_file_path_prefix
    test_data.expected_stdout = expected_stdout
    test_data.expected_stderr = expected_stderr
    test_data.expected_files = expected_files
  
    test_data.msg.input = INPUT_FEEDBACK_MSG.format(format_test_in_out_data(input_data)) if input_data != "" else ""
    
    test_data.msg.astcheck = run_astcheck_test(
        student_file_name=student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes,
        non_allowed_functions=non_allowed_functions,
        non_allowed_methods=non_allowed_methods,
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes,
        required_functions=required_functions,
        required_methods=required_methods,
        required_imports=required_imports,
    )
    
    # Stops test, before running student code if unallowed features are used.
    if test_data.msg.astcheck:
        test_data.success = False
        return test_data
    
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        # This is automatically removed after each function run
        file_path_to_run = student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME
        with open(file_path_to_run, "w") as fp:
            fp.write(RUN_SCRIPT_TEST_SUBPROCESS_FILE)
            
        command = ["python",  file_path_to_run, student_file_name, str(int(input_echoing))]
        
        _proc_ret, test_data.student.stdout, test_data.student.stderr, test_data.msg.timeout \
            = subprocess_run_with_truncated_output(
            command, 
            input_data.encode(), 
            MAX_SUBPROCESS_STDOUT_CHARS, 
            OUTPUT_TRUNCATION_MESSAGE, 
            script_timeout_seconds
        )
        
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(test_data)
        
    return test_data

####################################################################

def run_pep8_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        ignored_tests=DEFAULT_PEP8_IGNORED,                          # Names of tests to ignore, see flake8 documentation.
        truncation_length=DEFAULT_PEP8_TRUNCATION_LENGTH,            # Used internally to library not in testbench.
    ) -> TestData:
    '''
    Run PEP8 style checks on the student submission file, and any local imports
    '''    
    check_arg_type([str], student_file_name=student_file_name, student_file_path_prefix=student_file_path_prefix, ignored_tests=ignored_tests)

    test_data = TestData(TestData.TEST_PEP8)
    
    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)

    pep8_violations = ""
    for file in files_to_check:
        if truncation_length - len(pep8_violations) <= 0:
            break
        
        command = ['flake8', '--jobs=1', '--ignore='+ignored_tests, file]
        _proc_ret, proc_stdout, _proc_stderr, _timeout_message = subprocess_run_with_truncated_output(
            command, 
            "".encode(), 
            truncation_length - len(pep8_violations), 
            OUTPUT_TRUNCATION_MESSAGE
        )
         
        pep8_violations += proc_stdout.replace(student_file_path_prefix, '')
    
    if pep8_violations != "":
        test_data.msg.pep8 = PEP8_ERROR_MSG + pep8_violations
    else:
        test_data.success = True
            
    return test_data

####################################################################

def run_astcheck_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        non_allowed_nodes=[],                                        # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        non_allowed_functions=[],                                    # Function names of any specific functions to disallow
        non_allowed_methods=[],                                      # Method name strings of any specific methods to disallow
        non_allowed_imports=[],                                      # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        required_functions=[],                                       # Function name strings of any specific functions to require
        required_methods=[],                                         # Method name strings of any specific methods to require
        required_imports=[],                                         # Imports that must be somewhere in student file or any local imports
        truncation_length=DEFAULT_AST_TRUNCATION_LENGTH,            # Used only internally to library in other run functions, not in testbench
    ) -> TestData:
    '''
    Run abstract syntax tree checks on the student submission file, and any local imports
    '''
        
    check_arg_type([str], student_file_name=student_file_name, student_file_path_prefix=student_file_path_prefix)
    check_arg_type([list, tuple, dict], non_allowed_nodes=non_allowed_nodes, required_nodes=required_nodes)
    check_arg_type([list, tuple], non_allowed_functions=non_allowed_functions, non_allowed_methods=non_allowed_methods, non_allowed_imports=non_allowed_imports)
    check_arg_type([list, tuple], required_functions=required_functions, required_methods=required_methods, required_imports=required_imports)
    
    test_data = TestData(TestData.TEST_AST)
    
    # node checking allows for both passing an input as a list/tuple or nodes, or a dictionary
    # with node key, and description value. Passing a list uses the node names as the description
    if type(required_nodes) != dict:
        required_nodes = {node : node.__name__ for node in required_nodes}
    
    if type(non_allowed_nodes) != dict:
        non_allowed_nodes = {node : node.__name__ for node in non_allowed_nodes}
    
    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)
 
    ast_violations = ""
    for student_file in files_to_check:
        astchecker = AstChecker(student_file)

        ast_violations += astchecker.astcheck_nodes(non_allowed_nodes, required_nodes)
        ast_violations += astchecker.astcheck_functions(non_allowed_functions, required_functions)
        ast_violations += astchecker.astcheck_methods(non_allowed_methods, required_methods)
        ast_violations += astchecker.astcheck_imports(non_allowed_imports, required_imports)
            
    if ast_violations != "":
        ast_violations = AST_VIOLATION_MSG + ast_violations
        test_data.msg.astcheck = truncate_string(ast_violations, truncation_length, OUTPUT_TRUNCATION_MESSAGE)
    else:
        test_data.success = True

    return test_data

####################################################################

class AstChecker():
    def __init__(self, file):
        self.file = file
        self.tree = self.create_ast_object()
    
    def create_ast_object(self):
        with open(self.file) as f:
            source = f.read()
        try:
            tree = ast.parse(source, self.file)
        except:
            assert False, traceback.format_exc(limit=-1)

        return tree
        
    def find_imports(self):
        ''' Generate a list of import names from a given file '''
        
        visitor = self.NodeTypeVisitor((ast.Import, ast.ImportFrom), self.tree)
        imports = []
        for node in visitor.nodes:
            for alias in node.names:
                imports.append(alias.name)
        return imports
        
    def astcheck_nodes(self, non_allowed_nodes, required_nodes):
        ''' Check for all non allowed and required nodes '''
        ast_violations = ""
        
        # Check for all non allowed nodes
        non_allowed_node_visitor = self.NodeTypeVisitor(non_allowed_nodes.keys(), self.tree)
        for node in non_allowed_node_visitor.nodes:
            ast_violations += NON_ALLOWED_NODE_MSG.format(non_allowed_nodes[type(node)], node.lineno, self.file)
        
        # Check for all required nodes
        required_node_visitor = self.NodeTypeVisitor(required_nodes.keys(), self.tree)
        required_nodes_found = [type(x) for x in required_node_visitor.nodes]
        for node in required_nodes:
            if node not in required_nodes_found:
                ast_violations += REQUIRED_NODE_MSG.format(required_nodes[node])
            
        return ast_violations

    def astcheck_functions(self, non_allowed_functions, required_functions):
        ''' Check for all non allowed and required functions '''
        ast_violations = ""
        
        # Check for all non allowed functions
        name_visitor = self.NodeTypeVisitor([ast.Name], self.tree)
        for node in name_visitor.nodes:
            if node.id in non_allowed_functions:
                ast_violations += NON_ALLOWED_FUNCTION_MSG.format(node.id, node.lineno, self.file)
        
        # Check for all required functions
        functions_found = [node.id for node in name_visitor.nodes]
        for function in required_functions:
            if function not in functions_found:
                ast_violations += REQUIRED_FUNCTION_MSG.format(function)
        
        return ast_violations

    def astcheck_methods(self, non_allowed_methods, required_methods):
        ''' Check for all non allowed and required methods '''
        ast_violations = ""
        
        # Check for all non_allowed methods
        method_visitor = self.NodeTypeVisitor([ast.Attribute], self.tree)
        methods_found = [node.attr for node in method_visitor.nodes]
        for node in method_visitor.nodes:
            if node.attr in non_allowed_methods:
                ast_violations += NON_ALLOWED_METHOD_MSG.format(node.attr, node.lineno, self.file)

        # Check for all required methods
        for method in required_methods:
            if method not in methods_found:
                ast_violations += REQUIRED_METHOD_MSG.format(method)
                
        return ast_violations

    def astcheck_imports(self, non_allowed_imports, required_imports):
        ''' Check for all non allowed imports'''
        ast_violations = ""
        
        # Non allowed imports
        student_imports = self.find_imports(self.file)
        for lib in student_imports:
            if lib in non_allowed_imports:
                ast_violations += NON_ALLOWED_IMPORT_MSG.format(lib, self.file)

        # Required imports
        student_imports = self.find_imports(self.file)
        for lib in required_imports:
            if lib not in student_imports:
                ast_violations += REQUIRED_IMPORT_MSG.format(lib)
                
        return ast_violations
    
    class NodeTypeVisitor(ast.NodeVisitor):
        def __init__(self, types, tree):
            self.types = tuple(types)
            self.nodes = []
            self.visit(tree)

        def visit(self, node):
            if isinstance(node, self.types):
                self.nodes.append(node)
            super().visit(node)

####################################################################

def verify_program_output(test_data ):
    ''' 
    Produce the errors displayed to students when a test fails. 
    '''
    if test_data.msg.timeout:
        return test_data
    
    verify_expected_stderr(test_data)
    verify_expected_stderr(test_data)
    verify_function_return(test_data)
    verify_check_mutated_input(test_data)
    verify_expected_mutated_args(test_data)
    verify_expected_files(test_data)

####################################################################

def verify_expected_stderr(test_data: TestData):
     # Incorrect stderr messages
    if test_data.student.stderr != test_data.expected.stderr:
        if test_data.expected.stderr == "":
            formatted_proc_stderr = test_data.proc_stderr  
        else: 
            formatted_proc_stderr = format_test_in_out_data(test_data.proc.stderr)
        
        test_data.msg.student.stderr = WRONG_STDERR_MSG.format(formatted_proc_stderr)
        test_data.msg.expected.stderr = EXPECTED_STDERR_MSG \
            .format(format_test_in_out_data(test_data.expected.stderr)) if test_data.expected.stderr != "" else ""
        
        test_data.success = False

   
def verify_expected_stdout(test_data: TestData):
     # Incorrect stdout messages
    if test_data.proc_stdout != test_data.expected_stdout: 
        if test_data.expected_stdout != "":
            test_data.msg.student_stdout = WRONG_STDOUT_MSG.format(format_test_in_out_data(test_data.proc_stdout))
            test_data.msg.expected_stdout = EXPECTED_STDOUT_MSG.format(format_test_in_out_data(test_data.expected_stdout))
        else:
            test_data.msg.student_stdout = UNEXPECTED_STDOUT_MSG.format(format_test_in_out_data(test_data.proc_stdout))
            test_data.msg.expected_stdout = ""
        
        test_data.success = False


def verify_function_return(test_data: TestData):
    # Incorrect function return messages
    if hasattr(test_data, "student.returned") and test_data.student.returned != test_data.expected.returned:
        
        if test_data.student.func_succeeded:
            test_data.msg.student_return = STUDENT_RETURN_MSG \
                .format(
                    type(test_data.student_func_ret ).__name__, 
                    format_var_as_python_code(test_data.student_func_ret )
                )
        else:
            test_data.msg.student_return = ERROR_RETURN_MSG
        
        test_data.msg.expected_return = EXPECTED_RETURN_MSG \
            .format(
                type(test_data.expected_func_ret).__name__, 
                format_var_as_python_code(test_data.expected_func_ret)
            )
            
        test_data.success = False

def verify_check_mutated_input(test_data: TestData):
    # Check for mutated input
    if test_data.function_fail_on_mutated_args and test_data.student.final_args != test_data.expected.original_args:
        test_data.msg.mutation_check = FAIL_ON_MUTATION_MSG + RECIEVED_ARGS_MSG.format(format_as_func_arg_string(test_data.student_func_args))
        test_data.success = False


def verify_expected_mutated_args(test_data: TestData):
    # Check for expected mutated arguments
    if test_data.function_check_expected_mutated_args and test_data.student.final_args != test_data.expected.mutated_args:
        test_data.msg.student_mutated = RECIEVED_ARGS_MSG.format(format_as_func_arg_string(test_data.student.final_args))
        test_data.msg.expected_mutated = EXPECTED_MUTATED_ARGS_MSG.format(format_as_func_arg_string(test_data.expected.mutated_args))
        test_data.success = False


def verify_expected_files(test_data: TestData):
    expected_file_feedback = ""
    if (len(test_data.expected.filenames) > 0):
        for student_file, expected_file in test_data.expected.filenames:
            expected_file_path = test_data.student_file_path_prefix + expected_file
            student_file_path = test_data.student_file_path_prefix + student_file
            
            if not os.path.isfile(student_file_path):
                expected_file_feedback +=  f"{student_file_path} does not exist!\n"
            elif not os.path.isfile(expected_file_path):
                expected_file_feedback += f"{expected_file_path} does not exist!\n"
            elif not filecmp.cmp(student_file_path, expected_file_path, shallow=False):
                expected_file_feedback += f"{student_file_path} and {expected_file_path} are not equal.\n"
                
    if expected_file_feedback:
        test_data.success = False
        
    test_data.msg.expected_file = expected_file_feedback

        
####################################################################
# In order for safety checks to work properly all local imports from the 
# file being tested must be found and checked accordingly for non allowed
# features or libraries, formatting etc.

def find_local_import_paths(filepath):
    ''' Create a list of relative local import paths '''
    file_path_components = filepath.rsplit('/',1)
    path_prefix = ""
    if (len(file_path_components) > 1):
        path_prefix = file_path_components[0] + "/"
    
    astchecker = AstChecker(filepath)
    imports = astchecker.find_imports()
    local_import_paths = []
    for imported in imports:
        path = imported.split('.')
        path = path_prefix + "/".join(path) + ".py"
        if os.path.isfile(path):
            local_import_paths.append(path)
    
    return local_import_paths

def recursive_find_local_import_paths(filepath):
    ''' Create a list of every local import in the import tree '''
    local_imports = find_local_import_paths(filepath)
    files_checked = [filepath]
   
    while (len(local_imports) > 0):
       next_import = local_imports.pop()
       if next_import not in files_checked:
           files_checked.append(next_import)
           local_imports += find_local_import_paths(next_import)
    
    return files_checked
            
####################################################################

def format_test_in_out_data(data):
    ''' Return string so it shows invisible characters and line wrapping'''
    if FORMAT_TEST_IN_OUT_DATA_AS_STRING:
        return format_var_as_python_code(data)
    return str([data])[2:-2].replace("\\n", "\\n\n").strip("\n").replace("\\'","'")

def format_var_as_python_code(data):
    ''' Return variable as string so it prints exactly as required for python assignment'''
    if type(data) == str:
        return str([data])[1:-1]
    return str(data)

def format_as_func_arg_string(data):
    return f"({str(list(data))[1:-1]})"

####################################################################

def cache_hidden_test_files(files):
    '''
    Create a dictionary of Key, Value = Filename, File Content String
    for each file and remove it from path. The files can then be revealed
    only when running a given test, with HiddenFileManager, or its integration
    into run_function_test or run_script_test, to avoid data leakage. 
    '''
    file_dict = {}
    for file in files:
        with open(file, 'rb') as fp:
            file_dict[file] = fp.read()
        os.remove(file)
    return file_dict

class HiddenFileManager:
    ''' 
    Allow easy revealing and automatic removal of files from a hidden file dictionary
    by using the with keyword scope.
    '''
    def __init__(self, hidden_file_dict, files_to_reveal):
        self.hidden_file_dict = hidden_file_dict
        self.files_to_reveal = files_to_reveal
        for file in files_to_reveal:
            if file not in hidden_file_dict:
                raise Exception(f"Setup Issue: File to reveal '{file}' not in hidden_file_dict!")
            with open(file, 'wb') as fp:
                fp.write(self.hidden_file_dict[file])
        
    def __enter__(self):
        pass
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.files_to_reveal:
            os.remove(file)

####################################################################

def truncate_string(string, truncation_length, truncation_message, from_start=False):
    assert truncation_length >= 0, "Setup Issue: truncate_string: truncation_length <=0"
    if len(string) > truncation_length:
        if from_start:
            return truncation_message + string[truncation_length-len(string):len(string)]
        return string[:truncation_length] + truncation_message
    return string



# class MaxFileSizeManager:
#     ''' 
#     Automatically truncate the file in this context if it is oversized on exit
#     due to being finished with it, or an error.
#     '''
#     def __init__(self, filename, open_opt, truncation_size, truncation_message):
#         self.filename = filename
#         self.truncation_size = truncation_size
#         self.truncation_message = truncation_message
#         self.was_truncated = False
                
#     def __enter__(self):
#         self.file_fp  = open(filename, open_opt)
            
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.file_fp.close()
#         if (os.path.getsize(self.filename) > self.truncation_size):
#             # immediately truncate over sized output file, to avoid a new OSError.
#             stdout_fp = open("stdout.txt", "a")
#             stdout_fp.truncate(self.truncation_size)
#             stdout_fp.close()
#         if exc_type == OSError:
#             # Ignore this exception as it is from the file being oversized.
#             self.was_truncated = True
#             return True
        
            
            
def subprocess_run_with_truncated_output(command, input_data, max_output_size, truncation_message, timeout_seconds=1):
    '''
    subprocess.run() cannot limit the amount of input received from stdout and stederr. Given the memory and disk constraints
    on Ed, instead of trying to reliably control reading system calls, instead read stdout/stderr to a file until
    an OSError occurs due to running out of disk space, or the process finishes, before truncating the file to some
    predetermined size if necessary to recover space, storing it as a string, and then deleting the file.  
    
    Todo: 
        - look into if there is some nice way to redirect stdout of already running process to /dev/null
        - add a 'with' context class to handle managing the output files.
    '''
    proc_stdout = ""
    proc_stderr = ""
    timeout_message = ""
    timeout_suffix = "" if timeout_seconds == 1 else "s"
    # Two layers of try-except, one for each of stdout, stderr, as closing a file causes the 
    # buffered contents to be written to disk which can cause a new OSError due to insufficient space.
    proc_ret = None
    try:
        try:
            stdout_fp = open("stdout.txt", "wb") 
            stderr_fp = open("stderr.txt", "wb")

            try: 
                proc_ret = subprocess.run(command, stdout=stdout_fp, stderr=stderr_fp, input=input_data, timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                timeout_message = TIMEOUT_ERROR_MSG.format(timeout_seconds, timeout_suffix)
            
            stdout_fp.close()
            
        except OSError:
            # If too much output is generated there will be no more space on device
            pass
            
        if (os.path.getsize("stdout.txt") > max_output_size):
            # immediately truncate over sized output file, to avoid a new OSError.
            stdout_fp = open("stdout.txt", "a")
            stdout_fp.truncate(max_output_size)
            stdout_fp.close()
            proc_stdout += truncation_message
        
        stdout_fp = open("stdout.txt", "rb") 
        proc_stdout = stdout_fp.read().decode() + proc_stdout
        stdout_fp.close()
        os.remove("stdout.txt")
        stderr_fp.close()
        
    except OSError:
        # If too much output is generated there will be no more space on device
        pass
    
    if (os.path.getsize("stderr.txt") > max_output_size):
        # immediately truncate over sized output file, to avoid a new OSError.
        stderr_fp = open("stderr.txt", "a")
        stderr_fp.truncate(max_output_size)
        stderr_fp.close()
        proc_stderr += truncation_message
        
    stderr_fp = open("stderr.txt", "rb") 
    proc_stderr = stderr_fp.read().decode() + proc_stderr
    stderr_fp.close()
    os.remove("stderr.txt")
    
    return proc_ret, proc_stdout, proc_stderr, timeout_message

####################################################################
# Test Case Decorators for controlling Ed Integration
# use @hidden(), @private(), @score(), @setname()
# above unit test to control behaviour

def hidden(release_test_cases = False):
    ''' 
    Set the test case as hidden, so students can see pass/fail but not the input
    and output. Control variable overrides test to visible, so it can be 
    released to students easily.
    '''
    hidden = '#hidden' if release_test_cases == False else ''
    def dec(obj):
        obj.__doc__ = obj.__doc__ + hidden
        return obj
    return dec

def private(release_test_cases = False):
    ''' 
    Set the test case as private, so students cannot see the test exists. 
    Control variable overrides test to visible, so it can be 
    released to students easily.
    '''
    private = '#private' if release_test_cases == False else ''
    def dec(obj):
        if (obj.__doc__) == None:
            obj.__doc__ = " "
        obj.__doc__ = obj.__doc__ + private
        return obj
    return dec

def score(score):
    ''' 
    Set the score given for passing the test when per-testcase scoring is 
    enabled. Score can be an integer or a floating pointer number.
    '''
    def dec(obj):
        if (obj.__doc__) == None:
            obj.__doc__ = " "
        obj.__doc__ = obj.__doc__ + f"#score({score})"
        return obj
    return dec

def setname(name_override=None):
    ''' 
    Set the student visible testcase name from the test function name eg
    testVisible_1 shows as "Visible 1" or allows a direct override.
    '''
    def dec(obj):
        name = obj.__name__ if name_override == None else name_override
        if (obj.__doc__) == None:
            obj.__doc__ = " "
        obj.__doc__ = obj.__doc__ + f"#name({name.removeprefix('test').strip('_').replace('_',' ')})"
        return obj
    return dec

####################################################################
# Encode/decode the python objects passed for checking program correctness
# into a object file so it can be passed to a subprocess and loaded directly.
# All testing happens on the subprocess to avoid the main testing code from crashing.

def encode_obj_data(input_data, filename):
    ''' Create a file with python variable as binary data '''
    with open(filename,"wb") as f:
        pickle.dump(input_data, f)

def decode_obj_data(filename):
    ''' Load python variable from binary encoded python variable file '''
    with open(filename,"rb") as f:
        data = pickle.load(f)
    return data

def load_data_object_from_file(class_obj, attr, file):
    obj_exists = os.path.isfile(file)
    if obj_exists:
        setattr(class_obj, attr, decode_obj_data(file))
        os.remove(file)

####################################################################

def check_arg_type(valid_types, **kwargs):
    ''' Error out if the given keyword arguments have the wrong type, to prevent setup mistakes'''
    output = ""
    for name, arg in kwargs.items():
        if type(arg) not in valid_types:
            output += f"Test Argument {name} should be in {valid_types} but is {type(arg)}\n"
    if output:
        assert False, f"Setup Issue:\n" + output

def get_testcase_dict(function_name, docstring):
    ''' 
    Parse the given docstring of a function for #score() #name() #hidden #private
    and create a dictionary using the format specified by Edstem's custom grader json.
    '''
    if docstring == None:
        docstring = ""
        
    score_pattern = r"#score\((\d*\.?\d+)\)"
    name_pattern = r"#name\(((?:[^()\\]|\\.)*)\)"

    score = re.findall(score_pattern, docstring)[0]
    if score == "":
        score = 0
    elif '.' in score:
        score = float(score)
    else:
        score = int(score)

    matches = re.findall(name_pattern, docstring)
    if len(matches) > 0:
        name = re.sub(r'\\([()])', r'\1', matches[0])
    else:
        name = function_name
        
    private = True if "#private" in docstring else False
    hidden = True if "#hidden" in docstring and private == False else False
    testcase = {}
    testcase["name"] = name
    testcase["score"] = score
    testcase["ok"] = True
    testcase["passed"] = True
    testcase["hidden"] = hidden
    testcase["private"] = private

    return testcase

def get_test_methods_in_order(SafeTestClass):
    ''' Get a list of every test method object in the order it was defined in the test class '''
    methods = []
    for m_name in dir(SafeTestClass):
        method = getattr(SafeTestClass, m_name)
        if hasattr(method, '__code__') and callable(getattr(SafeTestClass, m_name)) and m_name.startswith("test"):
            methods.append((method.__code__.co_firstlineno, m_name))
            
    methods.sort()
    methods = [method[1] for method in methods]
    
    return methods


def generate_feedback_level(test_data: TestData, levels_to_reduce=0):
    if levels_to_reduce >= 1:
        pep8_truncation_length = max(DEFAULT_PEP8_TRUNCATION_LENGTH // levels_to_reduce, 200)
        ast_truncation_length = max(DEFAULT_AST_TRUNCATION_LENGTH // levels_to_reduce, 200)
        test_data.msg.pep8 = truncate_string(test_data.msg.pep8, pep8_truncation_length, OUTPUT_TRUNCATION_MESSAGE)
        test_data.msg.astcheck = truncate_string(test_data.msg.astcheck, ast_truncation_length, OUTPUT_TRUNCATION_MESSAGE)
    
    if test_data.test_type == TestData.TEST_PEP8:
        return test_data.msg.pep8
    
    feedback_priority_order = [
        test_data.msg.function_call,
        test_data.msg.input,
        test_data.msg.astcheck,
        test_data.msg.timeout,
        test_data.msg.student_stderr,
        test_data.msg.expected_stderr,
        test_data.msg.student_stdout,
        test_data.msg.expected_stdout,
        test_data.msg.student_return,
        test_data.msg.expected_return,
        test_data.msg.mutation_check,
        test_data.msg.student_mutated,
        test_data.msg.expected_mutated,
        test_data.msg.expected_file,
    ]
    
    if levels_to_reduce == 1:
        test_data.msg.student_stdout = truncate_string(test_data.msg.student_stdout, len(test_data.msg.expected_stdout), OUTPUT_TRUNCATION_MESSAGE)
        test_data.msg.student_return = truncate_string(test_data.msg.student_return, len(test_data.msg.expected_return), OUTPUT_TRUNCATION_MESSAGE)
        test_data.msg.student_mutated = truncate_string(test_data.msg.student_mutated, len(test_data.msg.expected_mutated), OUTPUT_TRUNCATION_MESSAGE)
    elif levels_to_reduce == 2:
        test_data.msg.student_stdout = ""
        test_data.msg.student_return = ""
        test_data.msg.student_mutated = ""
    
    # This needs high priority to be shown, as it is the mechanism for showing error messages.
    if levels_to_reduce >= 2:
        student_stderr_truncation_length = max(MAX_SUBPROCESS_STDOUT_CHARS // levels_to_reduce, len(test_data.msg.expected_stderr))
        test_data.msg.student_stderr = truncate_string(test_data.msg.student_stderr, student_stderr_truncation_length, OUTPUT_TRUNCATION_FROM_START_MSG, from_start=True)
        
    # remove all empty feedback messages, so they are not considered in the priority ordering
    for i in range(0,len(feedback_priority_order),-1):
        if feedback_priority_order[i] == "":
            feedback_priority_order.pop()
    
    # for a high enough level, feedback message will end up empty.
    if levels_to_reduce >= 3:
        for _ in range(levels_to_reduce - 1):
            if len(feedback_priority_order) > 0:
                feedback_priority_order.pop()
            else:
                break
    
    return "".join(feedback_priority_order)

def create_ed_test_json_obj(test_data_list: list[TestData]):
    testcase_json_list = []
    grader_output = {}
    grader_output["testcases"] = testcase_json_list
    
    for test_data in test_data_list:
        testcase_json_list.append(test_data.test_dict)
    
    if len(json.dumps(grader_output)) >= EDSTEM_MAX_GRADER_OUTPUT_CHARS:
        assert False, "Setup Issue: Too many test cases to have any output"
        
    # Show as much output as possible without exceeding the output limit which would crash grader.
    levels_to_reduce = 0
    
    while True:
        for testcase, test_data in zip(testcase_json_list, test_data_list):
            testcase["feedback"] = generate_feedback_level(test_data, levels_to_reduce)
        json_dump = json.dumps(grader_output)
        if len(json_dump) < EDSTEM_MAX_GRADER_OUTPUT_CHARS:
            return json_dump
        
        levels_to_reduce += 1
    
        
def run_tests(SafeTestClass, setup_mode=False, show_all_passed_tests_first=True):
    ''' Test Runner function that runs all test methods in a test class '''
    global MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION
    global MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK
    global FORMAT_TEST_IN_OUT_DATA_AS_STRING
    test_list = get_test_methods_in_order(SafeTestClass)
    
    # Needs to be small enough so that each test can produce this much output on stdout and stderr
    # while having enough free characters to have all the JSON syntax and other stuff also printed.
    MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK = int(EDSTEM_MAX_GRADER_OUTPUT_CHARS / (1.5 * len(test_list)))
    
    testbench = SafeTestClass()
    
    setup_mode_testcase = {}
    
    # if setup_mode:
    #     setup_mode_testcase = get_testcase_dict("Debug Data", "#name(Debug Data) #private #score(0)")
    #     FORMAT_TEST_IN_OUT_DATA_AS_STRING = True
    #     setup_mode_testcase["feedback"] = ""
    #     setup_mode_testcase["feedback"] += "All tests fail when SETUP_MODE is enabled, so that it is not left enabled by accident.\n"
    #     setup_mode_testcase["feedback"] += "FORMAT_TEST_IN_OUT_DATA_AS_STRING = True, so input and expected stdout/stderr can be copy pasted directly into testbench\n"
    #     setup_mode_testcase["feedback"] += "Having more test cases decreases this value accordingly, to prevent grader from crashing\n"
    #     setup_mode_testcase["feedback"] += f"> MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK : {MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK} chars\n"
    
    test_data_list = []
    for test in test_list:
        test_method = getattr(testbench, test)
        testcase = get_testcase_dict(test_method.__name__, test_method.__doc__)
        try:
            test_data: TestData = test_method()
        
            # Free up space
            del test_data.student
            del test_data.expected
            
            test_data.test_dict = testcase
            test_data_list.append(test_data)
            testcase["passed"] = test_data.success
            
        except Exception as e:
            testcase["feedback"] = str(e)
            testcase["passed"] = False
            testcase["ok"] = False # Test Bench Error.
            
        if setup_mode:
            testcase["feedback"] = "Setup Issue: Disable SETUP_MODE\n"
            testcase["passed"] = False
        
    
    ed_test_case_json = create_ed_test_json_obj(test_data_list)
    # if setup_mode_testcase:
    #     ed_test_case_json["testcases"].append(setup_mode_testcase)
    
    if show_all_passed_tests_first:
        ed_test_case_json["testcases"].sort(key=lambda x: not x["passed"])    
    
    print(json.dumps(ed_test_case_json))

####################################################################
# The runtestsubprocess files must be removed from path before running student code, so it is 
# convient to store it directly in here, to avoid version control inconvenience.
    
RUN_TEST_SUBPROCESS_FILENAME = "runtestsubprocess.py"

INPUT_WITH_ECHOING_FUNCTION = \
r'''
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
'''

# Used to patch the input() function to also print to stdout, when input_echoing is enabled
# Patching builtins before loading allows the custom version to be used when the code is run 
# by the import. Stack trace is cleaned up to make it look  almost the same as if not using input_echoing.
RUN_SCRIPT_TEST_SUBPROCESS_FILE = INPUT_WITH_ECHOING_FUNCTION + \
r'''
import os
import sys
import traceback
import builtins
import importlib.util
from builtins import input

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
INPUT_ECHOING = bool(int(sys.argv[2]))

if INPUT_ECHOING == True:
    builtins.input = input_with_echoing

try:
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1)) 
'''

SUBPROC_FILENAMES = \
r'''
SUBPROC_FUNC_INPUT_FILENAME = {0}
SUBPROC_FUNC_RETURN_FILENAME = {1}
SUBPROC_FUNC_ARGS_FILENAME = {2}
'''.format(SUBPROC_FUNC_INPUT_FILENAME, SUBPROC_FUNC_RETURN_FILENAME, SUBPROC_FUNC_ARGS_FILENAME)

RUN_FUNCTION_TEST_SUBPROCESS_FILE = INPUT_WITH_ECHOING_FUNCTION + SUBPROC_FILENAMES + \
r'''
import sys
import pickle
import os
import traceback
import importlib

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
INPUT_ECHOING = bool(int(sys.argv[3]))

def encode_obj_data(input_data, filename):
    with open(filename,"wb") as f:
        pickle.dump(input_data, f)

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return pickle.load(f)

FUNCTION_INPUT = decode_obj_data(SUBPROC_FUNC_INPUT_FILENAME)
os.remove(SUBPROC_FUNC_INPUT_FILENAME)

# Try import function from student code
# Run the function and check for timeout and mutating input 
try: 
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))
    if INPUT_ECHOING == True:
        # patch the input function to echo the input to stdout
        student_module.input = input_with_echoing
        
    if not hasattr(student_module, FUNCTION_NAME):
        exit(f"Your code should define a function named '{FUNCTION_NAME}'")

    student_function = getattr(student_module, FUNCTION_NAME)
    got = student_function(*FUNCTION_INPUT)
    encode_obj_data(got, SUBPROC_FUNC_RETURN_FILENAME)
    encode_obj_data(FUNCTION_INPUT, SUBPROC_FUNC_ARGS_FILENAME)
    
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1))
'''

####################################################################

