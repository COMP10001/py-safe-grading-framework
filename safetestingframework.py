# Safe Ed Assignment Unit Testing Framework V0.3.0 safetestingframework.py
# Depends on: runtestsubprocess.py
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
import unittest
import os
import subprocess
import pickle
import base64
import ast
import traceback

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

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

def verify_program_output(proc_ret, expected_stdout, expected_stderr):
    assert proc_ret.stderr == expected_stderr, f"Your program produced the following errors:\n{proc_ret.stderr}"
    assert proc_ret.stdout == expected_stdout, f"Your program produced the following output:\n{proc_ret.stdout}\n\nThe expected output is:\n{expected_stdout}"

####################################################################

def run_function_test(test_file=None, student_file_name=None, function_name=None, function_input=None, function_expected = None, 
        function_timeout_seconds = 1, check_mutate=False, expected_stdout="", expected_stderr="", non_allowed_nodes = (), 
        non_allowed_functions=(), non_allowed_imports = ("sys", "os", "subprocess", "signal"), required_nodes=()
    ):
    '''
    Test the return value, stdout, stderr of a student defined function. Includes the ability to check for mutated input. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''
    run_astcheck_test(student_file_name, test_file_path_prefix='/home/', 
                      non_allowed_nodes=non_allowed_nodes, 
                      non_allowed_functions=non_allowed_functions, 
                      non_allowed_imports=non_allowed_imports, 
                      required_nodes=required_nodes
                    )

    encode_obj_data(function_input, "subproc-func-input")
    encode_obj_data(function_expected, "subproc-func-expected")

    proc_ret = subprocess.run(
                        ("python", test_file, student_file_name, function_name, str(function_timeout_seconds), str(int(check_mutate))),
                        text=True,
                        capture_output=True,
                    )

    verify_program_output(proc_ret, expected_stdout, expected_stderr)
    
####################################################################

def run_script_test(student_file_name=None, student_file_path="/home/", timeout_seconds = 1, expected_stdout="", expected_stderr="", 
        non_allowed_nodes = (), non_allowed_functions=(), non_allowed_imports = ("sys", "os", "subprocess", "signal"), required_nodes=()
    ):
    '''
    Test the stdout, stderr of a student defined python script. 
    By default OS and other imports are blocked to mitigate attempts to bypass testing. Other nodes to check for via the 
    abstract syntax tree can be specified to check that students use or do not use certain python features.
    '''

    run_astcheck_test(student_file_name, test_file_path_prefix='/home/', 
                      non_allowed_nodes=non_allowed_nodes, 
                      non_allowed_functions=non_allowed_functions, 
                      non_allowed_imports=non_allowed_imports, 
                      required_nodes=required_nodes
                    )

    proc_ret = subprocess.run(
                            ("python", student_file_path + student_file_name),
                            text=True,
                            capture_output=True, 
                        )

    verify_program_output(proc_ret, expected_stdout, expected_stderr)

####################################################################

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'

def run_pep8_test(test_file=None, test_file_path_prefix = "/home/", ignored_tests=PEP8_IGNORED):
    '''
    Run PEP8 style checks on the student submission file.
    '''
    filename = test_file_path_prefix + test_file
    local_import_paths = recursive_find_local_import_paths(filename)
    files_to_check = [filename] + local_import_paths 
    
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

def cache_hidden_test_files(files):
    file_dict = {}
    for file in files:
        with open(file, 'r') as fp:
            file_dict[file] = fp.read()
        os.remove(file)
    return file_dict

class hidden_file_manager:
    def __init__(self, hidden_file_dict, files_to_reveal):
        self.hidden_file_dict = hidden_file_dict
        self.files_to_reveal = files_to_reveal
        for file in files_to_reveal:
            with open(file, 'w') as fp:
                fp.write(self.hidden_file_dict[file])
        
    def __enter__(self):
        pass
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.files_to_reveal:
            os.remove(file)
            
####################################################################

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
     
def find_imports(ast_tree):
    visitor = NodeTypeVisitor((ast.Import, ast.ImportFrom))
    visitor.visit(ast_tree)
    imports = []
    for node in visitor.nodes:
        for alias in node.names:
            imports.append(alias.name)
    return imports

def find_local_import_paths(filename):
    file_path_components = filename.rsplit('/',1)
    path_prefix = ""
    if (len(file_path_components) > 1):
        path_prefix = file_path_components[0] + "/"
        
    tree = create_ast_object(filename)
    imports = find_imports(tree)
    local_import_paths = []
    for imported in imports:
        path = imported.split('.')
        path = path_prefix + "/".join(path) + ".py"
        if os.path.isfile(path):
            local_import_paths.append(path)
    
    return local_import_paths

def recursive_find_local_import_paths(filename):
    local_imports = find_local_import_paths(filename)
    files_checked = [filename]
   
    while (len(local_imports) > 0):
       next_import = local_imports.pop()
       if next_import not in files_checked:
           files_checked.append(next_import)
           local_imports += find_local_import_paths(next_import)
    return files_checked
            

def run_astcheck_test(test_file=None, test_file_path_prefix="/home/", non_allowed_nodes = (), non_allowed_functions=(), non_allowed_imports = (), required_nodes=()):
    # Parse program.py.
    filename = test_file_path_prefix + test_file
    local_import_paths = recursive_find_local_import_paths(filename)
    files_to_check = [filename] + local_import_paths 

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

        student_imports = find_imports(tree)
        for lib in student_imports:
            if lib in non_allowed_imports:
                assert False, f'Your program is not allowed to import {lib}. Occured in file {student_file}.'
                

def hidden(release_test_cases: bool):
    hidden = '#hidden ' if release_test_cases == False else ''
    def dec(obj):
        obj.__doc__ = obj.__doc__ + hidden
        return obj
    return dec

def private(release_test_cases: bool):
    private = '#private ' if release_test_cases == False else ''
    def dec(obj):
        obj.__doc__ = obj.__doc__ + private
        return obj
    return dec

def score(score):
    def dec(obj):
        obj.__doc__ = obj.__doc__ + f"#score({score})"
        return obj
    return dec


####################################################################

RUN_TEST_SUBPROCESS = \
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

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
FUNCTION_TIMEOUT_SECONDS = int(sys.argv[3])
FUNCTION_CHECK_MUTATE = bool(int(sys.argv[4]))
FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_EXPECTED = decode_obj_data("subproc-func-expected")

TIMEOUT_SUFFIX = "" if FUNCTION_TIMEOUT_SECONDS == 1 else "s"
FUNCTION_INPUT_COPY = copy.deepcopy(FUNCTION_INPUT)

os.remove("subproc-func-input")
os.remove("subproc-func-expected")

####################################################################

# Try import function from student code
try:
    exec("from %s import %s" % (STUDENT_FILE_NAME.removesuffix(".py"), FUNCTION_NAME))
except:
    exit(traceback.format_exc(limit=-1))

####################################################################

def handle_timeout(signum, frame):
        raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

####################################################################
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

####################################################################

# Check for mutated input if desired.
if FUNCTION_CHECK_MUTATE and FUNCTION_INPUT != FUNCTION_INPUT_COPY:
    exit("Your code should not mutate the function input!")
        
if got != FUNCTION_EXPECTED:
    function_call = f"{FUNCTION_NAME}{FUNCTION_INPUT}"
    if len(FUNCTION_INPUT == 1):
        function_call = f"{FUNCTION_NAME}({FUNCTION_INPUT[0]})"
    exit(f"Called: {function_call}
'''



####################################################################
        
