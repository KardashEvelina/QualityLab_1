import ast
import json
from pathlib import Path


EXCLUDED_FILES = {
    "lab8_ck_metrics.py",
    "lab8_pass_metrics.py",
    "lab8_inheritance_metrics.py",
    "lab8_composition_metrics.py",
    "lab8_mood_metrics.py",
    "lab8_pass_demo.py",
    "lab8_composition_demo.py",
    "lab8_fail_demo.py",
    "lab8_inheritance_fail_demo.py",
    "lab8_god_metrics.py",
    "lab8_god_object.py",
    "lab8_inheritance_baseline.py",
}


def source_files():
    result = []

    for path in Path(".").glob("*.py"):
        if path.name in EXCLUDED_FILES:
            continue

        if path.name.startswith(
            ("lab5_", "lab6_")
        ):
            continue

        result.append(path)

    return sorted(result)


def is_dunder(name):
    return (
        name.startswith("__")
        and name.endswith("__")
    )


def public_or_hidden_methods(
    class_node,
):
    methods = []

    for node in class_node.body:
        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        if is_dunder(node.name):
            continue

        methods.append(node.name)

    return methods


def self_attributes(class_node):
    attributes = set()

    for node in ast.walk(class_node):
        if not isinstance(
            node,
            ast.Attribute,
        ):
            continue

        if not isinstance(
            node.value,
            ast.Name,
        ):
            continue

        if node.value.id != "self":
            continue

        attributes.add(node.attr)

    return attributes


def collect_classes(files):
    classes = []

    for path in files:
        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

        for node in tree.body:
            if isinstance(
                node,
                ast.ClassDef,
            ):
                classes.append(
                    {
                        "file": path.name,
                        "name": node.name,
                        "node": node,
                    }
                )

    return classes


def class_references(
    class_info,
    class_names,
):
    references = set()

    for node in ast.walk(
        class_info["node"]
    ):
        if not isinstance(
            node,
            ast.Name,
        ):
            continue

        if node.id not in class_names:
            continue

        if node.id == class_info["name"]:
            continue

        references.add(node.id)

    return references


def calculate_hiding(classes):
    total_methods = 0
    hidden_methods = 0

    total_attributes = 0
    hidden_attributes = 0

    for item in classes:
        methods = public_or_hidden_methods(
            item["node"]
        )

        attributes = self_attributes(
            item["node"]
        )

        total_methods += len(methods)
        hidden_methods += sum(
            name.startswith("_")
            for name in methods
        )

        total_attributes += len(
            attributes
        )

        hidden_attributes += sum(
            name.startswith("_")
            for name in attributes
        )

    return (
        total_methods,
        hidden_methods,
        total_attributes,
        hidden_attributes,
    )


def calculate_cof(classes):
    class_names = {
        item["name"]
        for item in classes
    }

    edges = {}

    for item in classes:
        key = (
            f"{item['file']}:"
            f"{item['name']}"
        )

        edges[key] = sorted(
            class_references(
                item,
                class_names,
            )
        )

    actual = sum(
        len(values)
        for values in edges.values()
    )

    class_count = len(classes)

    possible = (
        class_count
        * (class_count - 1)
    )

    cof = (
        actual / possible * 100
        if possible
        else 0.0
    )

    return actual, possible, cof, edges


files = source_files()
classes = collect_classes(files)

(
    total_methods,
    hidden_methods,
    total_attributes,
    hidden_attributes,
) = calculate_hiding(classes)

mhf = (
    hidden_methods
    / total_methods
    * 100
    if total_methods
    else 0.0
)

ahf = (
    hidden_attributes
    / total_attributes
    * 100
    if total_attributes
    else 0.0
)

(
    actual_edges,
    possible_edges,
    cof,
    coupling_edges,
) = calculate_cof(classes)


result = {
    "methodology": {
        "language": "Python",
        "MHF":
            "methods starting with _ are treated as hidden; dunder methods excluded",
        "AHF":
            "self attributes starting with _ are treated as hidden",
        "COF":
            "directed class references / N*(N-1)",
    },
    "files_analyzed": [
        path.name
        for path in files
    ],
    "class_count": len(classes),
    "methods": {
        "total": total_methods,
        "hidden": hidden_methods,
    },
    "attributes": {
        "total": total_attributes,
        "hidden": hidden_attributes,
    },
    "coupling": {
        "actual_edges": actual_edges,
        "possible_edges":
            possible_edges,
    },
    "MHF_percent": round(
        mhf,
        2,
    ),
    "AHF_percent": round(
        ahf,
        2,
    ),
    "COF_percent": round(
        cof,
        2,
    ),
    "coupling_edges":
        coupling_edges,
}


Path(
    "lab8_results/mood_metrics.json"
).write_text(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)


print("===== GLOBAL MOOD METRICS =====")
print(
    "Classes =",
    len(classes),
)
print(
    "Methods =",
    f"{hidden_methods}/{total_methods} hidden",
)
print(
    "Attributes =",
    f"{hidden_attributes}/{total_attributes} hidden",
)
print(
    "Coupling edges =",
    f"{actual_edges}/{possible_edges}",
)
print()
print(
    f"MHF = {mhf:.2f}%"
)
print(
    f"AHF = {ahf:.2f}%"
)
print(
    f"COF = {cof:.2f}%"
)
