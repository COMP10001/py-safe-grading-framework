# Safe Ed Assignment Testing Library V0.3.0 safetestingframework.py 
# Last Updated: 2025/06/09
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

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
DEFAULT_STUDENT_FILE_PATH_PREFIX = "/home/"
DEFAULT_NON_ALLOWED_FUNCTIONS = ("exec",)
DEFAULT_NON_ALLOWED_IMPORTS = ("sys", "os", "subprocess", "signal", "importlib")

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


####################################################################

def run_function_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        function_name=None,                                          # Function to test
        function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
        function_expected = None,                                    # Expected return value for function
        function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
        check_mutate=False,                                          # Check if the function input was mutated
        input="",                                                    # Input that can be read by input() seperated by newlines
        input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
        files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ):
    '''
    Test the return value, stdout, stderr of a student defined function. Includes the ability to check for mutated input. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    
    run_astcheck_test(
        student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes, 
        non_allowed_functions=non_allowed_functions, 
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes
    )

    encode_obj_data(function_input, "subproc-func-input")
    encode_obj_data(function_expected, "subproc-func-expected")
    
    with open(RUN_TEST_SUBPROCESS_FILENAME, "w") as fp:
        fp.write(RUN_FUNCTION_TEST_SUBPROCESS_FILE)
        
    command = (
        "python", 
        RUN_TEST_SUBPROCESS_FILENAME, 
        student_file_name, 
        function_name,
        str(function_timeout_seconds), 
        str(int(check_mutate)),
        str(int(input_echoing))
    )
            
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret, proc_stdout, proc_stderr = subprocess_run_with_truncated_output(command, input.encode(), MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION, OUTPUT_TRUNCATION_MESSAGE)
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(proc_stdout, proc_stderr, expected_stdout, expected_stderr, expected_files, student_file_path_prefix)
        
    
    
    test_pass_feedback = ""
    return test_pass_feedback
    
####################################################################

def run_script_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
        input="",                                                    # Input that can be read by input() seperated by newlines
        input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        expected_files=[],                                           # List of tuples of (student_file, test_file), test_file can come from files_to_reveal
        non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
        non_allowed_functions=DEFAULT_NON_ALLOWED_FUNCTIONS,         # Function names of any specific functions to disallow
        non_allowed_imports=DEFAULT_NON_ALLOWED_IMPORTS,             # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
        files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ):
    '''
    Test the stdout, stderr of a student defined python script. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    
    run_astcheck_test(
        student_file_name,
        student_file_path_prefix=student_file_path_prefix,
        non_allowed_nodes=non_allowed_nodes, 
        non_allowed_functions=non_allowed_functions, 
        non_allowed_imports=non_allowed_imports, 
        required_nodes=required_nodes
    )

    
    file_path_to_run = student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME
    with open(student_file_path_prefix + RUN_TEST_SUBPROCESS_FILENAME, "w") as fp:
        fp.write(RUN_SCRIPT_TEST_SUBPROCESS_FILE)

    command = (
        "python", 
        file_path_to_run,
        student_file_name,
        str(script_timeout_seconds),
        str(int(input_echoing))
    )
    
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret, proc_stdout, proc_stderr = subprocess_run_with_truncated_output(command, input.encode(), MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION, OUTPUT_TRUNCATION_MESSAGE)
        # This must be inside hidden file manager context so expected file checking can use hidden files.
        verify_program_output(proc_stdout, proc_stderr, expected_stdout, expected_stderr, expected_files, student_file_path_prefix)
        

    test_pass_feedback = ""
    return test_pass_feedback

####################################################################

def run_pep8_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        ignored_tests=PEP8_IGNORED                                   # Names of tests to ignore, see flake8 documentation.
    ):
    '''
    Run PEP8 style checks on the student submission file, and any local imports
    '''
    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)

    pep8_violations = ""
    for file in files_to_check:
        proc_ret = subprocess.run(
                            ('flake8',
                            '--jobs=1',
                            '--ignore='+ignored_tests,
                            file),
                            stdout=subprocess.PIPE,
                            text=True
                        )
        pep8_violations += proc_ret.stdout.replace('/home/', '')
        
    if pep8_violations != "":
        pep8_violations = "The following style errors were found:\n" + pep8_violations
        
        if len(pep8_violations) > MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION:
            pep8_violations = pep8_violations[:MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION] + OUTPUT_TRUNCATION_MESSAGE
        
        assert False, pep8_violations
    
    test_pass_feedback = ""
    return test_pass_feedback
        

