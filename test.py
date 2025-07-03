import os
import ast

def cache_hidden_test_files(files):
    file_dict = {}
    for file in files:
        with open(file, 'r') as fp:
            file_dict[file] = fp.read()
        os.remove(file)
    return file_dict

class hidden_file_manager:
    def __init__(self, hidden_file_dict, files_to_reveal):
        self.hidden_file_dict = hidden_file_dict
        self.files_to_reveal = files_to_reveal
        for file in files_to_reveal:
            with open(file, 'w') as fp:
                fp.write(self.hidden_file_dict[file])
        
    def __enter__(self):
        pass
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.files_to_reveal:
            os.remove(file)
            
with open("abc.txt","w") as fp:
    fp.write("1234")
    
hide = ['abc.txt'] 
file_dict = cache_hidden_test_files(hide)

with hidden_file_manager(file_dict, hide):
    with open('abc.txt') as fp:
        print(fp.read())


    




class NodeTypeVisitor(ast.NodeVisitor):
    def __init__(self, types, *args, **kwargs):
        self.types = tuple(types)
        self.nodes = []

    def visit(self, node):
        if isinstance(node, self.types):
            self.nodes.append(node)
        super().visit(node)
        
def create_ast_object(filename):
    with open(filename) as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename)
    except:
        assert False, traceback.format_exc(limit=-1)

    return tree
     
def find_imports(ast_tree):
    visitor = NodeTypeVisitor((ast.Import, ast.ImportFrom))
    visitor.visit(ast_tree)
    imports = []
    for node in visitor.nodes:
        for alias in node.names:
            imports.append(alias.name)
    return imports

def find_local_import_paths(filename):
    file_path_components = filename.rsplit('/',1)
    path_prefix = ""
    if (len(file_path_components) > 1):
        path_prefix = file_path_components[0] + "/"
        
    tree = create_ast_object(filename)
    imports = find_imports(tree)
    local_import_paths = []
    for imported in imports:
        path = imported.split('.')
        path = path_prefix + "/".join(path) + ".py"
        if os.path.isfile(path):
            local_import_paths.append(path)
    
    return local_import_paths

def recursive_find_local_import_paths(filename):
    local_imports = find_local_import_paths(filename)
    files_checked = [filename]
   
    while (len(local_imports) > 0):
       next_import = local_imports.pop()
       if next_import not in files_checked:
           files_checked.append(next_import)
           local_imports += find_local_import_paths(next_import)
    return files_checked
            
    


# tree = create_ast_tree("safetestingframework.py")

# print(recursive_find_local_import_paths("safetestingframework.py"))