# Note
See COMP10001 Worksheet Repository on Ed for runnable tests/examples etc
https://edstem.org/au/courses/20911/lessons/79913/slides/539891

# Usage Instructions (Reproduced from Ed at moment)
- Add the Run command using the same file name as in the Scaffold section, so that students can test their code without using the terminal. (e.g.) python task1.py or program.py

<p align="center">
  <img src="docs/images/run-command.png" />
</p>

- Choose "Custom" Test Method
- Add the Mark Command as python testbench.py or whatever the test file

<p align="center">
  <img src="docs/images/mark-command.png" width=60% />
</p>

- Ensure your Time Limit(s)is set to 300 (the maximum) or high enough relative to the timeout set within each test
- Check the Per-testcase Scores box
- Scroll down to advanced settings and enable Display Files by checking the box. This means the "test report" test cases can generate a txt file transcript of the complete program execution and a seperate file describing what each test is checking, aswell as show the expected output files if any.
- Copy the file safetestingframework.py into testing environment (see the "Releases" page for the most up-to date version, or copy it from below if the version number matches the most recent release)
- Create a testbench.py with relevant tests for the task.
    - See "Testbench Template Generator" page to minimise manual copy pasting effort.

<p align="center">
  <img src="docs/images/test-page-ed.png" />
</p>

# Notes:
- Hidden Tests show pass or fail, but not the input or output
- Private Tests do not show pass or fail, or the input and output
- Students cannot see the name of a hidden tests
- The tests will display to staff showing the name followed by (hidden) or (private) when set respectively
- The tests will display in the order they are defined in the test case file

### `testbench-minimal.py`
- This is the file you should write your tests into.

- See Testbench Template Generator slide, to help with setting up tests, and the feature tests slide / feature testbench for examples that are setup.

### `safetestingframework.py`
- This file can be reproduced exactly, unless fixes or changes are needed.


# Release History

### Known Unfixed Bugs/Todo:
- Add option to pass when only differing by line ending \r\n or \n
- Add ability to pass multiple options of output as correct

### V0.4.6 Kacie Beckett (09-10-2025)
- Extend printing protection to the entire execution of test bench, not just custom verification function (IE prints redirected to devnull)
- Exception checking now only compares name and message eg for ValueError('ABC') it checks 'ValueError' and 'ABC' match the expected exception to allow for custom exceptions where they are defined in different files (eg student code/ and in testbench).
- Fix crashing when student returns an object that cannot be pickled, by passing back the type(val) and str(val) to test framework to display error check message. Add error message for having an expected return that is not testable (cannot be pickled).

### V0.4.5 Kacie Beckett (21-08-2025)
- Fix missing fstring for astcheck parsing error message. Hide path when code has a syntax error so it looks like the message when running directly with python interpretter.

### V0.4.4 Kacie Beckett (05-08-2025)
- Move the stdout redirection to devnull for custom verification function from needing to be added to testbench, so it wraps the call, to prevent any code run inside a verification function from crashing the testbench, or not resetting the stdout to the original one.
- Catch all exceptions not just timeout error from the custom verification function, to prevent this from crashing testbench.

### V0.4.3 Kacie Beckett (28-07-2025)
- Bug fix function expected mutated args.
- Bug fix expected method_calls
- Bug fix hidden files not being restored after all test running, so they can be viewed as display files
- Bug fix expected exception message

### V0.4.2 Kacie Beckett (28-07-2025)
- Add custom_verification_data as option for function and script tests.
- Add function_expected_recursive_calls and related feedback message, so a function test will only pass if it produced the correct number of recursive calls, or if any of the student defined functions called within this function, have the correct number of recursive calls.
- Bug fix ast recursive file checking
- Bug fix ast check node visitor skipping function body

### V0.4.1 Kacie Beckett (28-07-2025)
- Add custom_verification_function , custom_verification_timeout , custom_verification_timeout_msg as options for function and script tests, so that a custom function to act on the test_data object can be passed in, and can set feedback a feedback message while having other tests. Used for patching in timely return testing etc in Ed Worksheets, and other one off testing code that doesn't need to be in the library.

