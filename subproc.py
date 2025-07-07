# RUN_TEST_SUBPROCESS_FILE = \
# '''
import sys
import pickle
import os
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
INPUT_ECHOING = bool(int(sys.argv[5]))

FUNCTION_INPUT = decode_obj_data("subproc-func-input")
FUNCTION_EXPECTED = decode_obj_data("subproc-func-expected")
TIMEOUT_SUFFIX = "" if FUNCTION_TIMEOUT_SECONDS == 1 else "s"
FUNCTION_INPUT_COPY = copy.deepcopy(FUNCTION_INPUT)

os.remove("subproc-func-input")
os.remove("subproc-func-expected")

def handle_timeout(signum, frame):
        raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

# Try import function from student code
# Run the function and check for timeout and mutating input 

def input_with_echoing(prompt):
    try:
        out = input(prompt)
        print(out) # echo the input to stdout
    except Exception:
        stack = "Traceback (most recent call last):\\n" 
        stack += "".join(traceback.format_stack(limit=2)[:1])
        exit(stack+traceback.format_exc(limit=0)) 
    return out

try: 
    exec("import %s" % (STUDENT_FILE_NAME.removesuffix(".py"),))
    if INPUT_ECHOING == True:
        # patch the input function to echo the input to stdout
        exec("%s.input = input_with_echoing" % (STUDENT_FILE_NAME.removesuffix(".py"),))

    exec("student_function = %s.%s" % (STUDENT_FILE_NAME.removesuffix(".py"),FUNCTION_NAME))
    got = student_function(*FUNCTION_INPUT)

    # exec("from %s import %s" % (STUDENT_FILE_NAME.removesuffix(".py"), FUNCTION_NAME))
    # got = globals()[FUNCTION_NAME](*FUNCTION_INPUT)
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
    function_call = f"{FUNCTION_NAME}{FUNCTION_INPUT_COPY}"
    if len(FUNCTION_INPUT_COPY) == 1:
        function_call = function_call.strip(",)") + ")"
    exit(f"► Called: {function_call}\\n► Returned <{type(got).__name__}>:\\n{format_invis_chars(got)}\\n► Expected <{type(FUNCTION_EXPECTED).__name__}>:\\n{format_invis_chars(FUNCTION_EXPECTED)}")
'''