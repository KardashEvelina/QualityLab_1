from datetime import date
from pathlib import Path
import re

today = date.today()
expired = []

for path in Path("docs").rglob("*.md"):
    text = path.read_text(encoding="utf-8")

    match = re.search(
        r"^review_date:\s*(\d{4}-\d{2}-\d{2})",
        text,
        re.MULTILINE,
    )

    if not match:
        continue

    review_date = date.fromisoformat(match.group(1))

    if review_date < today:
        expired.append((path, review_date))

print("===== DOCUMENT REVIEW AUDIT =====")

if not expired:
    print("No expired documentation found.")
else:
    for path, review_date in expired:
        print(f"EXPIRED: {path} -> {review_date}")

print(f"Expired documents: {len(expired)}")
