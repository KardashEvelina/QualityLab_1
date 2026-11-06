import ast
import json
from pathlib import Path


FILE = "lab8_inheritance_baseline.py"


def class_map(tree):
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def direct_parent(class_node):
    if not class_node.bases:
        return None

    base = class_node.bases[0]

    if isinstance(base, ast.Name):
        return base.id

    return None


def own_public_methods(class_node):
    return {
        node.name
        for node in class_node.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
        and not node.name.startswith("_")
    }


def inheritance_chain(
    class_name,
    classes,
):
    chain = []
    current = class_name

    while current in classes:
        chain.append(current)

        parent = direct_parent(
            classes[current]
        )

        if parent is None:
            break

        current = parent

    return chain


def public_interface(
    class_name,
    classes,
):
    methods = set()

    for name in inheritance_chain(
        class_name,
        classes,
    ):
        methods.update(
            own_public_methods(
                classes[name]
            )
        )

    return methods


def ancestor_methods(
    class_name,
    classes,
):
    chain = inheritance_chain(
        class_name,
        classes,
    )

    methods = set()

    for name in chain[1:]:
        methods.update(
            own_public_methods(
                classes[name]
            )
        )

    return methods


def analyze_class(
    class_name,
    classes,
):
    node = classes[class_name]

    own_methods = own_public_methods(
        node
    )

    inherited = ancestor_methods(
        class_name,
        classes,
    )

    overridden = (
        own_methods & inherited
    )

    chain = inheritance_chain(
        class_name,
        classes,
    )

    return {
        "class": class_name,
        "DIT": len(chain),
        "PIM": len(
            public_interface(
                class_name,
                classes,
            )
        ),
        "own_public_methods":
            len(own_methods),
        "overridden_methods":
            len(overridden),
        "overridden_names":
            sorted(overridden),
        "inheritance_chain":
            chain,
    }


source = Path(FILE).read_text(
    encoding="utf-8"
)

tree = ast.parse(source)
classes = class_map(tree)

targets = [
    "BasePlanningService",
    "ManagedPlanningService",
    "AdaptivePlanningService",
]

results = [
    analyze_class(
        name,
        classes,
    )
    for name in targets
]

Path(
    "lab8_results/inheritance_baseline.json"
).write_text(
    json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print(
    "===== INHERITANCE BASELINE ====="
)

for item in results:
    print()
    print(item["class"])
    print(
        "DIT =",
        item["DIT"],
    )
    print(
        "PIM =",
        item["PIM"],
    )
    print(
        "Overridden Methods =",
        item["overridden_methods"],
    )
    print(
        "Chain =",
        " -> ".join(
            item["inheritance_chain"]
        ),
    )

    if item["overridden_names"]:
        print(
            "Overrides:",
            ", ".join(
                item["overridden_names"]
            ),
        )
