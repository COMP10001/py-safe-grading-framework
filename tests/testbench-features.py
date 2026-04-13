# Feature Testing Testbench for safe testing framework
# Author: Kacie Beckett <kacie.beckett@unimelb.edu>
#
# Depends on Safe Ed Assignment Unit Testing Framework V0.3.1
# Author: Kacie Beckett <kacie.beckett@unimelb.edu> 2025/04/01
# Faculty of Engineering and IT - The University of Melbourne
# The latest version and documentation can be found in the COMP10001 Worksheet Repository
# https://edstem.org/au/courses/20911/lessons/79913/slides/539891
from pysafegradingfw import *

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
FILES_TO_HIDE = ["hidden.txt"] # eg ["abc.txt"]
PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'

test_bench = SafeTesting(
    setup_mode=True,
    make_all_tests_visible=RELEASE_TEST_CASES,
    show_all_passed_tests_first=True,
    show_test_reports=True,
    file_path_prefix='/home/',
)

test_bench.cache_hidden_test_files(FILES_TO_HIDE)

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
test_bench.register_pep8_test(
   name = "PEP8 Pass",
    student_file_name="pep8_pass.py",        
    ignored_tests=PEP8_IGNORED          
)

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
test_bench.register_pep8_test(
   name = "PEP8 Fail",
    student_file_name="pep8_fail.py",        
    ignored_tests=PEP8_IGNORED          
)

PEP8_IGNORED = 'E121,E123,E125,E126,E127,E128,E129,E221,E222,E223,E224,E225,E131,E133,E301,E302,E303,E304,E731,F401,F403,W2,W3,W503'
test_bench.register_pep8_test(
   name = "PEP8 Recursive File Check Fail",
    student_file_name="pep8_recursive_import_test.py",        
    ignored_tests=PEP8_IGNORED          
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Functions Pass ",
    student_file_name="astcheck_non_allowed_functions.py",
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Functions Fail ",
    student_file_name="astcheck_non_allowed_functions.py",
    non_allowed_functions=["print"],                         
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Pass",
    student_file_name="astcheck_non_allowed_imports.py",
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Fail",
    student_file_name="astcheck_non_allowed_imports.py",
    non_allowed_imports = ["sys"],                         
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Recursive Check Pass ",
    student_file_name="astcheck_recursive_import_test.py",
    non_allowed_imports = ["signal", "subprocess"],

)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Imports Recursive Check Fail ",
    student_file_name="astcheck_recursive_import_test.py",
    non_allowed_imports = ["sys","subprocess"],                         

)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Pass ",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = [ast.While],           
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Fail ",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = [ast.For],           
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Pass ",
    student_file_name="astcheck_required_nodes.py",
    required_nodes=[ast.For],                             
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Fail",
    student_file_name="astcheck_required_nodes.py",
    required_nodes=[ast.For, ast.While],                                 
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Custom Name Pass",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = {ast.While: "while loop"},    
)


test_bench.register_ast_test(
   name = "AST Check Non Allowed Nodes Custom Name Fail ",
    student_file_name="astcheck_non_allowed_nodes.py",
    non_allowed_nodes = {ast.For: "for loop"},            
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Custom Name Pass ",
    student_file_name="astcheck_required_nodes.py",
    required_nodes={ast.For: "for loop"},                              
)


test_bench.register_ast_test(
   name = "AST Check Required Nodes Custom Name Fail ",
    student_file_name="astcheck_required_nodes.py",
    required_nodes={ast.For: "for loop", ast.While: "while loop"},                            
)


test_bench.register_function_test(
   name = "Function Not Defined",
    student_file_name="function_tests.py",
    function_name="missing_function",                          
    function_args=["hello"],                                           
    function_expected = "Showing the fail formatting",                                 
    function_timeout_seconds = 1,                               
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Missing Body Fail",
    student_file_name="missing_function_body.py",
    function_name="missing_body",                          
    function_args=[],                                           
    function_expected = "",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Check 1 Input Arg Fail",
    student_file_name="function_tests.py",
    function_name="check_1_input_arg",                          
    function_args=("hello",),                                           
    function_expected = "Showing the fail formatting",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=True,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
)