### V0.4.0 Kacie Beckett (24-07-2025)
- Change test setup interface to use a custom SafeTesting class with methods, as no longer need to have a unittest subclass due of switching to a custom grader.
- Add expected mutated argument checking for run_function_test
- Add expected exception checking for run_function_test and run_script_test
- Add non_allowed_methods, required_methods, required_functions , required_imports options to ast check.
- Encapsulate ast checking under a class
- Encapsulate test data in a test data class, to make it easier to pass between functions
- Add a data classes following the forward of Ed's Custom Grader output json for nice interface for creating the output object
- Rewrite ast checking to only search callable nodes for functions/methods. Correctly label module functions as functions and not methods.
- Move all feedback message outputting to be handled in the main library file, and not in the sub processes so that handling of the feedback messages can be modified without touching that logic.
- Rewrite verify_program_output and related functions to no longer be what handles feedback length truncation.
- Feedback length is now truncated after all tests are run, with an iterative reduction of level of specificity, eventually terminating with empty feedback strings to guarantee that as long as all the tests can pass when setting up, the output json object will never be oversized and cause failure because of Ed's maximum stdout limit. This is an improvement on the previous system as as much feedback as possible will be shown within the limits.
- *For the sake of file size, there is maximum output limits set by a constant, well above what would be necessary just in case.
- Added a visible test report and execution transcript to show what each test is checking, and also the full test feedback that would be outputted if the output limit is not reached, in case not all of it is shown.
- Add a private test report and execution transcript for the hidden and private test cases, for testing/marking purposes.
- Move output message strings to be constants
- Show expected output files if they are available, using undocumented "output_files" json optional argument for test cases. *Requires display files option to be enabled under advanced settings tab
- Rename function_input to function_args
- Rename debug_output to setup_mode , which now also changes input, expected stdout/stderr to be formatted as a string for easy copy pasting into testbench. In setup mode, all tests fail to prevent accidentally leaving it enabled. Removed debug output testcase, in favour of the test report testcase.
- UI fix: replace("\\'", "'") in formatted input, expected stdout/stderr as this is not used as assignable python string.
- Change default sequence type to lists in test function arguments to prevent cases of missing comma for single element tuple
- Add pydantic validate_call type checking on all register test api methods
- Add type hinting to most functions

### V0.3.1 Kacie Beckett (2025-07-10)
- Bug fix hidden file manager to use read and write as bytes instead of utf8
- rename function/script input argument to input_data

### V0.3.0 Kacie Beckett (2025-07-10)
- Switch to using custom grader instead of PyUnit to bypass some limitations of Ed Implementation
- Hide the stacktrace previously shown by Ed's PyUnit Parser in favor of custom output message
- Testbench containing all the tests no longer exists in __pycache__ as it is not loaded by Edstem's ed-test-runner.py for extra security
- Added the ability to hide and reveal extra files such as txt, csv, etc files to use a test data, as needed, for a given test to avoid ability to print out contents, for run_function_test and run_script_test
- Improved AST checking for non allowed elements to run on all local import files and add run_astcheck_test function to avoid having seperate implementations of the same thing.
- Integrate run_astcheck_tst into interface for run_function_test and run_script_test
- Add input_echoing  boolean to run_function_test and run_script_test  so input from file mimics interactive user input
- Improved run_pep8_test to consider all local imports not just the test file
- Merged function runtestsubprocess.py into the safetestingframework.py file  as a string for easier version control
- Add script runtestsubprocess file, to allow for patching in input_echoing function
- Create, load, and then remove runtestsubprocess.py  before running student code to avoid ability to print out the contents
- Added check_mutate flag to run_function_test to check if the input was mutated
- Add ability to set an expected_stdout, expected_stderr
- Add rudimentary expected_file checking, to see if a given file exists and if it is an exact match for a given test file.
- Added @setname(), @hidden(), @private(), @score() decorator functions to abstract the Ed Stem integration.
- Added more non allowed default imports to disallow certain system functions
- Added Testbench Template Generator
- Improved Testbench example
- Added more inline documentation of the code
- Improve function output printing message to print strings exactly as required to write in python eg 'abc\n'
- Improve stdout printing message to show escaped characters like newlines, while also wrapping the lines
- Add ~60 Feature tests to verify functionality
- Add private debug output test case
- Bug fix line ending conversion due to the text=True argument for subprocess.run() instead of leaving it as a byte sequence and using decode() later
- Bug fix student code printing too much output being able to crash the testing code by running out memory by truncating  bypassing bad implementation by Ed.
- Having more test cases decreases the amount each test case can print before being truncated, and the amount is visible in the debug test case
- Bug fix file to test eg student-code.py having dashes in it causing import to fail by switching to importlib
- Switch timeout to happen inside the safetestingframework.py code instead of the runtest subprocess, to allow better output messages

### V0.2.0 - Kacie Beckett (2025-05-01)
- Initial relatively feature complete release
- Todo: add a mutability check boolean for use within test bench to avoid needing seperate mutability check runtestsubprocess file
- Todo: Consider loading testsubprocess.py content into python object, running the subprocess which removes the file from OS, and then rewriting the file back to OS after it finishes, so contents cannot be read by students.
- Small patches from being used on 2 assignments, such as ability to check mutability and output type format as int instead of <class 'int'>

### V0.1.x - Kacie Beckett (2025-04-01)
- Initial main development of framework