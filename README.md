# DSA
Hands-on data structures, algorithms, SQL challenges, and PySpark exercises, all in one Python-first workspace.
## Overview
- Python 3.12 project managed through `pyproject.toml` and compatible with either `uv` or traditional `pip` workflows.
- Data structure implementations paired with short writeups for quick revision.
- Self-contained DuckDB sandbox (DDL + seed data) to iterate on analytical SQL problems.
- PySpark notebooks converted to runnable scripts for distributed-processing practice.
## Repository Layout
```text
.
|-- algorithms/                 # Placeholder for upcoming algorithm walkthroughs
|-- datastructures/
|   `-- arrays/
|       |-- 283_move_zeroes.py  # LeetCode-style two-pointer exercise
|       |-- DYNAMIC_ARRAY_README.md
|       `-- dynamic_array_self.py
|-- duck_db/
|   |-- data/tables.json        # Table definitions + seed rows
|   |-- populate_duckdb.py      # Bootstrap the DuckDB file from JSON
|   `-- sql_challenges.duckdb   # Generated DuckDB database (git-ignored in CI/CD)
|-- spark/
|   `-- 17-BusinessExpansion.py # PySpark solution mirroring the SQL prompt
|-- sql/
|   |-- 17-BusinessExpansion.sql
|   `-- test_sql_code.py        # Helper to execute SQL scripts against DuckDB
|-- main.py
|-- pyproject.toml
`-- README.md
```
## Local Setup
### Prerequisites
- Python 3.12+
- Optional: [`uv`](https://github.com/astral-sh/uv) for fast dependency management
### Installation
1. Clone the repo.
2. Create and activate a virtual environment:
   - PowerShell: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - Bash: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies:
   - With `uv`: `uv sync`
   - With `pip`: `pip install -e .`
## Working With The Modules
### Data Structures & Algorithms
- `datastructures/arrays/dynamic_array_self.py` implements a Pythonic dynamic array backed by `ctypes`. Invoke directly with `python datastructures/arrays/dynamic_array_self.py` to step through the sample operations.
- `datastructures/arrays/283_move_zeroes.py` solves the in-place 'Move Zeroes' problem using a two-pointer approach. Run `python datastructures/arrays/283_move_zeroes.py` to see example outputs.
- Concept notes and diagrams for the dynamic array live in `datastructures/arrays/DYNAMIC_ARRAY_README.md`.
### DuckDB SQL Playground
1. Populate the database: `python duck_db/populate_duckdb.py`. The script reads `duck_db/data/tables.json` and materialises `duck_db/sql_challenges.duckdb`.
2. Execute a SQL solution: update `SQL_FILE` inside `sql/test_sql_code.py` (defaults to `17-BusinessExpansion.sql`) and run `python sql/test_sql_code.py`. Results print as a Markdown table.
3. Add new challenges by extending `tables.json` with additional table definitions and seeding data.
### PySpark Exercises
- `spark/17-BusinessExpansion.py` mirrors the SQL challenge with pure PySpark. Launch it via `python spark/17-BusinessExpansion.py`. The script creates an in-memory DataFrame, derives the first operation year per city, and aggregates the final counts.
## Tips & Next Steps
- Use `main.py` as a scratchpad entry point while experimenting with new modules.
- Keep challenge-specific assets together (problem statement, SQL, Python translation) for easier review.
- `uv sync --dev` can pin any future testing or linting toolchains once they are added.