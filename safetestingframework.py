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
DEFAULT_NON_ALLOWED_IMPORTS = ["sys", "os", "subprocess", "signal", "importlib"]

# This is set dynamically depending on the number of test cases in the testbench see run_test()
# MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION

OUTPUT_TRUNCATION_MESSAGE = "\n[...] Too much output was produced.\n"

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

MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE = "Setup Issue: Given function args / return value too much of the allocated feedback message length. Reduce the number of test cases or amount of data in the test input/output."

FUNCTION_CALLED_MSG = "► Called: {0}\n"
INPUT_FEEDBACK_MSG = "► Input:\n{0}\n"

EXPECTED_RETURN_MSG = "► Expected Return <{0}>:\n{1}\n"
STUDENT_RETURN_MSG = "► Returned <{0}>:\n{1}\n"

ERROR_RETURN_MSG = "► No value was returned due to errors\n"
WRONG_STDERR_MSG = "► Your program produced the following stderr output:\n{0}"
EXPECTED_STDERR_MSG = "► The expected stderr output is:\n{0}"

UNEXPECTED_STDOUT_MSG = "► Your program printed the following output when no printing was expected:\n{0}"
WRONG_STDOUT_MSG = "► Your program printed the following output:\n{0}"
EXPECTED_STDOUT_MSG = "► The expected printed output is:\n{0}"

PEP8_ERROR_MSG = "► The following style errors were found:\n"
AST_VIOLATION_MSG = "► The following AST violations were found:\n"
FILE_CHECK_ERROR_MSG = "► The following expected file errors were found:\n"

NON_ALLOWED_NODE_MSG = "Your program is not allowed to use a {0}. This occurred on line {1} of {2}.\n"
REQUIRED_NODE_MSG = "Your program must use a {0}.\n"
NON_ALLOWED_FUNCTION_MSG = 'Your program is not allowed to use the {0} function. This occurred on line {1} of {2}.\n'
NON_ALLOWED_IMPORT_MSG = 'Your program is not allowed to import {0}. Occured in file {1}.\n'

####################################################################

def verify_program_output(
        test_feedback, 
        proc_stdout, 
        proc_stderr, 
        expected_stdout, 
        expected_stderr, 
        expected_files, 
        student_file_path_prefix,
        value_returned=None,
        student_func_ret=None, 
        expected_func_ret=None
    ):
    ''' 
    Produce the errors displayed to students when a test fails. When a test function
    raises an exception, it is considered as having failed.
    '''
    
    test_feedback["expected_return"] = EXPECTED_RETURN_MSG.format(type(expected_func_ret).__name__, format_var_as_python_code(expected_func_ret))
    test_feedback["expected_stdout"] = EXPECTED_STDOUT_MSG.format(format_test_in_out_data(expected_stdout)) if expected_stdout != "" else ""
    test_feedback["expected_stderr"] = EXPECTED_STDERR_MSG.format(format_test_in_out_data(expected_stderr)) if expected_stderr != "" else ""
    
    
    errors = ""
    err_count = 4
    
    truncation_length = int((MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION * 0.48 - len(test_feedback)) / (err_count))
    assert truncation_length > 0, MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
    
    # Incorrect output files messages
    expected_file_feedback = check_expected_files_equal(expected_files, student_file_path_prefix)
    if expected_file_feedback != "":
        test_feedback["expected_file"] = FILE_CHECK_ERROR_MSG + expected_file_feedback
    
    errors = False
    # Function output error messages
    if value_returned and student_func_ret != expected_func_ret:
        errors = True
        test_feedback["student_return"] = STUDENT_RETURN_MSG.format(type(student_func_ret).__name__, format_var_as_python_code(student_func_ret))
    elif value_returned == False:
        errors = True
        test_feedback["student_return"] = ERROR_RETURN_MSG
    
    # Incorrect stderr messages
    if proc_stderr != expected_stderr:
        errors = True
        formatted_proc_stderr = proc_stderr if expected_stderr == "" else format_test_in_out_data(proc_stderr)
        test_feedback["student_stderr"] = WRONG_STDERR_MSG.format(formatted_proc_stderr)
            
    # Incorrect stdout messages
    if proc_stdout != expected_stdout: 
        errors = True
        if expected_stdout == "":
            test_feedback["student_stdout"] = UNEXPECTED_STDOUT_MSG.format(format_test_in_out_data(proc_stdout))
        else:
            test_feedback["student_stdout"] = WRONG_STDOUT_MSG.format(format_test_in_out_data(proc_stdout))
            
    for x in ("expected_file", "student_return", "student_stderr", "student_stdout"):
        if x in test_feedback.keys():
            test_feedback[x] = truncate_string(test_feedback[x], truncation_length, OUTPUT_TRUNCATION_MESSAGE)

    feedback_ordering = ["function_call", "input_feedback", "student_return", "expected_return", "student_stderr", "expected_stderr", "student_stdout", "expected_stdout", "expected_file"]
    
    if errors:
         feedback = "".join([test_feedback[x] for x in feedback_ordering if x in test_feedback.keys()])
         assert False, feedback
         

