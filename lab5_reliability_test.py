import json
import subprocess
from pathlib import Path


SOURCE_FILE = Path("external_service.py")
RESULTS_DIR = Path("lab5_results")


def run_radon(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


def get_complexity(file_path):
    result = run_radon([
        "radon",
        "cc",
        str(file_path),
        "-j"
    ])

    blocks = next(iter(result.values()))

    return {
        block["name"]: block["complexity"]
        for block in blocks
    }


def get_raw_metrics(file_path):
    result = run_radon([
        "radon",
        "raw",
        str(file_path),
        "-j"
    ])

    metrics = next(iter(result.values()))

    return {
        "LOC": metrics["loc"],
        "LLOC": metrics["lloc"],
        "SLOC": metrics["sloc"]
    }


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    source = SOURCE_FILE.read_text(
        encoding="utf-8"
    )

    # Нормалізуємо переноси рядків.
    source = source.replace(
        "\r\n",
        "\n"
    ).replace(
        "\r",
        "\n"
    )

    lf_file = RESULTS_DIR / "external_service_lf.py"
    crlf_file = RESULTS_DIR / "external_service_crlf.py"

    # Версія Unix LF.
    lf_file.write_bytes(
        source.encode("utf-8")
    )

    # Версія Windows CRLF.
    crlf_file.write_bytes(
        source.replace(
            "\n",
            "\r\n"
        ).encode("utf-8")
    )

    lf_complexity = get_complexity(lf_file)
    crlf_complexity = get_complexity(crlf_file)

    lf_raw = get_raw_metrics(lf_file)
    crlf_raw = get_raw_metrics(crlf_file)

    print("=== RELIABILITY TEST ===")
    print()
    print("LF:")
    print("Raw metrics:", lf_raw)
    print("Complexity:", lf_complexity)

    print()
    print("CRLF:")
    print("Raw metrics:", crlf_raw)
    print("Complexity:", crlf_complexity)

    print()

    if (
        lf_complexity == crlf_complexity
        and lf_raw == crlf_raw
    ):
        print("RESULT: PASS")
        print(
            "Метрики однакові для LF та CRLF."
        )
    else:
        print("RESULT: FAIL")
        print(
            "Метрики змінилися через формат файлу."
        )


if __name__ == "__main__":
    main()