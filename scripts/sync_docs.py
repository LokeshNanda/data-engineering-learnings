from __future__ import annotations

import shutil
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "docs",
    "site",
}

ASSET_EXTS = {
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
}


def collect_sources() -> list[Path]:
    sources: list[Path] = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        root_path = Path(root)
        for name in files:
            path = root_path / name
            suffix = path.suffix.lower()
            if suffix == ".md" or suffix in ASSET_EXTS:
                sources.append(path)
    return sources


def clean_docs_dir() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def copy_sources(sources: list[Path]) -> None:
    for source in sources:
        rel_path = source.relative_to(REPO_ROOT)
        target = DOCS_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def ensure_index() -> None:
    readme = REPO_ROOT / "README.md"
    index = DOCS_DIR / "index.md"
    if readme.exists():
        shutil.copy2(readme, index)
    else:
        index.write_text("# Documentation\n", encoding="utf-8")


def main() -> None:
    clean_docs_dir()
    sources = collect_sources()
    copy_sources(sources)
    ensure_index()


if __name__ == "__main__":
    main()
