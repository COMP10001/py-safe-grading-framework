import re

line = 'name = "MY_TEXT_HERE",'
with open("tests/testbench-features.py") as fp:
    testfile = fp.read()
new_testfile = re.sub(
    r' (name\s*=\s*")([^"]*)(")', 
    lambda m: m.group(1) + m.group(2).replace('_', ' ') + m.group(3), 
    testfile
)

with open("newtestbench-features.py", "w") as fp:
    fp.write( new_testfile)
