import subprocess
import shutil
import os
import json
import sys
from difflib import unified_diff

docker_mode = "--docker" in sys.argv

FILE_PATH_PREFIX = "/home" if docker_mode else os.getcwd() + "/build/tests"
print(os.listdir("/home"))
if not docker_mode:
    try:
        shutil.rmtree("build/tests")
    except FileNotFoundError:
        pass

    shutil.copytree("tests", "build/tests")
    shutil.copy("pysafegradingfw.py", "build/tests/pysafegradingfw.py")


sp = subprocess.run(["python", "testbench-features.py", "--prod"],
                    cwd=FILE_PATH_PREFIX,
                    capture_output=True)

if "--debug" in sys.argv:
    print(sp.stdout.decode())
    print(sp.stderr.decode())


grader_object = json.loads(sp.stdout.decode())

fail_count = 0
possible_fail_count = 0
success_count = 0

for testcase in grader_object["testcases"]:
    testcase["name"] = testcase["name"].removeprefix("Disable DEBUG_MODE ")

    with open(FILE_PATH_PREFIX + f"/test_feedback/{testcase["name"]}.txt") as fp:
        expected_test_feedback = fp.read()
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

        elif testcase["feedback"] != expected_test_feedback:

            if testcase["feedback"].replace(FILE_PATH_PREFIX, "/home") != expected_test_feedback:
                print(f"⚠️ Possible Fail: {testcase["name"]}")
                print("  - Testcase 'feedback' does not match existing feedback. Verify if intentional and update test file.")

                possible_fail_count += 1
                diff = unified_diff(testcase["feedback"].splitlines(), expected_test_feedback.splitlines(), lineterm='')
                print('\n'.join(list(diff)))
            else:
                print(f"✅ Success: {testcase["name"]}")
                success_count += 1

        else:
            print(f"✅ Success: {testcase["name"]}")
            success_count += 1


print(f"\n{fail_count} Failing Tests, {possible_fail_count} Possibly Failing Tests, {success_count} Successful Tests")

if not docker_mode:
    try:
        shutil.rmtree("build/tests")
    except FileNotFoundError:
        pass
else:
    # Copy docker home folder to local directory for easy debugging
    try:
        shutil.rmtree("/output/home")
    except FileNotFoundError:
        pass
    shutil.copytree("/home","/output/home")



exit(fail_count)

