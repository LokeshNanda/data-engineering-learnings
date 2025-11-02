# Data Engineering Practice Book
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DuckDB](https://img.shields.io/badge/DuckDB-000000?style=for-the-badge&logo=DuckDB&logoColor=yellow)
![PySpark](https://img.shields.io/badge/PySpark-000000?style=for-the-badge&logo=apachespark&logoColor=E25A1C)
![VSCode Extension](https://img.shields.io/badge/DBCode-vscode_extension-blue)

Practical data engineering playground covering data structures, algorithms, analytical SQL, and PySpark - all within a single Python-first workspace.

## Table of Contents
- [Data Engineering Practice Book](#data-engineering-practice-book)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Tech Stack](#tech-stack)
  - [Project Layout](#project-layout)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Working With the Exercises](#working-with-the-exercises)
    - [Data Structures \& Algorithms](#data-structures--algorithms)
    - [DuckDB SQL Workflow](#duckdb-sql-workflow)
    - [PySpark Practice](#pyspark-practice)
    - [Design Patterns \& Theory](#design-patterns--theory)
  - [Running Checks](#running-checks)
  - [Adding New Content](#adding-new-content)
  - [Tooling Tips](#tooling-tips)
  - [Contributing](#contributing)

## Overview
- Central place to practice core data engineering skills: DSA problems, SQL analytics patterns, and PySpark data pipelines.
- Project metadata managed via `pyproject.toml`, enabling both [`uv`](https://github.com/astral-sh/uv) and `pip` workflows.
- Ready-to-run DuckDB sandbox for iterating on SQL questions with seeded tables and reproducible data.
- Lightweight documentation (both Markdown and code comments) to support quick revision before interviews or design sessions.

## Key Features
- **Data structures & algorithms:** Python implementations for array manipulation challenges, complete with supporting notes (`datastructures/arrays/DYNAMIC_ARRAY_README.md`).
- **SQL challenge lab:** DuckDB database generated from JSON definitions plus curated SQL prompts under `sql/`.
- **PySpark mirrors:** Equivalent PySpark solutions (for example, `spark/17-BusinessExpansion.py`) that model distributed transformations similar to the SQL outputs.
- **Design pattern primers:** Focused write-ups such as `designpatterns/SINGLETON_PATTERN.md` for systems design preparation.
- **Extensible layout:** Clean directory separation for future additions (system-design notes, additional algorithms, Spark jobs, etc.).

## Tech Stack
- **Language:** Python 3.12
- **Data tooling:** DuckDB, pandas, PySpark, tabulate
- **Package management:** `uv` (preferred) or standard `pip`
- **Recommended IDE:** VS Code with the DBCode extension for SQL execution

## Project Layout
```text
.
|-- algorithms/
|   `-- Time_Space_Complexity/
|       |-- TIMESPACE.md
|       `-- images/
|-- datastructures/
|   `-- arrays/
|       |-- 121_buy_sell_stock.py
|       |-- 169_majority_element.py
|       |-- 189_rotate_array.py
|       |-- 238_productarrayexceptself.py
|       |-- 26_remove_duplicate_sorted_array.py
|       |-- 283_move_zeroes.py
|       |-- DYNAMIC_ARRAY_README.md
|       |-- dynamic_array_self.py
|       `-- image.png
|-- designpatterns/
|   `-- SINGLETON_PATTERN.md
|-- duck_db/
|   |-- data/tables.json
|   |-- populate_duckdb.py
|   `-- sql_challenges.duckdb
|-- spark/
|   `-- 17-BusinessExpansion.py
|-- sql/
|   |-- 17-BusinessExpansion.sql
|   |-- 18-HeroProducts.sql
|   |-- 24-AccountBalance.sql
|   |-- 25-BoatLifestyleMarketing.sql
|   |-- 27-incomeTaxReturn.sql
|   |-- 29-SoftwareVsDataAnalytics.sql
|   `-- test_sql_code.py
|-- main.py
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

## Getting Started
### Prerequisites
- Python 3.12+
- Optional: `uv` for isolated, reproducible dependency management
- DuckDB and PySpark are installed automatically through `pip`/`uv`; no system-level binaries required

### Installation
1. Clone the repository.
2. Create and activate a virtual environment:
   - PowerShell: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - Bash: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies:
   - With `uv`: `uv sync`
   - With `pip`: `pip install -e .`

## Working With the Exercises
### Data Structures & Algorithms
- Run any solution directly with `python datastructures/arrays/<file>.py`. Scripts print sample inputs/outputs for quick verification.
- `datastructures/arrays/dynamic_array_self.py` demonstrates a `ctypes`-backed dynamic array; pair it with the accompanying guide in `datastructures/arrays/DYNAMIC_ARRAY_README.md`.
- Use `main.py` as a scratchpad entry point when prototyping new algorithm walkthroughs.

### DuckDB SQL Workflow
1. Seed the DuckDB database (idempotent): `python duck_db/populate_duckdb.py`. The script reads table schemas and rows from `duck_db/data/tables.json`.
2. Point `sql/test_sql_code.py` to the SQL file you want to validate by adjusting the `SQL_FILE` constant.
3. Execute the runner: `python sql/test_sql_code.py`. Results render as Markdown tables, so you can paste them into documentation or pull requests.
4. Inspect or query the generated database interactively using DuckDB CLI or compatible clients if desired; the file lives at `duck_db/sql_challenges.duckdb`.

### PySpark Practice
- `spark/17-BusinessExpansion.py` recreates the SQL solution in PySpark to reinforce transformations on distributed datasets.
- Launch the job with `python spark/17-BusinessExpansion.py`. A local `SparkSession` is created (no external cluster needed) and outputs the aggregated results to stdout.

### Design Patterns & Theory
- `designpatterns/SINGLETON_PATTERN.md` covers the Singleton pattern with examples and is a template for adding more design pattern deep dives.
- `algorithms/Time_Space_Complexity/` contains quick-reference notes and diagrams for Big-O reasoning.

## Running Checks
- SQL validation: `python sql/test_sql_code.py` (after setting `SQL_FILE`) runs the query against the DuckDB database.
- PySpark scripts: run with `python spark/<file>.py`; Spark will report schema issues or transformation errors immediately.
- Additional automated tests are not yet included; add them under a `tests/` directory or integrate CI as the project grows.

## Adding New Content
1. **SQL challenge:** extend `duck_db/data/tables.json` with new tables and seed rows, rerun `python duck_db/populate_duckdb.py`, then drop your SQL under `sql/` with a meaningful file name.
2. **PySpark solution:** mirror the SQL logic in `spark/`, using the same dataset so results remain comparable.
3. **DSA problem:** place Python solutions inside `datastructures/` (e.g., `lists/`, `trees/`) or `algorithms/` with accompanying Markdown notes.
4. **Documentation:** capture problem statements, diagrams, or reasoning in Markdown beside the corresponding code to keep everything self-contained.

## Tooling Tips
- Install the DBCode VS Code extension to run SQL files directly within the editor and preview results inline.
- `uv sync --dev` can lock additional tooling (linters, formatters, pytest) once you introduce them.
- Keep the generated DuckDB file out of version control for clean diffs; it is safe to regenerate on demand via the populate script.

## Contributing
- Use feature branches and open pull requests when collaborating.
- Match existing code style (PEP 8 for Python, uppercase keywords for SQL).
- Document non-obvious decisions in Markdown or code comments so others can follow along.
- Update this README when adding new practice areas to keep the catalog current.
