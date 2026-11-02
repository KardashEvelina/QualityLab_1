import json
import subprocess
import sys
from pathlib import Path


COVERAGE_THRESHOLD = 80.0
MUTATION_THRESHOLD = 65.0

COVERAGE_FILE = Path("coverage.json")
MUTATION_FILE = Path(
    "mutants/mutmut-cicd-stats.json"
)


def run(command):
    print("$", " ".join(command))

    result = subprocess.run(
        command
    )

    if result.returncode != 0:
        print("Помилка виконання команди.")
        sys.exit(result.returncode)


def get_coverage():
    run([
        "coverage",
        "erase",
    ])

    run([
        "coverage",
        "run",
        "--source=external_service",
        "-m",
        "pytest",
        "tests/test_resilience.py",
        "-q",
    ])

    run([
        "coverage",
        "json",
        "-o",
        str(COVERAGE_FILE),
    ])

    data = json.loads(
        COVERAGE_FILE.read_text(
            encoding="utf-8"
        )
    )

    return float(
        data["totals"]["percent_covered"]
    )


def get_mutation_score():
    run([
        "mutmut",
        "run",
    ])

    run([
        "mutmut",
        "export-cicd-stats",
    ])

    data = json.loads(
        MUTATION_FILE.read_text(
            encoding="utf-8"
        )
    )

    killed = int(data["killed"])
    timeout = int(data["timeout"])
    total = int(data["total"])
    skipped = int(data["skipped"])

    tested = total - skipped

    if tested == 0:
        return 0.0

    return (
        (killed + timeout)
        / tested
        * 100
    )


def main():
    print("=" * 55)
    print("LAB 5 — BALANCED QUALITY GATE")
    print("=" * 55)

    coverage = get_coverage()
    mutation = get_mutation_score()

    coverage_pass = (
        coverage >= COVERAGE_THRESHOLD
    )

    mutation_pass = (
        mutation >= MUTATION_THRESHOLD
    )

    final_pass = (
        coverage_pass
        and mutation_pass
    )

    print()
    print(
        f"Coverage: "
        f"{coverage:.2f}% "
        f">= {COVERAGE_THRESHOLD:.0f}% "
        f"=> "
        f"{'PASS' if coverage_pass else 'FAIL'}"
    )

    print(
        f"Mutation Score: "
        f"{mutation:.2f}% "
        f">= {MUTATION_THRESHOLD:.0f}% "
        f"=> "
        f"{'PASS' if mutation_pass else 'FAIL'}"
    )

    print()
    print(
        "FORMULA:"
    )

    print(
        f"({coverage:.2f}% >= 80%) "
        "AND "
        f"({mutation:.2f}% >= 65%)"
    )

    print()
    print(
        "FINAL QUALITY GATE:",
        "PASS" if final_pass else "FAIL"
    )

    sys.exit(
        0 if final_pass else 1
    )


if __name__ == "__main__":
    main()
