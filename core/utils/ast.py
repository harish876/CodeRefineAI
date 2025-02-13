
import ast

def extract_class(source_code: str, class_name: str) -> str:
    tree = ast.parse(source_code)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return ast.unparse(node)  

    return None  
