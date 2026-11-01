import ast

with open('app.py', 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

# Find all function definitions
print("All functions defined at module level:")
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        print(f"  {node.name} at line {node.lineno}")
        
print("\nFunctions with 'sentiment' in name:")
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and 'sentiment' in node.name.lower():
        print(f"  {node.name} at line {node.lineno}")
