from __future__ import annotations

from pathlib import Path

from cdd_audit.cli import run_cli
from cdd_audit.config import empty_config
from cdd_audit.model import AuditResult
from cdd_audit.scanner import audit as scan


def audit(root: Path) -> AuditResult:
    return scan(root, empty_config())


__all__ = ("audit", "run_cli", "scan")