def run_function_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        function_name="",                                            # Function to test
        function_args=[],                                            # Must be wrapped in a tuple/list like test() -> [] or test(1) -> [1]
        function_expected=None,                                      # Expected return value for function
        function_timeout_seconds=1,                                  # Time in seconds until test fails due to timeout
        function_check_mutate=False,                                 # Check if the function input was mutated
        input_data="",                                               # Input that can be read by input() seperated by newlines
        input_echoing=True,                                          # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
        non_allowed_nodes=DEFAULT_NON_ALLOWED_NODES,                 # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        files_to_reveal=[],                                          # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict={},                                         # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ):
    '''
    Test the return value, stdout, stderr of a student defined function. Includes the ability to check for mutated input. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    check_arg_type(
        [str],
        student_file_name=student_file_name,
        function_name=function_name,
        input_data=input_data,
        expected_stdout=expected_stdout,
        expected_stderr=expected_stderr,
    )
        
    check_arg_type([list, tuple], function_args=function_args, expected_files=expected_files)
    check_arg_type([int], function_timeout_seconds=function_timeout_seconds)
    check_arg_type([bool], function_check_mutate=function_check_mutate, input_echoing=input_echoing)
    check_arg_type([dict], hidden_file_dict=hidden_file_dict)
    
    test_feedback = {}
    
    test_feedback["function_call"] = FUNCTION_CALLED_MSG.format(f"{function_name}({str(list(function_args))[1:-1]})")
    test_feedback["input_feedback"] = INPUT_FEEDBACK_MSG.format(format_test_in_out_data(input_data)) if input_data != "" else ""
    
    feedback_ordering = ["function_call", "input_feedback", "expected_return", "expected_stderr", "expected_stdout"]
    feedback = "".join([test_feedback[x] for x in feedback_ordering if x in test_feedback.keys()])
    
    used_feedback_len = len(feedback)

    assert used_feedback_len < int(MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK * 0.48), MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
    
    ast_violations = run_astcheck_test(
        student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes, 
        non_allowed_functions=non_allowed_functions, 
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes,
    )
    
    remaining_max_feedback_len = MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK - used_feedback_len
    assert remaining_max_feedback_len > 0, MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
    
    if ast_violations != "":
        assert False, feedback + truncate_string(ast_violations, remaining_max_feedback_len, OUTPUT_TRUNCATION_MESSAGE)
    
    encode_obj_data(function_args, "subproc-func-input")
    
    # This is automatically removed after each function run
    with open(RUN_TEST_SUBPROCESS_FILENAME, "w") as fp:
        fp.write(RUN_FUNCTION_TEST_SUBPROCESS_FILE)
        
    command = (
        "python", 
        RUN_TEST_SUBPROCESS_FILENAME, 
        student_file_name, 
        function_name,
        str(int(function_check_mutate)),
        str(int(input_echoing))
    )
      
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret, proc_stdout, proc_stderr = subprocess_run_with_truncated_output(
            command, 
            input_data.encode(), 
            remaining_max_feedback_len, 
            OUTPUT_TRUNCATION_MESSAGE, 
            function_timeout_seconds
        )
        
        student_func_ret = None
        value_returned = os.path.isfile("subproc-func-return")
        if value_returned:
            student_func_ret = decode_obj_data("subproc-func-return")
            os.remove("subproc-func-return")
            
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(test_feedback, proc_stdout, proc_stderr, expected_stdout, expected_stderr, expected_files, student_file_path_prefix, value_returned, student_func_ret, function_expected)
     
    return feedback
    
####################################################################

def run_script_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
        input_data="",                                               # Input that can be read by input() seperated by newlines
        input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
        non_allowed_nodes=DEFAULT_NON_ALLOWED_NODES,                 # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see run_astcheck_test
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        files_to_reveal=[],                                          # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict={},                                         # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ):
    '''
    Test the stdout, stderr of a student defined python script. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    
    check_arg_type(
        [str],
        student_file_name=student_file_name,
        input_data=input_data,
        expected_stdout=expected_stdout,
        expected_stderr=expected_stderr,
    )
        
    check_arg_type([list, tuple], expected_files=expected_files)
    check_arg_type([int], script_timeout_seconds=script_timeout_seconds)
    check_arg_type([bool], input_echoing=input_echoing)
    check_arg_type([dict], hidden_file_dict=hidden_file_dict)
    
    test_feedback = {}
    test_feedback["input_feedback"] = INPUT_FEEDBACK_MSG.format(format_test_in_out_data(input_data)) if input_data != "" else ""

    feedback_ordering = ["input_feedback", "expected_stderr", "expected_stdout"]
    feedback = "".join([test_feedback[x] for x in feedback_ordering if x in test_feedback.keys()])
    
    used_feedback_len = len(feedback)

    assert used_feedback_len < int(MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK * 0.48), MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
    
    ast_violations = run_astcheck_test(
        student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes, 
        non_allowed_functions=non_allowed_functions, 
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes,
        raise_error=False
    )
    
    remaining_max_feedback_len = MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK - used_feedback_len
    assert remaining_max_feedback_len > 0, MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
        
    if ast_violations != "":
        assert False, feedback + truncate_string(ast_violations, remaining_max_feedback_len, OUTPUT_TRUNCATION_MESSAGE)

    file_path_to_run = student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME
    
     # This is automatically removed after each function run
    with open(student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME, "w") as fp:
        fp.write(RUN_SCRIPT_TEST_SUBPROCESS_FILE)

    command = (
        "python", 
        file_path_to_run,
        student_file_name,
        str(int(input_echoing))
    )
    
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret, proc_stdout, proc_stderr = subprocess_run_with_truncated_output(
            command, 
            input_data.encode(), 
            MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION, 
            OUTPUT_TRUNCATION_MESSAGE, 
            script_timeout_seconds
        )
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(test_feedback, proc_stdout, proc_stderr, expected_stdout, expected_stderr, expected_files, student_file_path_prefix)
        
    return feedback

