Overview
=======================================
**NOTE**: This documentation is a work in progress.

Testing infrastructure for safely testing student code, with easy access to testing specific functions,
entire script files, performing AST checks, and style checks. Output feedback clearly specifies, what
function return types should be, if they should or should not print output etc, with output and stderr formatting
showing hidden chars such as newlines while also preserving line wrapping to make it easier for students to understand
why their output differs.

Configured for use with Edstem, but could be extended to work with other platforms with minimal effort.

Developed primarily for COMP10001 at the University of Melbourne, but has also been used for other subjects.
The primary goal of this project is to make it as easy as possible to setup whatever test is required for an assignment.
The existing tooling inside Edstem, and with test libraries such as PyUnit are not suitable.

Issues that this project solves:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If a student crashes the testing infrastructure code they get 0, even if they passed preceeding test cases
    - Every test is run as a seperate subprocess with a time limit, so the tests are independant, and cannot
      influence the main process unless there is a bug which needs to be patched.
- Using input output tests, does not allow for particularly descriptive outputs or type checking
    - Can directly test python objects for types etc
- Custom checks are time consuming to setup
    - A comprehensive set of features are provided




Recommended Steps:
~~~~~~~~~~~~~~~~~~
- First write your sample solution
- To use this grading framework, you will need to create one file which specifies all the tests which you need to run.
  To make it easy, you can run the script linked on :doc:`testbench-gen`, which will create a template for you to fill in the blanks
- You then need to specify the expected outputs etc for each test case, whether the test is visible, hidden or private,
  and how many points are attached to it.
- Download `pysafegradingfw.py <https://github.com/COMP10001/py-safe-grading-framework/blob/main/pysafegradingfw.py>`_ to your local directory, or Ed test file directory.
- To run it locally you can use ``python testbench.py --local-dev``, which ensures your testbench file will not be deleted.
  For safety you will probably want to develop this inside Ed, as then you can't accidentally delete your work.
  I do not recommend removing the file delete portion of the testbench file as if you forget to add it back, students could access all the testcases.
- If you need to check expected stdout as part of your test, I recommend enabling `format_test_in_out_data_as_str` from the testbench template, to make
  it easy to copy paste the output from edstem feedback box, formatted exactly as a python string, before disabling it again.
- To set it up inside Edstem see :doc:`edstem-setup`


.. toctree::
   :maxdepth: 2
   :caption: Index

   self
   edstem-setup
   api
   testbench-gen
   full-module-reference
   release-history