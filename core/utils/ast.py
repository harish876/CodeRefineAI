
import ast
from html.parser import HTMLParser
import re

def extract_class(source_code: str, class_name: str) -> str:
    tree = ast.parse(source_code)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return ast.unparse(node)  

    return None  

def extract_python_code(text):
    code_blocks = re.findall(r"```py(.*?)```", text, re.DOTALL)
    return "\n\n".join(code_blocks).strip()