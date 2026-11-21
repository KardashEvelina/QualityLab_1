import json
import os
from pathlib import Path


REPORT_FILE = Path("lab9_results/report.json")
LEDGER_FILE = Path("FINANCIAL_LEDGER.md")


def load_report():
    with REPORT_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    measures = {
        item["metric"]: float(item["value"])
        for item in data["component"]["measures"]
    }

    return (
        data["component"]["key"],
        measures["sqale_index"],
        measures["ncloc"],
    )


def load_config():
    hourly_rate = float(os.environ["HOURLY_RATE"])
    overload_coeff = float(os.environ["OVERLOAD_COEFF"])
    discount_rate = float(os.environ["DISCOUNT_RATE"])

    return hourly_rate, overload_coeff, discount_rate


def calculate_principal(
    sqale_index,
    hourly_rate,
    overload_coeff,
):
    return (
        (sqale_index / 60)
        * hourly_rate
        * overload_coeff
    )


def calculate_cost_of_delay(
    ncloc,
    hourly_rate,
):
    return (
        (ncloc / 100)
        * hourly_rate
    )


def calculate_npv(
    principal,
    cost_of_delay,
    discount_rate,
):
    cash_flows = []
    payback_month = None
    cumulative_gain = 0

    for month in range(1, 7):
        discounted_gain = (
            cost_of_delay
            / (1 + discount_rate) ** month
        )

        cumulative_gain += discounted_gain

        npv = (
            cumulative_gain
            - principal
        )

        cash_flows.append(
            {
                "month": month,
                "discounted_gain": discounted_gain,
                "npv": npv,
            }
        )

        if (
            npv > 0
            and payback_month is None
        ):
            payback_month = month

    return cash_flows, payback_month


def generate_ledger(
    project_key,
    ncloc,
    sqale_index,
    principal,
    cost_of_delay,
    cash_flows,
    payback_month,
):
    lines = [
        "# SOFTWARE ECONOMICS & FINANCIAL QUALITY LEDGER",
        "",
        "## System Baseline",
        "",
        f"- Project key: {project_key}",
        f"- NCLOC: {int(ncloc)}",
        f"- SQALE Index: {int(sqale_index)} minutes",
        "",
        "## Investment",
        "",
        f"- Principal: ${principal:.2f}",
        f"- Cost of Delay: ${cost_of_delay:.2f} per month",
        "",
        "## NPV",
        "",
        "| Month | Discounted Gain | Cumulative NPV |",
        "|---:|---:|---:|",
    ]

    for row in cash_flows:
        lines.append(
            f"| {row['month']} "
            f"| ${row['discounted_gain']:.2f} "
            f"| ${row['npv']:.2f} |"
        )

    lines.append("")

    if payback_month is not None:
        lines.append(
            f"Payback Period: Month {payback_month}"
        )
        lines.append("")
        lines.append("Quality Gate: PASS")
    else:
        lines.append("Payback Period: not reached")
        lines.append("")
        lines.append("Quality Gate: FAIL")

    LEDGER_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "FINANCIAL_LEDGER.md created successfully"
    )


def main():
    project_key, sqale_index, ncloc = load_report()

    (
        hourly_rate,
        overload_coeff,
        discount_rate,
    ) = load_config()

    principal = calculate_principal(
        sqale_index,
        hourly_rate,
        overload_coeff,
    )

    cost_of_delay = calculate_cost_of_delay(
        ncloc,
        hourly_rate,
    )

    cash_flows, payback_month = calculate_npv(
        principal,
        cost_of_delay,
        discount_rate,
    )

    generate_ledger(
        project_key,
        ncloc,
        sqale_index,
        principal,
        cost_of_delay,
        cash_flows,
        payback_month,
    )


if __name__ == "__main__":
    main()