test_bench.register_function_test(
   name = "Function Check 2 Input Arg Fail",
    student_file_name="function_tests.py",

    function_name="check_2_input_arg",                          
    function_args=["hello",12345],                                           
    function_expected = "Showing the fail formatting",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=True,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",

)


test_bench.register_function_test(
   name = "function fail on mutated args Input Fail",
    student_file_name="function_tests.py",
    function_name="check_mutate_fail",                          
    function_args=([1,2,3],),                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=True,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  

)


test_bench.register_function_test(
   name = "Function Return Int Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_int",                                         
    function_args=[],                                           
    function_expected = 1,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Int Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_int",                                         
    function_args=[],                                           
    function_expected = 4,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function  Str Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_str",                                         
    function_args=[],                                           
    function_expected = "abc\ndefgh\t\r\nhello",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Str Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_str",                                         
    function_args=[],                                           
    function_expected = "1234\n1234\n1234",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Float Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_float",                                         
    function_args=[],                                           
    function_expected = 1.0,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Float Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_float",                                         
    function_args=[],                                           
    function_expected = 1.5,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return List Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_list",                                         
    function_args=[],                                           
    function_expected = [1, 1.0, "abc", ("hi", 123)],                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return List Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_list",                                         
    function_args=[],                                           
    function_expected = [1,2,3,"abc"],                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Tuple Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_tuple",                                         
    function_args=[],                                           
    function_expected = (123, "abc", [1,2,3]),                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Return Tuple Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_tuple",                                         
    function_args=[],                                           
    function_expected = (1,2,3,"abc"),                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stdout Pass",
    student_file_name="function_tests.py",
    function_name="expected_stdout",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="Abc\nabc\t\r\nabc\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stdout Fail",
    student_file_name="function_tests.py",
    function_name="expected_stdout",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="1234\n1234\n\t\r\nasdfsdf",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stderr Pass",
    student_file_name="function_tests.py",
    function_name="expected_stderr",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="Fake Error has occurred.\n",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stderr Fail",
    student_file_name="function_tests.py",
    function_name="expected_stderr",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="Error",                                    
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stderr Exception Pass",
    student_file_name="function_tests.py",
    function_name="expected_stderr_exception",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr='Traceback (most recent call last):\n  File "/home/function_tests.py", line 34, in expected_stderr_exception\n    raise Exception("An error occured")\nException: An error occured\n\n',
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Stderr Exception Fail",
    student_file_name="function_tests.py",
    function_name="expected_stderr_exception",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="Error",                                    
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Return and Stdout Pass",
    student_file_name="function_tests.py",
    function_name="expected_return_and_stdout",                                         
    function_args=[],                                           
    function_expected = "abc",                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="abc\ndef\n",                               
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected Return and Stdout Fail",
    student_file_name="function_tests.py",
    function_name="expected_return_and_stdout",                                         
    function_args=[],                                           
    function_expected = "abc1234",                            
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="abc\ndef\nefgh\n",                               
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Timeout 1 second Fail",
    student_file_name="function_tests.py",
    function_name="timeout_fail",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Timeout 2 second Fail",
    student_file_name="function_tests.py",
    function_name="timeout_fail",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 2,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Hidden File Valid Access Pass",
    student_file_name="function_tests.py",
    function_name="hidden_files_access",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="verysecretfilecontents\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = ["hidden.txt"],
)


test_bench.register_function_test(
   name = "Function Hidden File Invalid Access Fail",
    student_file_name="function_tests.py",
    function_name="hidden_files_access",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="verysecretfilecontents\n",                
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Input Pass",
    student_file_name="function_tests.py",
    function_name="input_echoing",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="1\n2\n",                                                    
    input_echoing = False,                                        
    expected_stdout="Type in 1:Type in 2:True\nTrue\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = ["hidden.txt"],                                  
)


test_bench.register_function_test(
   name = "Function Input Fail",
    student_file_name="function_tests.py",
    function_name="input_echoing",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="1\n",                                                    
    input_echoing = False,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = ["hidden.txt"],                                  
)


