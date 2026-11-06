import ast
from pathlib import Path


FILE = "lab8_god_object.py"


def collect_imports(tree):
    imports = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                imports[local] = alias.name

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                local = alias.asname or alias.name
                imports[local] = f"{module}.{alias.name}"

    return imports


def class_dependencies(class_node, imports):
    dependencies = set()

    for node in ast.walk(class_node):
        if isinstance(node, ast.Name) and node.id in imports:
            dependencies.add(imports[node.id])

    return dependencies


source = Path(FILE).read_text(encoding="utf-8")
tree = ast.parse(source)
imports = collect_imports(tree)

god_class = next(
    node
    for node in tree.body
    if isinstance(node, ast.ClassDef)
    and node.name == "Lab8GodObject"
)

dependencies = class_dependencies(
    god_class,
    imports
)

print("===== GOD OBJECT COUPLING =====")
print("Class: Lab8GodObject")
print("CBO =", len(dependencies))
print()

for dependency in sorted(dependencies):
    print("-", dependency)

if len(dependencies) > 15:
    print()
    print("STATUS: CRITICAL GOD OBJECT (CBO > 15)")
else:
    print()
    print("STATUS: CBO NOT CRITICAL")
