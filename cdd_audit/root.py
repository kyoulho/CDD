from __future__ import annotations

from pathlib import Path


def detect_project_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if _is_project_root(candidate):
            return candidate
    return current


def _is_project_root(path: Path) -> bool:
    markers = (
        path / ".git",
        path / ".cdd-audit.json",
        path / "cdd-audit.json",
        path / "docs" / "README.md",
        path / "docs" / "project" / "current-work.md",
        path / "document-registry.yml",
        path / "document-registry.yaml",
        path / "AGENTS.md",
    )
    return any(marker.exists() for marker in markers)
