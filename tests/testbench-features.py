# Feature Testing Testbench for safe testing framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu>
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.0
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from safetestingframework import *

### ENSURE PER TESTCASE SCORING IS ENABLED!
### ENSURE TIMEOUT (s) IS SET HIGHER THAN THE SUM OF 'function_timeout_seconds' FOR EACH TEST!
### SEE TESTBENCH EXAMPLE FOR MORE EXPLANATION

# Remove the test file after loading by Ed, to prevent ability to print out contents
# os.remove(__file__)

# DANGER: Overrides Hidden and Private Tests so they become visible,
# Need to re-run test cases for all students for it to work
RELEASE_TEST_CASES = False 

STUDENT_FUNCTION = "test"
STUDENT_FILE_NAME = "program.py"
STUDENT_FILE_PATH_PREFIX = "/home/"

DEBUG_OUTPUT = True
SHOW_ALL_PASSED_TESTS_FIRST = True

FILES_TO_HIDE = ["hidden.txt"] # eg ["abc.txt"]
HIDDEN_FILE_DICT = cache_hidden_test_files(FILES_TO_HIDE)

class SafeTesting():
    @setname() 
    @score(0)
    def test_PEP8_Pass(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name="pep8_pass.py",         # File to test function from
            student_file_path_prefix="/home/",   # File path prefix, could change by Ed, but otherwise does not need to be touched
            ignored_tests=PEP8_IGNORED           # Modify as desired, this is the default value set in the framework.
        )
        
    @setname()
    @score(0)
    def test_PEP8_Fail(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name="pep8_fail.py",         # File to test function from
            student_file_path_prefix="/home/",   # File path prefix, could change by Ed, but otherwise does not need to be touched
            ignored_tests=PEP8_IGNORED           # Modify as desired, this is the default value set in the framework.
        )
        
    @setname()
    @score(0)
    def test_PEP8_Recursive_File_Check_Fail(self):
        PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
        run_pep8_test(
            student_file_name="pep8_recursive_import_test.py",         # File to test function from
            student_file_path_prefix="/home/",   # File path prefix, could change by Ed, but otherwise does not need to be touched
            ignored_tests=PEP8_IGNORED           # Modify as desired, this is the default value set in the framework.
        )

    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Functions_Pass(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_functions.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Functions_Fail(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_functions.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=("print"),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )

    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Imports_Pass(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_imports.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Imports_Fail(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_imports.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = ("sys"),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
        
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Imports_Recursive_Check_Pass(self): 
        run_astcheck_test(
            student_file_name="astcheck_recursive_import_test.py",
            student_file_path_prefix="/home/", # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = ("signal", "subprocess"),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Imports_Recursive_Check_Fail(self): 
        run_astcheck_test(
            student_file_name="astcheck_recursive_import_test.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = ("sys","subprocess"),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
        
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Nodes_Pass(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_nodes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (ast.While,),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testAST_Check_Non_Allowed_Nodes_Fail(self): 
        run_astcheck_test(
            student_file_name="astcheck_non_allowed_nodes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (ast.For,),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                 # Eg ast.Name, see ast library
        )

    @setname()
    @score(0)
    def testAST_Check_Required_Nodes_Pass(self): 
        run_astcheck_test(
            student_file_name="astcheck_required_nodes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(ast.For,),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testAST_Check_Required_Nodes_Fail(self): 
        run_astcheck_test(
            student_file_name="astcheck_required_nodes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX, # File path prefix, could change by Ed, but otherwise does not need to be touched
            non_allowed_nodes = (),            # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                          # Function names of any specific functions to disallow
            non_allowed_imports = (),                          # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(ast.For, ast.While),                                 # Eg ast.Name, see ast library
        )
    
    @setname()
    @score(0)
    def testFunction_Check_1_Input_Arg_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="check_1_input_arg",                           # Function to test
            function_input=("hello",),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "Showing the fail formatting",                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=True,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Check_2_Input_Arg_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="check_2_input_arg",                           # Function to test
            function_input=("hello",12345),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "Showing the fail formatting",                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=True,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Check_Mutate_Input_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="check_mutate_fail",                           # Function to test
            function_input=([1,2,3],),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=True,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )


    @setname()
    @score(0)
    def testFunction_Return_Int_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_int",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = 1,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Return_Int_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_int",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = 4,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Return_Str_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_str",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "abc\ndefgh\t\r\nhello",                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Return_Str_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_str",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "1234\n1234\n1234",                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Return_Float_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_float",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = 1.0,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Return_Float_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_float",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = 1.5,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Return_List_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_list",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = [1, 1.0, "abc", ("hi", 123)],                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Return_List_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_list",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = [1,2,3,"abc"],                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Return_Tuple_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_tuple",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = (123, "abc", [1,2,3]),                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Return_List_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_tuple",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = (1,2,3,"abc"),                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
        
    @setname()
    @score(0)
    def testFunction_Expected_Stdout_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stdout",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="Abc\nabc\t\r\nabc\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Stdout_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stdout",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="1234\n1234\n\t\r\nasdfsdf",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Stderr_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stderr",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="Fake Error has occurred.\n",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Stderr_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stderr",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="Error",                                    # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Expected_Stderr_Exception_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stderr_exception",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr='Traceback (most recent call last):\n  File "/home/function_tests.py", line 34, in expected_stderr_exception\n    raise Exception("An error occured")\nException: An error occured\n\n',                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Stderr_Exception_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_stderr_exception",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="Error",                                    # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Return_and_Stdout_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_and_stdout",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "abc",                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="abc\ndef\n",                                # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_Return_and_Stdout_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_return_and_stdout",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = "abc1234",                               # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="abc\ndef\nefgh\n",                                # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Timeout_1_second_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="timeout_fail",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Timeout_2_second_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="timeout_fail",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 2,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )


    @setname()
    @score(0)
    def testFunction_Hidden_File_Valid_Access_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="hidden_files_access",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="verysecretfilecontents\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = ["hidden.txt"],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Hidden_File_Invalid_Access_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="hidden_files_access",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="verysecretfilecontents\n",                 # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    
    @setname()
    @score(0)
    def testFunction_Input_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="input_echoing",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="1\n2\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = False,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="Type in 1:Type in 2:True\nTrue\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = ["hidden.txt"],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Input_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="input_echoing",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="1\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = False,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = ["hidden.txt"],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testFunction_Input_Echoing_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="input_echoing",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="1\n2\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    

    @setname()
    @score(0)
    def testFunction_Input_Echoing_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="input_echoing",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                                # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="1\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Spam_Print_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="spam_print",                                          # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 10,                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Spam_Print_Stdout_and_Stderr_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="spam_print_stdout_stderr",                   # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 10,                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Import_With_Dashes_Pass(self):
        return run_function_test(
            student_file_name="import-with-dashes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="func",                   # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = 123,                                    # Expected value for function
            function_timeout_seconds = 10,                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testFunction_Expected_File_Pass(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_file",                   # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            expected_files=[("student_file.txt", "expected_file1.txt")],
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testFunction_Expected_File_Fail(self):
        return run_function_test(
            student_file_name="function_tests.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            function_name="expected_file",                   # Function to test
            function_input=(),                                           # Must be wrapped in a tuple like test() -> () or test(1) -> (1,)
            function_expected = None,                                    # Expected value for function
            function_timeout_seconds = 1,                               # Time in seconds until test fails due to timeout
            check_mutate=False,                                          # Check if the function input was mutated
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            expected_files=[("student_file.txt", "expected_file2.txt")],
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports = (), # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
        
    @setname()
    @score(0)
    def testScript_Input_Pass(self):
        return run_script_test(
            student_file_name="script_input_echoing.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="1\n2\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = False,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="Type in 1:Type in 2:True\nTrue\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
        
    @setname()
    @score(0)
    def testScript_Input_Fail(self):
        return run_script_test(
            student_file_name="script_input_echoing.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="1\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = False,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    @setname()
    @score(0)
    def testScript_Input_Echoing_Pass(self):
        return run_script_test(
            student_file_name="script_input_echoing.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="1\n2\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
          
    @setname()
    @score(0)
    def testScript_Input_Echoing_Fail(self):
        return run_script_test(
            student_file_name="script_input_echoing.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="1\n",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testScript_Timeout_1_Second_Fail(self):
        return run_script_test(
            student_file_name="script_timeout_fail.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testScript_Timeout_2_Second_Fail(self):
        return run_script_test(
            student_file_name="script_timeout_fail.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=2,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testScript_Expected_Stdout_Pass(self):
        return run_script_test(
            student_file_name="script_expected_stdout.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="hello\n1234\t\r\nsdfsfds\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testScript_Expected_Stdout_Fail(self):
        return run_script_test(
            student_file_name="script_expected_stdout.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="1234",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testScript_Expected_Stderr_Pass(self):
        return run_script_test(
            student_file_name="script_expected_stderr.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="hello\n1234\t\r\nsdfsfds\n",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testScript_Expected_Stderr_Fail(self):
        return run_script_test(
            student_file_name="script_expected_stderr.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="1234",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )

    @setname()
    @score(0)
    def testScript_Expected_Stderr_Exception_Pass(self):
        return run_script_test(
            student_file_name="script_expected_stderr_exception.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr='Traceback (most recent call last):\n  File "/home/script_expected_stderr_exception.py", line 1, in <module>\n    raise Exception("Test exception")\nException: Test exception\n\n',                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testScript_Expected_Stderr_Exception_Fail(self):
        return run_script_test(
            student_file_name="script_expected_stderr_exception.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="1234",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = {},                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testScript_Hidden_File_Valid_Access_Pass(self):
        return run_script_test(
            student_file_name="script_hidden_files.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="verysecretfilecontents\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = ["hidden.txt"],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testScript_Hidden_File_Invalid_Access_Fail(self):
        return run_script_test(
            student_file_name="script_hidden_files.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="verysecretfilecontents\n",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
    
    @setname()
    @score(0)
    def testScript_Import_With_Dashes_Pass(self):
        return run_script_test(
            student_file_name="import-with-dashes.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testScript_Expected_File_Pass(self):
        return run_script_test(
            student_file_name="script_expected_file.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            expected_files=[("student_file.txt", "expected_file1.txt")],
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        
    @setname()
    @score(0)
    def testScript_Expected_File_Fail(self):
        return run_script_test(
            student_file_name="script_expected_file.py",
            student_file_path_prefix=STUDENT_FILE_PATH_PREFIX,           # File path prefix
            script_timeout_seconds=1,                                    # Time in seconds until test fails due to timeout
            input="",                                                    # Input that can be read by input() seperated by newlines
            input_echoing = True,                                        # When enabled, all input is echoed to stdout when read, similar to interactive terminal
            expected_stdout="",                                          # Expected value in stdout
            expected_stderr="",                                          # Expected value in stderr
            expected_files=[("student_file.txt", "expected_file2.txt")],
            non_allowed_nodes = (),                                      # Eg ast.Name, see run_astcheck_test and ast library
            non_allowed_functions=(),                                    # Function names of any specific functions to disallow
            non_allowed_imports=(),   # Imports that are not allowed anywhere in student file or any local imports
            required_nodes=(),                                           # Eg ast.Name, see run_astcheck_test and ast library
            files_to_reveal = [],                                        # Filenames in the hidden_file_dict keys to add to the path while this function runs
            hidden_file_dict = HIDDEN_FILE_DICT,                                       # Key: Filename, Value: File Content String | See cache_hidden_test_files function
        )
        

    @setname()
    @hidden()
    @score(0)
    def testHidden(self):
        pass
    
    @setname()
    @private()
    @score(0)
    def testPrivate(self):
        pass

    @setname()
    @score(1)
    def testInt_Score(self):
        pass
    
    @setname()
    @score(0.5)
    def testFloat_Score(self):
        pass

if __name__ == "__main__":
    run_tests(SafeTesting, debug_output=DEBUG_OUTPUT, show_all_passed_tests_first=SHOW_ALL_PASSED_TESTS_FIRST)
