---
owner: Developer Owner
status: published
review_date: 2027-02-19
---

# Local Development Environment

## Requirements

- Python 3.12;
- Git;
- virtual environment;
- pip.

## Setup

1. Clone repository:

git clone https://github.com/KardashEvelina/QualityLab_1.git
cd QualityLab_1

2. Create virtual environment:

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Run tests:

pytest -q

5. Run Flask API:

python3 app.py

6. Check service:

curl http://127.0.0.1:5000/health

STATUS: published
