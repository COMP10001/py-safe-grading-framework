# Safe Ed Assignment Unit Testing Framework V0.3.0 safetestingframework.py 
# Last Updated: 2025/06/03
# Author: Kacie Beckett <kacie.beckett@unimelb.edu.au> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20912/lessons/79913/slides/539891

# Note: be careful if developing locally, as importing this code will cause it to be 
# irreplaceably removed, unlike on Ed.

import unittest
import os
import subprocess
import pickle
import ast
import traceback

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
DEFAULT_STUDENT_FILE_PATH_PREFIX = os.getcwd() + '/'
DEFAULT_NON_ALLOWED_IMPORTS = ("sys", "os", "subprocess", "signal")
####################################################################

def run_function_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        function_name=None,                                          # Function to test
        function_input=(),                                           # Input to function, must be wrapped in a tuple
        function_expected = None,                                    # Expected value for function
        function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
        check_mutate=False,                                          # Check if the function input was mutated
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
        non_allowed_functions=(),                                    # Function names of any specific functions to disallow
        non_allowed_imports = DEFAULT_NON_ALLOWED_IMPORTS,           # Imports that are not allowed anywhere in student file or any local imports
        required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
        files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
        hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
    ):
    '''
    Test the return value, stdout, stderr of a student defined function. Includes the ability to check for mutated input. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    run_astcheck_test(student_file_name,
                      student_file_path_prefix=student_file_path_prefix,
                      non_allowed_nodes=non_allowed_nodes, 
                      non_allowed_functions=non_allowed_functions, 
                      non_allowed_imports=non_allowed_imports, 
                      required_nodes=required_nodes
                    )

    encode_obj_data(function_input, "subproc-func-input")
    encode_obj_data(function_expected, "subproc-func-expected")
    
    with open(RUN_TEST_SUBPROCESS_FILENAME, "w") as fp:
        fp.write(RUN_TEST_SUBPROCESS_FILE)
        
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret = subprocess.run(
                            ("python", RUN_TEST_SUBPROCESS_FILENAME, student_file_name, function_name, str(function_timeout_seconds), str(int(check_mutate))),
                            capture_output=True,
                        )

    verify_program_output(proc_ret, expected_stdout, expected_stderr)
    
####################################################################

def run_script_test(
        student_file_name=None,                                      # File to test function from
        student_file_path_prefix=DEFAULT_STUDENT_FILE_PATH_PREFIX,   # File path prefix
        expected_stdout="",                                          # Expected value in stdout
        expected_stderr="",                                          # Expected value in stderr
        non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
        non_allowed_functions=(),                                    # Function names of any specific functions to disallow
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

    run_astcheck_test(student_file_name,
                      student_file_path_prefix=student_file_path_prefix,
                      non_allowed_nodes=non_allowed_nodes, 
                      non_allowed_functions=non_allowed_functions, 
                      non_allowed_imports=non_allowed_imports, 
                      required_nodes=required_nodes
                    )
    
    with HiddenFileManager(hidden_file_dict, files_to_reveal):
        proc_ret = subprocess.run(
                                ("python", student_file_path_prefix + student_file_name),
                                capture_output=True, 
                            )

    verify_program_output(proc_ret, expected_stdout, expected_stderr)

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
    local_import_paths = recursive_find_local_import_paths(filepath)
    files_to_check = [filepath] + local_import_paths 
    
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
                                    
    assert pep8_violations == "", "The following style errors were found:\n" + pep8_violations

            
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
    local_import_paths = recursive_find_local_import_paths(filepath)
    files_to_check = [filepath] + local_import_paths 

    for student_file in files_to_check:
        tree = create_ast_object(student_file)

        # Run the AST node type visitor over the tree to search for forbidden nodes.
        visitor = NodeTypeVisitor(non_allowed_nodes)
        visitor.visit(tree)
        if visitor.nodes:
            node = visitor.nodes[0]
            assert False, 'Your program is not allowed to use a {}. This occurred on line {} of {}.'.format(type(node).__name__, node.lineno, student_file)

        # Run the AST node type visitor over the tree to search for specific functions
        visitor = NodeTypeVisitor((ast.Name,))
        visitor.visit(tree)
        for node in required_nodes:
            if node.id not in visitor.nodes:
                assert False, f'Your program must include {node.id}.'

        for node in visitor.nodes:
            if node.id in non_allowed_functions:
                assert False, 'Your program is not allowed to use the {} function. This occurred on line {} of {}.'.format(node.id, node.lineno, student_file)

        student_imports = find_imports(student_file)
        for lib in student_imports:
            if lib in non_allowed_imports:
                assert False, f'Your program is not allowed to import {lib}. Occured in file {student_file}.'

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
        obj.__doc__ = obj.__doc__ + f"#name({name.strip('test').strip('_').replace('_',' ')})"
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


def verify_program_output(proc_ret, expected_stdout, expected_stderr):
    ''' 
    Produce the errors displayed to students when a test fails. In a unit test
    assert is used to say the test failed, before moving onto the next.
    '''
    errors = ""
    if proc_ret.stderr.decode() != expected_stderr:
        if expected_stderr == "":
            errors += "\n► Your program produced the following errors:\n{0}" \
            .format(proc_ret.stderr.decode())
        else:
            errors +="\n► Your program produced the following errors:\n{0}\n► The expected errors are:{1}" \
                .format(proc_ret.stderr.decode(), expected_stderr)
            
    if proc_ret.stdout.decode() != expected_stdout: 
        if expected_stdout == "":
            errors += "\n► Your program printed the following output when no printing was expected:\n{0}" \
            .format(format_invis_chars(proc_ret.stdout.decode()), format_invis_chars(expected_stdout))
        else:
            errors += "\n► Your program printed the following output:\n{0}\n► The expected printed output is:\n{1}" \
            .format(format_invis_chars(proc_ret.stdout.decode()), format_invis_chars(expected_stdout))
        
    if errors != "":
        raise Exception(errors)
        
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
# The runtestsubprocess file must be removed from path before running student code, so it is convient to store it directly
# in here, to avoid version control inconvenience.

# Note: All occurances of \ need to be escaped as \\
RUN_TEST_SUBPROCESS_FILENAME = "runtestsubprocess.py"
RUN_TEST_SUBPROCESS_FILE = \
'''
import sys
import pickle
import os
import ast
import signal
import traceback
import copy

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

