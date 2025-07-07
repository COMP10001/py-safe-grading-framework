import pty
import subprocess
import os
import tty
import termios
import sys
import time


host_fd, client_fd = pty.openpty()
input_data = "a\nb\nb\n"
command = ("python", "program.py")
output = ""
with subprocess.Popen(command, stdin=client_fd, stdout=client_fd, stderr=client_fd) as process:
    os.close(client_fd) # Only used to create subprocess
    for line in input_data.splitlines(keepends=True):
        output += os.read(host_fd, 1024).decode()
        os.write(host_fd, line.encode())
        time.sleep(0.1)
    output += os.read(host_fd, 1024).decode()
print(output)
