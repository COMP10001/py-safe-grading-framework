import os
import signal
import traceback
import builtins
from builtins import input

# Remove the test file after loading, to prevent ability to print out contents
os.remove(__file__)

FUNCTION_TIMEOUT_SECONDS = {0}
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

builtins.input = input_with_echoing


def handle_timeout(signum, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(FUNCTION_TIMEOUT_SECONDS)  # seconds

try: 
    import {1}
except TimeoutError:
    exit(f"Your program took too long to run and was terminated after {FUNCTION_TIMEOUT_SECONDS} second{TIMEOUT_SUFFIX}. Do you have an infinite loop?")
except Exception:
    # Print the exception excluding information about this file path
    exit(traceback.format_exc(limit=-1)) 
finally:
    signal.alarm(0)