# Object data is encoded and decoded to be passed in python object format
# between processes
def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return pickle.load(f)

STUDENT_FILE_PATH = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
FUNCTION_TIMEOUT_SECONDS = int(sys.argv[3])
FUNCTION_CHECK_MUTATE = bool(int(sys.argv[4]))
FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_EXPECTED = decode_obj_data("subproc-func-expected")

TIMEOUT_SUFFIX = "" if FUNCTION_TIMEOUT_SECONDS == 1 else "s"
FUNCTION_INPUT_COPY = copy.deepcopy(FUNCTION_INPUT)

os.remove("subproc-func-input")
os.remove("subproc-func-expected")

# Try import function from student code
try:
    exec("from %s import %s" % (STUDENT_FILE_PATH.removesuffix(".py"), FUNCTION_NAME))
except:
    exit(traceback.format_exc(limit=-1))

def handle_timeout(signum, frame):
        raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

# Run the function and check for timeout and mutating input 
try: 
    got = globals()[FUNCTION_NAME](*FUNCTION_INPUT)
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

def format_invis_chars(data):
    if type(data) == str:
        # This forces it to show characters as being escaped and wrapped in quotation marks for consistency
        return str((data,))[1:-2]
    return str(data)
  
if got != FUNCTION_EXPECTED:
    function_call = f"{FUNCTION_NAME}{FUNCTION_INPUT}"
    if len(FUNCTION_INPUT) == 1:
        function_call = function_call.strip(",)") + ")"
    exit(f"► Called: {function_call}\\n► Returned <{type(got).__name__}>:\\n{format_invis_chars(got)}\\n► Expected <{type(FUNCTION_EXPECTED).__name__}>:\\n{format_invis_chars(FUNCTION_EXPECTED)}")
'''

####################################################################
