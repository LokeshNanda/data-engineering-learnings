# DSA
Curated data structures, algorithms implemented in Python, and SQL patterns & questions.
## Overview
- Hands-on implementations of core data structures with accompanying explanations.
- Opinionated project structure ready to scale with more algorithms and SQL examples.
- Python-first tooling managed through `pyproject.toml` and compatible with `uv` or `pip` workflows.
## Current Modules
- `arrays/dynamic_array_self.py`: Classic dynamic array implementation with resize logic and sample usage.
- `arrays/DYNAMIC_ARRAY_README.md`: Conceptual deep-dive and visuals that accompany the array implementation.
## Repository Layout
```text
.
|-- arrays/
|   |-- DYNAMIC_ARRAY_README.md
|   `-- dynamic_array_self.py
|-- main.py
|-- pyproject.toml
|-- uv.lock
`-- README.md
```
> A local `.venv/` is optional and kept out of version control.
## Getting Started
### Prerequisites
- Python 3.12 or newer
- (Optional) [`uv`](https://github.com/astral-sh/uv) for fast dependency management, or standard `pip`
### Installation
1. Clone the repository.
2. Create a virtual environment (recommended):
   - PowerShell: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - Bash: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies (currently none, but this keeps the workflow consistent):
   - With `uv`: `uv sync`
   - With `pip`: `pip install -e .`

## Usage
- Run the sample dynamic array script: `python arrays/dynamic_array_self.py`
- Explore `main.py` as the entry point for future orchestrated demos or CLI tooling.
## Documentation
- Module-specific guides live alongside their implementations (e.g., `arrays/DYNAMIC_ARRAY_README.md`).
