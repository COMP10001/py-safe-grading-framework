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

# Try import function from student code
try:
    exec("from %s import %s" % (STUDENT_FILE_NAME.removesuffix(".py"), FUNCTION_NAME))
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
        
if got != FUNCTION_EXPECTED:
    function_call = f"{FUNCTION_NAME}{FUNCTION_INPUT}"
    if len(FUNCTION_INPUT == 1):
        function_call = f"{FUNCTION_NAME}({FUNCTION_INPUT[0]})"
    exit("Called: {function_call}\\n\\nGot: {got}\\nType: {type(got).__name__}\\n\\nExpected: {FUNCTION_EXPECTED}\\nType: {type(FUNCTION_EXPECTED).__name__}")