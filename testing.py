import json
import re
####################################################################

def get_testcase_dict(function_name, docstring):
    score_pattern = r"#score\((\d*\.?\d+)\)"
    name_pattern = r"#name\(((?:[^()\\]|\\.)*)\)"

    try:
        score = re.findall(score_pattern, docstring)[0]
        if '.' in score:
            score = float(score)
        else:
            score = int(score)
    except:
        score = 0

    try:
        matches = re.findall(name_pattern, docstring)[0]
        name = "".join([re.sub(r'\\([()])', r'\1', match) for match in matches])
    except:
        name = function_name
        
    private = True if "#private" in docstring else False
    hidden = True if "#hidden" in docstring and private == False else False
    testcase = {}
    testcase["name"] = name
    testcase["score"] = score
    testcase["ok"] = True
    testcase["passed"] = True
    testcase["hidden"] = hidden
    testcase["private"] = private

    return testcase

def run_tests(SafeTesting):
    test_list = [func for func in dir(SafeTesting) if callable(getattr(SafeTesting, func)) and func.startswith("test")]
    testbench = SafeTesting()
    testcase_output = []
    grader_output = {}
    grader_output["testcases"] = testcase_output
    for test in test_list:
        test_method = getattr(testbench, test)
        testcase = get_testcase_dict(test_method.__name__, test_method.__doc__)
        try:
            test_method()
        except Exception as e:
            testcase["feedback"] = str(e)
            testcase["passed"] = False
        testcase_output.append(testcase)
    print(json.dumps(grader_output))