####################################################################

def run_astcheck_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
        non_allowed_functions=(),                                    # Function names of any specific functions to disallow
        non_allowed_imports = (),                                    # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=(),                                           # Eg ast.Name, see ast library
    ):
    '''
    Run abstract syntax tree checks on the student submission file, and any local imports
    '''
    filepath = student_file_path_prefix + student_file_name
    files_to_check = recursive_find_local_import_paths(filepath)
 
    output = ""
    for student_file in files_to_check:
        
        tree = create_ast_object(student_file)

        # Run the AST node type visitor over the tree to search for forbidden nodes.
        forbidden_node_visitor = NodeTypeVisitor(non_allowed_nodes)
        forbidden_node_visitor.visit(tree)
        for node in forbidden_node_visitor.nodes:
            output += "Your program is not allowed to use a '{}'. This occurred on line {} of {}.\n".format(type(node).__name__, node.lineno, student_file)
            
        required_node_visitor = NodeTypeVisitor(required_nodes)
        required_node_visitor.visit(tree)
        required_nodes_found = [type(x) for x in required_node_visitor.nodes]
        for node in required_nodes:
            if node not in required_nodes_found:
                output += f"Your program must use a '{node.__name__}'.\n"
                
        # Run the AST node type visitor over the tree to search for specific functions
        name_visitor = NodeTypeVisitor((ast.Name,))
        name_visitor.visit(tree)
        for node in name_visitor.nodes:
            if node.id in non_allowed_functions:
                output += 'Your program is not allowed to use the {} function. This occurred on line {} of {}.\n'.format(node.id, node.lineno, student_file)

        student_imports = find_imports(student_file)
        for lib in student_imports:
            if lib in non_allowed_imports:
                output += f'Your program is not allowed to import {lib}. Occured in file {student_file}.\n'

    if output != "":
        if len(output) > MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION:
            output = output[:MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION] + OUTPUT_TRUNCATION_MESSAGE
        assert False, output
    
    test_pass_feedback = ""
    return test_pass_feedback
    
class NodeTypeVisitor(ast.NodeVisitor):
    def __init__(self, types, *args, **kwargs):
        self.types = tuple(types)
        self.nodes = []

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
    visitor = NodeTypeVisitor((ast.Import, ast.ImportFrom))
    visitor.visit(ast_tree)
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
    Having #hidden in the docstring of a unit test causes the test to 
    be set as hidden in Ed's backend when using PyUnit testing.
    Boolean control variable means tests can be easily 
    realeased after the duedate by setting it to True, and rerunning
    the testcases for all students to set it as visible.
    '''
    hidden = '#hidden' if release_test_cases == False else ''
    def dec(obj):
        obj.__doc__ = obj.__doc__ + hidden
        return obj
    return dec

def private(release_test_cases = False):
    ''' 
    Having #private in the docstring of a unit test causes the test to 
    be set as private in Ed's backend when using PyUnit testing.
    Boolean control variable means tests can be easily 
    realeased after the duedate by setting it to True, and rerunning
    the testcases for all students to set it as visible.
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
    Having #score(value) in the docstring of a unit test sets the per
    testcase score to value when per-testcase scoring is enabled.
    Score can be an integer or a floating pointer number.
    '''
    def dec(obj):
        if (obj.__doc__) == None:
            obj.__doc__ = " "
        obj.__doc__ = obj.__doc__ + f"#score({score})"
        return obj
    return dec

def setname(name_override=None):
    ''' 
    Having #name(value) in the docstring of a unit test 
    sets the student visible testcase name to be value instead of 
    the function name. This function formats the name nicer by 
    removing test or test_ from the name and replacing '_' with ' ' 
    for example testVisible_1 shows as "Visible 1" or allows
    a direct override.
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
    with open(filename,"wb") as f:
        pickle.dump(input_data, f)

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        data = pickle.load(f)
    return data

####################################################################

def format_invis_chars(data):
    if type(data) == str:
        return str((data,))[2:-3].replace("\\n", "\\n\n")
    return str(data)