test_bench.register_function_test(
   name = "Function Input Echoing Pass",
    student_file_name="function_tests.py",
    function_name="input_echoing",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="1\n2\n",                                                    
    input_echoing = True,                                        
    expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Input Echoing Fail",
    student_file_name="function_tests.py",
    function_name="input_echoing",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                               
    function_fail_on_mutated_args=False,                                      
    input_data="1\n",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Spam Print Fail",
    student_file_name="function_tests.py",
    function_name="spam_print",                                         
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 10,                              
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Spam Print Stdout and Stderr Fail",
    student_file_name="function_tests.py",
    function_name="spam_print_stdout_stderr",                  
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 10,                              
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Import With Dashes Pass",
    student_file_name="import-with-dashes.py",
    function_name="func",                  
    function_args=[],                                           
    function_expected = 123,                                 
    function_timeout_seconds = 10,                              
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected File Pass",
    student_file_name="function_tests.py",
    function_name="expected_file",                  
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                              
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file1.txt")],
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_function_test(
   name = "Function Expected File Fail",
    student_file_name="function_tests.py",
    function_name="expected_file",                  
    function_args=[],                                           
    function_expected = None,                                 
    function_timeout_seconds = 1,                              
    function_fail_on_mutated_args=False,                                      
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file2.txt")],
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports = [],
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Input Pass",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,                                   
    input_data="1\n2\n",                                                    
    input_echoing = False,                                        
    expected_stdout="Type in 1:Type in 2:True\nTrue\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Input Fail",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,                                   
    input_data="1\n",                                                    
    input_echoing = False,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Input Echoing Pass",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,                                   
    input_data="1\n2\n",                                                    
    input_echoing = True,                                        
    expected_stdout="Type in 1:1\nType in 2:2\nTrue\nTrue\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Input Echoing Fail",
    student_file_name="script_input_echoing.py",
    script_timeout_seconds=1,                                   
    input_data="1\n",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Timeout 1 Second Fail",
    student_file_name="script_timeout_fail.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Timeout 2 Second Fail",
    student_file_name="script_timeout_fail.py",
    script_timeout_seconds=2,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected Stdout Pass",
    student_file_name="script_expected_stdout.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="hello\n1234\t\r\nsdfsfds\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected Stdout Fail",
    student_file_name="script_expected_stdout.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="1234",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected Stderr Pass",
    student_file_name="script_expected_stderr.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="hello\n1234\t\r\nsdfsfds\n",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected Stderr Fail",
    student_file_name="script_expected_stderr.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="1234",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                 
)


test_bench.register_script_test(
   name = "Script Expected Stderr Exception Pass",
    student_file_name="script_expected_stderr_exception.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr='Traceback (most recent call last):\n  File "/home/script_expected_stderr_exception.py", line 1, in <module>\n    raise Exception("Test exception")\nException: Test exception\n\n',
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected Stderr Exception Fail",
    student_file_name="script_expected_stderr_exception.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="1234",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
    )


test_bench.register_script_test(
   name = "Script Hidden File Valid Access Pass",
    student_file_name="script_hidden_files.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="verysecretfilecontents\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = ["hidden.txt"],                                  
)


test_bench.register_script_test(
   name = "Script Hidden File Invalid Access Fail",
    student_file_name="script_hidden_files.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="verysecretfilecontents\n",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Import With Dashes Pass",
    student_file_name="import-with-dashes.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected File Pass",
    student_file_name="script_expected_file.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file1.txt")],
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


test_bench.register_script_test(
   name = "Script Expected File Fail",
    student_file_name="script_expected_file.py",
    script_timeout_seconds=1,                                   
    input_data="",                                                    
    input_echoing = True,                                        
    expected_stdout="",                                         
    expected_stderr="",
    expected_files=[("student_file.txt", "expected_file2.txt")],
    non_allowed_nodes = [],                                     
    non_allowed_functions=[],                                   
    non_allowed_imports=[],  
    required_nodes=[],                                          
    files_to_reveal = [],                                  
)


# @hidden[]

# testHidden
# pass


# @private[]

# testPrivate
# pass


# @score(1)
# testInt_Score
# pass


# @score(0.5)
# testFloat_Score
# pass

if __name__ == "__main__":
    test_bench.run_tests()