####################################################################

def run_pep8_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        ignored_tests=DEFAULT_PEP8_IGNORED,                          # Names of tests to ignore, see flake8 documentation.
        raise_error=True,
    ):
    '''
    Run PEP8 style checks on the student submission file, and any local imports
    '''
    
    check_arg_type([str], student_file_name=student_file_name, student_file_path_prefix=student_file_path_prefix, ignored_tests=ignored_tests)

    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)

    pep8_violations = ""
    
    for file in files_to_check:
        command = ('flake8', '--jobs=1', '--ignore='+ignored_tests, file)
        proc_ret = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            text=True
        )
        pep8_violations += proc_ret.stdout.replace('/home/', '')
        
    if raise_error and pep8_violations != "":
        pep8_violations = PEP8_ERROR_MSG + pep8_violations
        pep8_violations = truncate_string(pep8_violations, MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION, OUTPUT_TRUNCATION_MESSAGE)     
        assert False, pep8_violations
            
    return pep8_violations

def truncate_string(string, truncation_length, truncation_message):
    assert truncation_length > 0, MAX_FEEDBACK_LEN_EXCEEDED_MESSAGE
    if len(string) > truncation_length:
        return string[:truncation_length] + truncation_message
    return string


####################################################################

def run_astcheck_test(
        student_file_name="",                                        # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        required_nodes=[],                                           # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        non_allowed_nodes=[],                                        # Eg [ast.For, ast.While] as a list/tuple or with description eg {ast.For: "for loop"}, see ast library
        non_allowed_functions=[],                                    # Function names of any specific functions to disallow
        non_allowed_imports=[],                                      # Imports that are not allowed anywhere in student file or any local imports
        raise_error = True,
    ):
    '''
    Run abstract syntax tree checks on the student submission file, and any local imports
    '''
    check_arg_type([str], student_file_name=student_file_name, student_file_path_prefix=student_file_path_prefix)
    check_arg_type([list, tuple, dict], non_allowed_nodes=non_allowed_nodes, required_nodes=required_nodes)
    check_arg_type([list, tuple], non_allowed_functions=non_allowed_functions, non_allowed_imports=non_allowed_imports)
    
    if type(required_nodes) != dict:
        required_nodes = {node : node.__name__ for node in required_nodes}
    
    if type(non_allowed_nodes) != dict:
        non_allowed_nodes = {node : node.__name__ for node in non_allowed_nodes}
    
    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)
 
    ast_violations = ""
    for student_file in files_to_check:
        tree = create_ast_object(student_file)

        #  # Check for all non allowed nodes
        non_allowed_node_visitor = NodeTypeVisitor(non_allowed_nodes.keys(), tree)
        for node in non_allowed_node_visitor.nodes:
            ast_violations += NON_ALLOWED_NODE_MSG .format(non_allowed_nodes[node], node.lineno, student_file)
        
         # Check for all required nodes
        required_node_visitor = NodeTypeVisitor(required_nodes.keys(), tree)
        required_nodes_found = [type(x) for x in required_node_visitor.nodes]
        for node in required_nodes:
            if node not in required_nodes_found:
                ast_violations += REQUIRED_NODE_MSG.format(required_nodes[node])
                
        # Check for all non allowed functions
        name_visitor = NodeTypeVisitor([ast.Name], tree)
        for node in name_visitor.nodes:
            if node.id in non_allowed_functions:
                ast_violations += NON_ALLOWED_FUNCTION_MSG.format(node.id, node.lineno, student_file)

        # Check for all non allowed imports
        student_imports = find_imports(student_file)
        for lib in student_imports:
            if lib in non_allowed_imports:
                ast_violations += NON_ALLOWED_IMPORT_MSG.format(lib, student_file)

    if ast_violations != "":
        ast_violations = AST_VIOLATION_MSG + ast_violations
        
    if raise_error and ast_violations != "":
        ast_violations = truncate_string(ast_violations, MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK, OUTPUT_TRUNCATION_MESSAGE)
        assert False, ast_violations
        
    return ast_violations
    
