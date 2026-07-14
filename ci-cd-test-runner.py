import subprocess
import shutil
import os
import json
try:
    shutil.rmtree("build/tests")
except FileNotFoundError:
    pass

shutil.copytree("tests", "build/tests")
shutil.copy("pysafegradingfw.py", "build/tests/pysafegradingfw.py")
sp = subprocess.run(["python", "testbench-features.py", "--prod"],
                    cwd=os.getcwd()+"/build/tests/",
                    capture_output=True)

grader_object = json.loads(sp.stdout.decode())

fail_count = 0
success_count = 0

for testcase in grader_object["testcases"]:
    if not (("Pass" in testcase["name"] and "Fail" not in testcase["name"])
         or ("Fail" in testcase["name"] and "Pass" not in testcase["name"])):
        print(f"❌ Fail: {testcase["name"]}")
        print("  - Testcase name needs to contain 'Pass' or 'Fail' for CI/CD validation")
        print(f"  - {testcase}")
        fail_count += 1
    elif (("Pass" in testcase["name"]) != bool(testcase["passed"])):
        print(f"❌ Fail: {testcase["name"]}")
        print("  - Testcase 'passed' parameter does not match expected value based on name.")
        print(f"  - {testcase}")
        fail_count += 1
    else:
        print(f"✅ Success: {testcase["name"]}")
        success_count += 1

print(f"\n{fail_count} Failing Tests, {success_count} Successful Tests")

try:
    shutil.rmtree("build/tests")
except FileNotFoundError:
    pass

exit(fail_count)

