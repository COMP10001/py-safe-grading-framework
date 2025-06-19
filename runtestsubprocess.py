# Safe Ed Assignment Unit Testing Framework V0.2.0 runtestsubprocess.py
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891

# Note that this file is not removed immediately after loading so the contents should 
# not contain any information related to the test cases to avoid data leakage
import sys
import pickle
import os 
import ast
import signal
import traceback
import copy

# Object data is encoded and decoded to be passed in python object format 
# between processes
def decode_obj_data(filename):
    with open(filename,"rb") as f:
        return pickle.load(f)

STUDENT_FILE_NAME = sys.argv[1]
FUNCTION_NAME = sys.argv[2]
FUNCTION_TIMEOUT = int(sys.argv[3])
FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_EXPECTED = decode_obj_data("subproc-func-expected")

os.remove("subproc-func-input")
os.remove("subproc-func-expected")


####################################################################
#  Check for non allowed functions and features using AST Checker  #
####################################################################

class NodeTypeVisitor(ast.NodeVisitor):
    def __init__(self, types, *args, **kwargs):
        self.types = tuple(types)
        self.nodes = []

    def visit(self, node):
        if isinstance(node, self.types):
            self.nodes.append(node)
        super().visit(node)

# Parse input python file
filename = '/home/' + STUDENT_FILE_NAME 
with open(filename) as f:
    source = f.read()
try:
    tree = ast.parse(source, filename)
except:
    exit(traceback.format_exc(limit=-1))


# Run the AST node type visitor over the tree to search for uses of exec, eval, and exit
# Or other non allowed functions/features that may allow for breaking the testing environment
visitor = NodeTypeVisitor((ast.Name,))
visitor.visit(tree)
for node in visitor.nodes:
    if node.id in ('eval', 'exec', 'exit'):
        exit('Your program is not allowed to use the {} function. This occurred on line {} of {}.'.format(node.id, node.lineno, filename))

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
signal.alarm(FUNCTION_TIMEOUT)  # seconds

####################################################################
# Run the function and check for timeout and mutating input 
TIMEOUT_SUFFIX = '' if FUNCTION_TIMEOUT == 1 else 's'
FUNCTION_INPUT_COPY = copy.deepcopy(FUNCTION_INPUT)
try: 
    got = globals()[FUNCTION_NAME](*FUNCTION_INPUT)
except TimeoutError:
    exit(f"Your program took too long to run and was terminated after {FUNCTION_TIMEOUT} second{TIMEOUT_SUFFIX}. Do you have an infinite loop?")
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1)) 
finally:
    signal.alarm(0)

####################################################################

# Check for mutated input if desired.
# if FUNCTION_INPUT[XYZ] != FUNCTION_INPUT_COPY[XYZ]:
#             exit("Your code should not mutate the function input!")
        
if got != FUNCTION_EXPECTED:
    exit(f"Called: {FUNCTION_NAME}{FUNCTION_INPUT}\n\nGot: {got}\nType: {type(got).__name__}\n\nExpected: {FUNCTION_EXPECTED}\nType: {type(FUNCTION_EXPECTED).__name__}")