class NodeTypeVisitor(ast.NodeVisitor):
    def __init__(self, types, tree, *args, **kwargs):
        self.types = tuple(types)
        self.nodes = []
        self.visit(tree)

    def visit(self, node):
        if isinstance(node, self.types):
            self.nodes.append(node)
        super().visit(node)
        
        
def create_ast_object(filename):
    with open(filename) as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename)
    except:
        assert False, traceback.format_exc(limit=-1)

    return tree

####################################################################
# In order for safety checks to work properly all local imports from the 
# file being tested must be found and checked accordingly for non allowed
# features or libraries, formatting etc.

def find_imports(filepath):
    ''' Generate a list of import names from a given file '''
    ast_tree = create_ast_object(filepath)
    visitor = NodeTypeVisitor((ast.Import, ast.ImportFrom), ast_tree)
    imports = []
    for node in visitor.nodes:
        for alias in node.names:
            imports.append(alias.name)
    return imports

def find_local_import_paths(filepath):
    ''' Create a list of relative local import paths '''
    file_path_components = filepath.rsplit('/',1)
    path_prefix = ""
    if (len(file_path_components) > 1):
        path_prefix = file_path_components[0] + "/"
        
    imports = find_imports(filepath)
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

####################################################################
def format_test_in_out_data(data):
    ''' Return string so it shows invisible characters and line wrapping'''
    if FORMAT_TEST_IN_OUT_DATA_AS_STRING:
        return format_var_as_python_code(data)
    return str([data])[2:-2].replace("\\n", "\\n\n").replace("\\'","'")

def format_var_as_python_code(data):
    ''' Return variable as string so it prints exactly as required for python assignment'''
    if type(data) == str:
        return str([data])[1:-1]
    return str(data)

def check_expected_files_equal(expected_files, student_file_path_prefix):
    errors = ""
    if (len(expected_files) > 0):
        for student_file, test_file in expected_files:
            if not os.path.isfile(student_file_path_prefix + student_file):
                errors +=  f"{student_file_path_prefix + student_file} does not exist!\n"
            elif not os.path.isfile(student_file_path_prefix + test_file):
                errors += f"{student_file_path_prefix + test_file} does not exist!\n"
            elif not filecmp.cmp(student_file_path_prefix + student_file, student_file_path_prefix + test_file, shallow=False):
                errors += f"{student_file_path_prefix + student_file} and {student_file_path_prefix + test_file} are not equal.\n"
        
    return errors

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
            
