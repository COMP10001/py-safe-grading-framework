# Py Safe Grading Framework

Testing infrastructure for safely testing student code, with easy access to testing specific functions,
entire script files, performing AST checks, and style checks. Output feedback clearly specifies, what
function return types should be, if they should or should not print output etc, with output and stderr formatting
showing hidden chars such as newlines while also preserving line wrapping to make it easier for students to understand
why their output differs.

The primary goal of this project is to make it as easy as possible to setup whatever test is required for an assignment. The existing tooling inside Edstem, and with test libraries such as PyUnit are not suitable.

Issues that this project solves:
- If a student crashes the testing infrastructure code they get 0, even if they passed preceeding test cases
    - Every test is run as a seperate subprocess with a time limit, so the tests are
      independant, and cannot influence the main process unless there is a bug which needs to
      be patched.
- Using input output tests, does not allow for particularly descriptive outputs or type checking
    - Can directly test python objects for types etc
- Custom checks are time consuming to setup
    - A comprehensive set of features are provided

Configured for use with Edstem, but could be extended to work with other platforms with minimal effort.

Developed primarily for COMP10001 at the University of Melbourne, but has also been used for other subjects.

For full documentation see [Documentation](https://comp10001.github.io/py-safe-grading-framework), or to build it locally use:

```bash
python -m venv .venv
source .venv/bin/activate # or equivalent for your OS
pip install -r requirements.txt
pip install -r doc-requirements.txt
python -m sphinx -b html docs/source docs/build/html
python -m http.server 8080 -d docs/build/html
```
Then you can access the documentation on localhost at `http://127.0.0.1:8080`.

### Author
Kacie Beckett, University of Melbourne

### License
MIT License
