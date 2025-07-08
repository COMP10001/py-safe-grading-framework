import io
import selectors
import subprocess
import sys
import os
import io
import selectors    
def _subprocess_run_with_truncated_stdout(command, input_data, max_output_size, truncation_message):
    proc_stdout = ""
    proc_stderr = ""
    
    try:
        try:
            stdout_fp = open("stdout.txt", "w") 
            stderr_fp = open("stderr.txt", "w")
            proc_ret = subprocess.run(command, stdout=stdout_fp, stderr=stderr_fp, input=input_data)
            stdout_fp.close()
            
        except OSError:
            # If too much output is generated there will be no more space on device
            stdout_fp = open("stdout.txt", "a")
            stdout_fp.truncate(max_output_size - len(truncation_message))
            stdout_fp.close()
            proc_stdout += truncation_message
        
        stdout_fp = open("stdout.txt", "r") 
        proc_stdout = stdout_fp.read() + proc_stdout
        stdout_fp.close()
        os.remove("stdout.txt")
        
        stderr_fp.close()
    except OSError:
            # If too much output is generated there will be no more space on device
            stderr_fp = open("stderr.txt", "a")
            stderr_fp.truncate(max_output_size - len(truncation_message))
            stderr_fp.close()
            proc_stderr += truncation_message
    
    stderr_fp = open("stderr.txt", "r") 
    proc_stdout = stderr_fp.read() + proc_stderr
    stderr_fp.close()
    os.remove("stderr.txt")
    
    return proc_ret, proc_stdout, proc_stderr

command = ("python", "printspam.py")

print(_subprocess_run_with_truncated_stdout(command,"".encode(), 1000, "\nTruncated"))