import ast
import json
from pathlib import Path


FILES = {
    "Core Domain": {
        "source": "consent_service.py",
        "sonar_json": "lab8_results/core_domain_ck.json",
    },
    "Infrastructure": {
        "source": "privacy_logging.py",
        "sonar_json": "lab8_results/infrastructure_ck.json",
    },
    "Utility/DTO": {
        "source": "report_service.py",
        "sonar_json": "lab8_results/utility_ck.json",
    },
}


def read_sonar_complexity(path):
    data = json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

    measures = (
        data["component"]
        .get("measures", [])
    )

    for measure in measures:
        if measure["metric"] == "complexity":
            return int(measure["value"])

    return None


def collect_imports(tree):
    imports = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            add_direct_imports(
                node,
                imports
            )

        elif isinstance(node, ast.ImportFrom):
            add_from_imports(
                node,
                imports
            )

    return imports


def add_direct_imports(node, imports):
    for alias in node.names:
        local_name = (
            alias.asname
            or alias.name.split(".")[0]
        )

        imports[local_name] = alias.name


def add_from_imports(node, imports):
    module = node.module or ""

    for alias in node.names:
        local_name = (
            alias.asname
            or alias.name
        )

        imports[local_name] = (
            f"{module}.{alias.name}"
        )


def class_methods(class_node):
    return [
        node
        for node in class_node.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            )
        )
        and node.name != "__init__"
    ]


def method_self_attributes(method):
    attributes = set()

    for node in ast.walk(method):
        if is_self_attribute(node):
            attributes.add(node.attr)

    return attributes


def is_self_attribute(node):
    return (
        isinstance(node, ast.Attribute)
        and isinstance(
            node.value,
            ast.Name
        )
        and node.value.id == "self"
    )


def method_self_calls(method):
    calls = set()

    for node in ast.walk(method):
        if is_self_method_call(node):
            calls.add(node.func.attr)

    return calls


def is_self_method_call(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(
            node.func,
            ast.Attribute
        )
        and isinstance(
            node.func.value,
            ast.Name
        )
        and node.func.value.id == "self"
    )


def build_method_data(methods):
    attributes = {}
    calls = {}

    for method in methods:
        attributes[method.name] = (
            method_self_attributes(
                method
            )
        )

        calls[method.name] = (
            method_self_calls(
                method
            )
        )

    return attributes, calls


def methods_are_connected(
    left,
    right,
    attributes,
    calls,
):
    shared_attribute = bool(
        attributes[left]
        & attributes[right]
    )

    direct_call = (
        right in calls[left]
    )

    reverse_call = (
        left in calls[right]
    )

    return (
        shared_attribute
        or direct_call
        or reverse_call
    )


def create_graph(
    methods,
    attributes,
    calls,
):
    graph = {
        method.name: set()
        for method in methods
    }

    names = list(graph)

    for index, left in enumerate(names):
        connect_method(
            left,
            names[index + 1:],
            graph,
            attributes,
            calls,
        )

    return graph


def connect_method(
    left,
    remaining,
    graph,
    attributes,
    calls,
):
    for right in remaining:
        if methods_are_connected(
            left,
            right,
            attributes,
            calls,
        ):
            graph[left].add(right)
            graph[right].add(left)


def visit_component(
    start,
    graph,
    visited,
):
    stack = [start]

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        stack.extend(
            graph[current] - visited
        )


def count_components(graph):
    visited = set()
    components = 0

    for method_name in graph:
        if method_name in visited:
            continue

        components += 1

        visit_component(
            method_name,
            graph,
            visited,
        )

    return components


def calculate_lcom4(class_node):
    methods = class_methods(
        class_node
    )

    if not methods:
        return 0

    attributes, calls = (
        build_method_data(methods)
    )

    graph = create_graph(
        methods,
        attributes,
        calls,
    )

    return count_components(graph)


def imported_dependencies(
    class_node,
    imports,
):
    dependencies = set()

    for node in ast.walk(class_node):
        dependency = dependency_from_node(
            node,
            imports,
        )

        if dependency:
            dependencies.add(
                dependency
            )

    return dependencies


def dependency_from_node(
    node,
    imports,
):
    if isinstance(node, ast.Name):
        return imports.get(node.id)

    if isinstance(node, ast.Attribute):
        root = attribute_root(node)
        return imports.get(root)

    return None


def attribute_root(node):
    current = node

    while isinstance(
        current,
        ast.Attribute
    ):
        current = current.value

    if isinstance(current, ast.Name):
        return current.id

    return None


def analyze_file(filename):
    source = Path(filename).read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)
    imports = collect_imports(tree)

    classes = [
        node
        for node in tree.body
        if isinstance(
            node,
            ast.ClassDef
        )
    ]

    return [
        analyze_class(
            class_node,
            imports,
        )
        for class_node in classes
    ]


def analyze_class(
    class_node,
    imports,
):
    dependencies = (
        imported_dependencies(
            class_node,
            imports,
        )
    )

    return {
        "class": class_node.name,
        "CBO": len(dependencies),
        "dependencies": sorted(
            dependencies
        ),
        "LCOM4": calculate_lcom4(
            class_node
        ),
    }


def build_results():
    results = []

    for role, config in FILES.items():
        results.append({
            "role": role,
            "file": config["source"],
            "complexity":
                read_sonar_complexity(
                    config["sonar_json"]
                ),
            "classes":
                analyze_file(
                    config["source"]
                ),
        })

    return results


def save_results(results):
    Path(
        "lab8_results/ck_metrics.json"
    ).write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def print_results(results):
    print("===== CK METRICS =====")

    for item in results:
        print()
        print(
            f"{item['role']}: "
            f"{item['file']}"
        )

        print(
            "Sonar complexity =",
            item["complexity"],
        )

        for class_info in item["classes"]:
            print(
                f"{class_info['class']}: "
                f"CBO={class_info['CBO']}, "
                f"LCOM4={class_info['LCOM4']}"
            )

            print(
                "Dependencies:",
                ", ".join(
                    class_info[
                        "dependencies"
                    ]
                )
                or "none",
            )


results = build_results()
save_results(results)
print_results(results)
