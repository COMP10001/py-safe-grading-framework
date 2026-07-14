def mutated_args_pass(test_list):
    test_list.append(5)
    return test_list



def mutated_args_fail(test_list):
    return test_list + [5]
