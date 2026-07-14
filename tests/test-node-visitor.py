from pysafegradingfw import *
sys.stdout = ORIGINAL_STDOUT

tree,_ = create_ast_object("node_visitor_sample.py")
checker = CustomNodeVisitor(tree, types=[ast.While, ast.For])
print("Imports", checker.imports)
print("Function Calls", sorted(checker.function_calls))
print("Method Calls", sorted(checker.method_calls))
print("Attributes Called", sorted(checker.attributes_called))
print("Attribute Paths", sorted(checker.attribute_paths))
print("Defined Functions", sorted(checker.defined_functions))
print("Nodes", sorted(checker.nodes))


