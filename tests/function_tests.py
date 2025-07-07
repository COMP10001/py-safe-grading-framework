import sys

def check_mutate_fail(a: list):
    a.append(1)

def expected_return_int():
    return 1
    
def expected_return_str():
    return "abc\ndefgh\t\r\nhello"
    
def expected_return_float():
    return 1.0
    
def expected_return_list():
    return [1, 1.0, "abc", ("hi", 123)]
    
def expected_return_tuple():
    return (123, "abc", [1,2,3])
    
def expected_stdout():
    print("Abc\nabc\nabc")

def expected_stderr():
    print("Fake Error has occurred.", file=sys.stderr)

def expected_stderr_exception():
    raise Exception("An error occured")
    
def expected_return_and_stdout():
    print("abc\ndef")
    return "abc"

    
def timeout_fail():
    while True:
        pass

def spam_print():
    while True:
        print("abcdefgh")
    
def hidden_files_invalid_access():
    with open("hidden.txt") as fp:
        print(fp.read())
    
def hidden_files_valid_access():
    with open("hidden.txt") as fp:
        print(fp.read())

def input_echoing():
    a = input("Type in 1:")
    b = input("Type in 2:")
    print(a == "1")
    print(b == "2")