def verify_program_output(proc_stdout, proc_stderr, expected_stdout, expected_stderr, expected_files, student_file_path_prefix):
    ''' 
    Produce the errors displayed to students when a test fails. In a unit test
    assert is used to say the test failed, before moving onto the next.
    '''
    errors = ""
    if proc_stderr != expected_stderr:
        if expected_stderr == "":
            errors += "► Your program produced the following errors:\n{0}" \
            .format(proc_stderr)
        else:
            errors +="► Your program produced the following errors:\n{0}\n► The expected errors are:\n{1}" \
                .format(format_invis_chars(proc_stderr), format_invis_chars(expected_stderr))
            
    if proc_stdout != expected_stdout: 
        if expected_stdout == "":
            errors += "► Your program printed the following output when no printing was expected:\n{0}" \
            .format(format_invis_chars(proc_stdout), format_invis_chars(expected_stdout))
        else:
            errors += "► Your program printed the following output:\n{0}\n► The expected printed output is:\n{1}" \
            .format(format_invis_chars(proc_stdout), format_invis_chars(expected_stdout))
            
    errors += check_expected_files_equal(expected_files, student_file_path_prefix)
        
    if errors != "":
         assert False, errors

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
        with open(file, 'r') as fp:
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
            with open(file, 'w') as fp:
                fp.write(self.hidden_file_dict[file])
        
    def __enter__(self):
        pass
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.files_to_reveal:
            os.remove(file)

####################################################################

def subprocess_run_with_truncated_output(command, input_data, max_output_size, truncation_message):
    '''
    subprocess.run() cannot limit the amount of input received from stdout and stederr. Given the memory and disk constraints
    on Ed, instead of trying to reliably control reading system calls, instead read stdout/stderr to a file until
    an OSError occurs due to running out of disk space, or the process finishes, before truncating the file to some
    predetermined size if necessary to recover space, storing it as a string, and then deleting the file.  
    '''
    proc_stdout = ""
    proc_stderr = ""
    
    # Two layers of try-except, one for each of stdout, stderr, as closing a file causes the 
    # buffered contents to be written to disk which can cause an OSError due to insufficient space.
    try:
        try:
            stdout_fp = open("stdout.txt", "wb") 
            stderr_fp = open("stderr.txt", "wb")
            proc_ret = subprocess.run(command, stdout=stdout_fp, stderr=stderr_fp, input=input_data)
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
    proc_stderr = stderr_fp.read().decode() + proc_stderr
    stderr_fp.close()
    os.remove("stderr.txt")
    
    return proc_ret, proc_stdout, proc_stderr

####################################################################

def get_testcase_dict(function_name, docstring):
    ''' 
    Parse the given docstring of a function for #score() #name() #hidden #private
    and create a dictionary using the format specified by Edstem's custom grader json.
    '''
    if docstring == None:
        docstring = ""
        
    score_pattern = r"#score\((\d*\.?\d+)\)"
    name_pattern = r"#name\(((?:[^()\\]|\\.)*)\)"

    try:
        score = re.findall(score_pattern, docstring)[0]
        if '.' in score:
            score = float(score)
        else:
            score = int(score)
    except:
        score = 0

    try:
        matches = re.findall(name_pattern, docstring)[0]
        name = "".join([re.sub(r'\\([()])', r'\1', match) for match in matches])
    except:
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

def run_tests(SafeTestClass, debug_output=True, show_all_passed_tests_first=True):
    global MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION
    test_list = get_test_methods_in_order(SafeTestClass)
    
    # Needs to be small enough so that each test can produce this much output on stdout and stderr
    # while having enough free characters to have all the JSON syntax and other stuff also printed.
    # 2.5x should be a decent overestimate to avoid the testing code ever crashing.
    MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION = int(EDSTEM_MAX_GRADER_OUTPUT_CHARS / (2.5 * len(test_list)))
    
    testbench = SafeTestClass()
    testcase_output = []
    grader_output = {}
    grader_output["testcases"] = testcase_output
    
    if debug_output:
        testcase = get_testcase_dict("Debug Data", "#name(Debug Data) #private #score(0)")
        testcase["feedback"] = "# More test cases decreases this value accordingly\n"
        testcase["feedback"] += f"MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION: {MAX_PROCESS_STDOUT_STDERR_OUTPUT_LENGTH_BEFORE_TRUNCATION} bytes\n"
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
        testcase_output.append(testcase)
        
    if show_all_passed_tests_first:
        testcase_output.sort(key=lambda x: not x["passed"])    
    
    
    print(json.dumps(grader_output))

