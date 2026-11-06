import ast
import json
from pathlib import Path


FILE = "lab8_composition.py"


def get_classes(tree):
    return [
        node
        for node in tree.body
        if isinstance(
            node,
            ast.ClassDef,
        )
    ]


def public_methods(class_node):
    return [
        node.name
        for node in class_node.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
        and not node.name.startswith("_")
    ]


def calculate_dit(class_node):
    if not class_node.bases:
        return 1

    return 2


def overridden_methods(class_node):
    if not class_node.bases:
        return 0

    return len(
        public_methods(class_node)
    )


source = Path(FILE).read_text(
    encoding="utf-8"
)

tree = ast.parse(source)

results = []

for class_node in get_classes(tree):
    results.append({
        "class":
            class_node.name,
        "DIT":
            calculate_dit(
                class_node
            ),
        "PIM":
            len(
                public_methods(
                    class_node
                )
            ),
        "Overridden":
            overridden_methods(
                class_node
            ),
    })


Path(
    "lab8_results/"
    "inheritance_pass.json"
).write_text(
    json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)


print(
    "===== COMPOSITION METRICS ====="
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
        item["Overridden"],
    )


max_dit = max(
    item["DIT"]
    for item in results
)

max_overridden = max(
    item["Overridden"]
    for item in results
)

print()
print(
    "Maximum DIT =",
    max_dit,
)

print(
    "Maximum Overridden =",
    max_overridden,
)

if (
    max_dit == 1
    and max_overridden == 0
):
    print(
        "STATUS: GREEN / PASS"
    )
else:
    print(
        "STATUS: FAILED"
    )
