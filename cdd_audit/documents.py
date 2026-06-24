from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path
import re

from cdd_audit.config import AuditConfig
from cdd_audit.model import ACTIVE_SIGNALS, HISTORY_SIGNALS, NON_SOT_SIGNALS, DocumentInfo

HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
CDD_PUBLIC_ENTRYPOINTS = frozenset(
    {
        "start-here.md",
        "plan-task.md",
        "write-implementation-prompt.md",
        "cleanup-delete.md",
        "verify-work.md",
        "revise-work.md",
        "complete-work.md",
    }
)

IGNORED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".nuxt",
        ".cache",
        "__pycache__",
    }
)


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    path: str
    text: str
    metadata: Mapping[str, str]
    signals: tuple[str, ...]
    status: str | None


def read_documents(root: Path, config: AuditConfig) -> list[DocumentInfo]:
    result: list[DocumentInfo] = []
    cdd_skill_root = _is_cdd_skill_root(root)
    for path in sorted(root.rglob("*")):
        if not _readable_document(path, root, config):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        text = raw.decode("utf-8", errors="replace")
        lowered = text.lower()
        path_lower = rel.lower()
        metadata = _frontmatter(text)
        signals = _signals(path_lower, lowered)
        status = _status(lowered, metadata)
        parsed = ParsedDocument(path_lower, lowered, metadata, signals, status)
        role = _role(parsed, config, cdd_skill_root)
        result.append(
            DocumentInfo(
                path=rel,
                role=role,
                lines=text.count("\n") + (0 if text.endswith("\n") or not text else 1),
                bytes_size=len(raw),
                in_default_read_path=_in_default_read_path(parsed, role, config),
                status=status,
                signals=signals,
                headings=_headings(text),
                text=text,
                text_lower=f"{path_lower}\n{lowered}",
            )
        )
    return result


def _readable_document(path: Path, root: Path, config: AuditConfig) -> bool:
    if not path.is_file() or path.suffix.lower() not in {".md", ".yml", ".yaml"}:
        return False
    rel = path.relative_to(root).as_posix()
    if any(part in IGNORED_DIRS for part in path.parts):
        return False
    return not any(fnmatchcase(rel, pattern) for pattern in config.ignore_patterns)


def _signals(path: str, text: str) -> tuple[str, ...]:
    found: list[str] = []
    for signal in NON_SOT_SIGNALS + HISTORY_SIGNALS + ACTIVE_SIGNALS:
        if signal in path or signal in text:
            found.append(signal)
    return tuple(found)


def _headings(text: str) -> tuple[str, ...]:
    result: list[str] = []
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line.strip())
        if match is not None:
            result.append(f"{match.group(1)} {match.group(2).strip()}")
    return tuple(result)


def _role(parsed: ParsedDocument, config: AuditConfig, cdd_skill_root: bool) -> str:
    override = _role_override(parsed.path, config)
    if override is not None:
        return override
    declared = (
        parsed.metadata.get("role") or parsed.metadata.get("documentRole") or parsed.metadata.get("type") or ""
    ).lower()
    if declared in {"current-criteria", "active-index", "task-contract", "history", "non-sot-reference", "unknown"}:
        return declared
    if config.current_work_pointer == parsed.path:
        return "active-index"
    if cdd_skill_root:
        cdd_role = _cdd_skill_role(parsed.path)
        if cdd_role is not None:
            return cdd_role
    if any(signal in parsed.path for signal in NON_SOT_SIGNALS) or "role: non-sot-reference" in parsed.text:
        return "non-sot-reference"
    if (
        any(signal in parsed.path for signal in HISTORY_SIGNALS)
        or "role: history" in parsed.text
        or parsed.status in {"COMPLETE", "SUPERSEDED"}
    ):
        return "history"
    if "current-work" in parsed.path:
        return "active-index"
    if any(token in parsed.path for token in ("product", "engineering", "sot", "design")):
        return "current-criteria"
    if "task" in parsed.path:
        return "task-contract"
    return "unknown"


def _is_cdd_skill_root(root: Path) -> bool:
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return False
    try:
        metadata = _frontmatter(skill_path.read_text(encoding="utf-8"))
    except OSError:
        return False
    return metadata.get("name") == "cdd"


def _cdd_skill_role(path: str) -> str | None:
    if path in CDD_PUBLIC_ENTRYPOINTS:
        return "cdd-public-entrypoint"
    if path.startswith("_") and path.endswith(".md"):
        return "cdd-internal-module"
    if path.startswith("references/"):
        return "cdd-reference"
    return None


def _role_override(path: str, config: AuditConfig) -> str | None:
    for override in config.role_overrides:
        if fnmatchcase(path, override.path):
            return override.role
    return None


def _in_default_read_path(parsed: ParsedDocument, role: str, config: AuditConfig) -> bool:
    if any(fnmatchcase(parsed.path, pattern) for pattern in config.default_read_path):
        return True
    if role in {"history", "non-sot-reference"}:
        return False
    index_path = parsed.path in {"readme.md", "docs/readme.md", "agents.md", "skill.md"}
    registry = "document-registry" in parsed.path or "current-work" in parsed.path
    criteria = any(token in parsed.path for token in ("product", "engineering", "sot", "design"))
    task_index = any(token in parsed.path for token in ("task-contract", "implementation-task-contract"))
    return index_path or registry or criteria or task_index


def _status(text: str, metadata: dict[str, str]) -> str | None:
    declared = metadata.get("status")
    if declared:
        return declared.upper()
    for status in ("APPROVED", "DRAFT", "COMPLETE", "DEPRECATED", "SUPERSEDED"):
        if re.search(rf"(?im)^\s*status\s*[:=]\s*['\"]?{status.lower()}['\"]?\b", text):
            return status
    return None


def _frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result