####################################################################
# The runtestsubprocess files must be removed from path before running student code, so it is 
# convient to store it directly in here, to avoid version control inconvenience.
# Note: All occurances of \ need to be escaped as \\ in multi line strings
    
RUN_TEST_SUBPROCESS_FILENAME = "runtestsubprocess.py"

# Used to patch the input() function to also print to stdout, when input_echoing is enabled
# Patching builtins before loading allows the custom version to be used when the code is run 
# by the import. Stack trace is cleaned up to make it look  almost the same as if not using input_echoing.
RUN_SCRIPT_TEST_SUBPROCESS_FILE = \
'''
import os
import sys
import signal
import traceback
import builtins
import importlib.util
from builtins import input

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_TIMEOUT_SECONDS = int(sys.argv[2])
INPUT_ECHOING = bool(int(sys.argv[3]))
TIMEOUT_SUFFIX = "" if FUNCTION_TIMEOUT_SECONDS == 1 else "s"

def input_with_echoing(prompt):
    try:
        out = input(prompt)
        print(out) # echo the input to stdout
    except Exception:
        stack = "Traceback (most recent call last):\\n" 
        stack += "".join(traceback.format_stack(limit=2)[:1])
        exit(stack+traceback.format_exc(limit=0)) 
    return out

if INPUT_ECHOING == True:
    builtins.input = input_with_echoing

def handle_timeout(signum, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

try:
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))
except TimeoutError:
    exit(f"Your program took too long to run and was terminated after {FUNCTION_TIMEOUT_SECONDS} second{TIMEOUT_SUFFIX}. Do you have an infinite loop?")
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1)) 
finally:
    signal.alarm(0)
'''

RUN_FUNCTION_TEST_SUBPROCESS_FILE = \
'''
import sys
import pickle
import os
import signal
import traceback
import importlib

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
FUNCTION_TIMEOUT_SECONDS = int(sys.argv[3])
FUNCTION_CHECK_MUTATE = bool(int(sys.argv[4]))
INPUT_ECHOING = bool(int(sys.argv[5]))

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return pickle.load(f)

FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_INPUT_COPY = decode_obj_data("subproc-func-input")
FUNCTION_EXPECTED = decode_obj_data("subproc-func-expected")

os.remove("subproc-func-input")
os.remove("subproc-func-expected")

TIMEOUT_SUFFIX = "" if FUNCTION_TIMEOUT_SECONDS == 1 else "s"

def input_with_echoing(prompt):
    try:
        out = input(prompt)
        print(out) # echo the input to stdout
    except Exception:
        stack = "Traceback (most recent call last):\\n" 
        stack += "".join(traceback.format_stack(limit=2)[:1])
        exit(stack+traceback.format_exc(limit=0)) 
    return out

def format_invis_chars(data):
    if type(data) == str:
        # This forces it to show characters as being escaped and wrapped in quotation marks for consistency
        return str((data,))[1:-2]
    return str(data)

def handle_timeout(signum, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

# Try import function from student code
# Run the function and check for timeout and mutating input 
try: 
    # Use importlib instead of import keyword in case the studentfile has dashes eg student-file.py
    student_module = importlib.import_module(STUDENT_FILE_NAME.removesuffix(".py"))
    
    if INPUT_ECHOING == True:
        # patch the input function to echo the input to stdout
        student_module.input = input_with_echoing

    exec("student_function = student_module.%s" % (FUNCTION_NAME,))
    got = student_function(*FUNCTION_INPUT)
except TimeoutError:
    exit(f"Your program took too long to run and was terminated after {FUNCTION_TIMEOUT_SECONDS} second{TIMEOUT_SUFFIX}. Do you have an infinite loop?")
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1)) 
finally:
    signal.alarm(0)

# Check for mutated input if desired.
if FUNCTION_CHECK_MUTATE and FUNCTION_INPUT != FUNCTION_INPUT_COPY:
    exit("Your code should not mutate the function input!")

if got != FUNCTION_EXPECTED:
    function_call = f"{FUNCTION_NAME}{FUNCTION_INPUT_COPY}"
    if len(FUNCTION_INPUT_COPY) == 1:
        function_call = function_call.strip(",)") + ")"
    exit(f"► Called: {function_call}\\n► Returned <{type(got).__name__}>:\\n{format_invis_chars(got)}\\n► Expected <{type(FUNCTION_EXPECTED).__name__}>:\\n{format_invis_chars(FUNCTION_EXPECTED)}")
'''
####################################################################
