import ast
import json
from pathlib import Path


FILE = "lab8_pass_architecture.py"


def collect_imports(tree):
    imports = {}

    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                local = alias.asname or alias.name
                imports[local] = f"{module}.{alias.name}"

        elif isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name
                imports[local] = alias.name

    return imports


def class_dependencies(class_node, imports):
    dependencies = set()

    for node in ast.walk(class_node):
        if isinstance(node, ast.Name):
            dependency = imports.get(node.id)

            if dependency:
                dependencies.add(dependency)

    return dependencies


def class_methods(class_node):
    return [
        node
        for node in class_node.body
        if isinstance(node, ast.FunctionDef)
        and node.name != "__init__"
    ]


def self_attributes(method):
    result = set()

    for node in ast.walk(method):
        if not isinstance(node, ast.Attribute):
            continue

        if not isinstance(node.value, ast.Name):
            continue

        if node.value.id == "self":
            result.add(node.attr)

    return result


def connected(left, right):
    return bool(
        self_attributes(left)
        & self_attributes(right)
    )


def build_graph(methods):
    graph = {
        method.name: set()
        for method in methods
    }

    for index, left in enumerate(methods):
        for right in methods[index + 1:]:
            if connected(left, right):
                graph[left.name].add(
                    right.name
                )
                graph[right.name].add(
                    left.name
                )

    return graph


def count_components(graph):
    visited = set()
    components = 0

    for name in graph:
        if name in visited:
            continue

        components += 1
        stack = [name]

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            stack.extend(
                graph[current] - visited
            )

    return components


def calculate_lcom4(class_node):
    methods = class_methods(class_node)

    if not methods:
        return 0, 0.0

    if len(methods) == 1:
        return 1, 0.0

    graph = build_graph(methods)
    components = count_components(graph)

    normalized = (
        (components - 1)
        / len(methods)
    )

    return (
        components,
        normalized,
    )


source = Path(FILE).read_text(
    encoding="utf-8"
)

tree = ast.parse(source)
imports = collect_imports(tree)

results = []

for node in tree.body:
    if not isinstance(node, ast.ClassDef):
        continue

    dependencies = class_dependencies(
        node,
        imports,
    )

    lcom4, normalized = (
        calculate_lcom4(node)
    )

    results.append({
        "class": node.name,
        "CBO": len(dependencies),
        "dependencies": sorted(
            dependencies
        ),
        "LCOM4_components": lcom4,
        "LCOM_normalized": round(
            normalized,
            2
        ),
    })


Path(
    "lab8_results/pass_ck_metrics.json"
).write_text(
    json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)


print(
    "===== PASS CK METRICS ====="
)

for item in results:
    print()
    print(item["class"])
    print("CBO =", item["CBO"])
    print(
        "LCOM4 components =",
        item["LCOM4_components"],
    )
    print(
        "LCOM normalized =",
        item["LCOM_normalized"],
    )
    print(
        "Dependencies:",
        ", ".join(
            item["dependencies"]
        )
        or "none",
    )

max_cbo = max(
    item["CBO"]
    for item in results
)

max_lcom = max(
    item["LCOM_normalized"]
    for item in results
)

print()
print(
    "Maximum CBO =",
    max_cbo
)
print(
    "Maximum normalized LCOM =",
    max_lcom
)

if max_cbo <= 8 and max_lcom <= 0.2:
    print(
        "STATUS: GREEN / PASS"
    )
else:
    print(
        "STATUS: ARCHITECTURE LIMIT FAILED"
    )
