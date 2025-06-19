# Safe Ed Assignment Unit Testing Framework V0.2.0 safetestingframework.py
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

# Remove the test file after loading by Ed, to prevent ability to print out contents
os.remove(__file__)

def encode_obj_data(input_data, filename):
    with open(filename,"wb") as f:
        pickle.dump(input_data, f)

def decode_obj_data(filename):
    with open(filename,"rb") as f:
        data = pickle.load(f)
    return data

def run_test(test_file=None, student_file_name=None, function_name=None, function_input=None, function_expected = None, 
            function_timeout_seconds = 1, expected_stdout="", expected_stderr=""):

    encode_obj_data(function_input, "subproc-func-input")
    encode_obj_data(function_expected, "subproc-func-expected")

    proc_ret =  subprocess.run(
                        ("python", test_file, student_file_name, function_name, str(function_timeout_seconds)),
                        text=True,
                        capture_output=True,
                    )

    assert proc_ret.stderr == expected_stderr, f"Your program produced the following errors:\n{proc_ret.stderr}"
    assert proc_ret.stdout == expected_stdout, f"Your program produced the following output:\n{proc_ret.stdout}\n\nThe expected output is:\n{expected_stdout}"

def run_test_as_script(test_file=None, test_file_path="/home/", timeout_seconds = 1, expected_stdout="", expected_stderr=""):
    proc_ret =  subprocess.run(
                            ("python", test_file_path+test_file),
                            text=True,
                            capture_output=True,
                        )

    assert proc_ret.stderr == expected_stderr, f"Your program produced the following errors:\n{proc_ret.stderr}"
    assert proc_ret.stdout == expected_stdout, f"Your program produced the following output:\n{proc_ret.stdout}\n\nThe expected output is:\n{expected_stdout}"

def format_file_path(stdout):
    return stdout.replace('/home/', '')

def run_test_pep8(test_file=None):
    proc_ret = subprocess.run(
                        ('flake8',
                         '--jobs=1',
                         '--ignore=E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503',
                         '/home/'+test_file),
                        stdout=subprocess.PIPE,
                        text=True
                    )
    output = format_file_path(proc_ret.stdout)
    assert proc_ret.returncode == 0, f'{output}'

# The AST Checking code is adapted from the testing infrastructure written for grok
class NodeTypeVisitor(ast.NodeVisitor):
    def __init__(self, types, *args, **kwargs):
        self.types = tuple(types)
        self.nodes = []

    def visit(self, node):
        if isinstance(node, self.types):
            self.nodes.append(node)
        super().visit(node)


def run_test_astcheck(test_file=None, test_file_path="/home/", non_allowed_nodes = (), non_allowed_functions=(), required_nodes=()):
    # Parse program.py.
    filename = test_file_path + test_file
    with open(filename) as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename)
    except:
        assert False, traceback.format_exc(limit=-1)

    # Run the AST node type visitor over the tree to search for forbidden nodes.
    visitor = NodeTypeVisitor(non_allowed_nodes)
    visitor.visit(tree)
    if visitor.nodes:
        node = visitor.nodes[0]
        assert False, 'Your program is not allowed to use a {}. This occurred on line {} of {}.'.format(type(node).__name__, node.lineno, test_file)


    # Run the AST node type visitor over the tree to search for specific functions
    visitor = NodeTypeVisitor((ast.Name,))
    visitor.visit(tree)
    for node in visitor.nodes:
        if node.id in non_allowed_functions:
            assert False, 'Your program is not allowed to use the {} function. This occurred on line {} of {}.'.format(node.id, node.lineno, test_file)
    