def subprocess_run_with_truncated_output(command, input_data, max_output_size, truncation_message, timeout_seconds):
    '''
    subprocess.run() cannot limit the amount of input received from stdout and stederr. Given the memory and disk constraints
    on Ed, instead of trying to reliably control reading system calls, instead read stdout/stderr to a file until
    an OSError occurs due to running out of disk space, or the process finishes, before truncating the file to some
    predetermined size if necessary to recover space, storing it as a string, and then deleting the file.  
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
                timeout_message = f"Your program took too long to run and was terminated after {timeout_seconds} second{timeout_suffix}. Do you have an infinite loop?\n" 
            
            stdout_fp.close()
            
        except OSError:
            # If too much output is generated there will be no more space on device
            pass
            
        if (os.path.getsize("stdout.txt") > max_output_size):
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
        stderr_fp = open("stderr.txt", "a")
        stderr_fp.truncate(max_output_size)
        stderr_fp.close()
        proc_stderr += truncation_message
        
    stderr_fp = open("stderr.txt", "rb") 
    proc_stderr = timeout_message + stderr_fp.read().decode() + proc_stderr
    stderr_fp.close()
    os.remove("stderr.txt")
    
    return proc_ret, proc_stdout, proc_stderr

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

def run_tests(SafeTestClass, setup_mode=False, show_all_passed_tests_first=True):
    global MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION
    global MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK
    test_list = get_test_methods_in_order(SafeTestClass)
    
    # Needs to be small enough so that each test can produce this much output on stdout and stderr
    # while having enough free characters to have all the JSON syntax and other stuff also printed.
    # 3x should be a decent overestimate to avoid the testing code ever crashing.
    MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION = int(EDSTEM_MAX_GRADER_OUTPUT_CHARS / (3 * len(test_list)))
    MAX_TEST_FEEDBACK_LEN_BEFORE_ERROR_RISK = int(EDSTEM_MAX_GRADER_OUTPUT_CHARS / (1.5 * len(test_list)))
    
    testbench = SafeTestClass()
    testcase_output = []
    grader_output = {}
    grader_output["testcases"] = testcase_output
    
    if setup_mode:
        testcase = get_testcase_dict("Debug Data", "#name(Debug Data) #private #score(0)")
        global FORMAT_TEST_IN_OUT_DATA_AS_STRING 
        FORMAT_TEST_IN_OUT_DATA_AS_STRING = True
        testcase["feedback"] = ""
        testcase["feedback"] += "All tests fail when SETUP_MODE is enabled, so that it is not left enabled by accident.\n"
        testcase["feedback"] += "FORMAT_TEST_IN_OUT_DATA_AS_STRING = True, so input and expected stdout/stderr can be copy pasted directly into testbench\n"
        testcase["feedback"] += "Having more test cases decreases this value accordingly, to prevent grader from crashing\n"
        testcase["feedback"] += f"> MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION: {MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION} chars\n"
        testcase_output.append(testcase)
    
    for test in test_list:
        test_method = getattr(testbench, test)
        testcase = get_testcase_dict(test_method.__name__, test_method.__doc__)
        try:
            feedback = test_method()
            if feedback != "":
                testcase["feedback"] = feedback
        except Exception as e:
            testcase["feedback"] = str(e)
            testcase["passed"] = False
            
        if setup_mode:
            testcase["feedback"] = "Setup Issue: Disable SETUP_MODE\n" + str(e)
            testcase["passed"] = False
            
        testcase_output.append(testcase)
        
    if show_all_passed_tests_first:
        testcase_output.sort(key=lambda x: not x["passed"])    
    
    print(json.dumps(grader_output))

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

RUN_FUNCTION_TEST_SUBPROCESS_FILE = INPUT_WITH_ECHOING_FUNCTION + \
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
FUNCTION_CHECK_MUTATE = bool(int(sys.argv[3]))
INPUT_ECHOING = bool(int(sys.argv[4]))

def encode_obj_data(input_data, filename):
    with open(filename,"wb") as f:
        pickle.dump(input_data, f)

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return pickle.load(f)

FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_INPUT_COPY = decode_obj_data("subproc-func-input")

os.remove("subproc-func-input")

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
    encode_obj_data(got, "subproc-func-return")
    
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1))

# Check for mutated input
if FUNCTION_CHECK_MUTATE and FUNCTION_INPUT != FUNCTION_INPUT_COPY:
    exit("Your code should not mutate the function input!")

'''
####################################################################
