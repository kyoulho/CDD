from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from cdd_audit.model import JsonValue, SectionHint


@dataclass(frozen=True, slots=True)
class RoleOverride:
    path: str
    role: str


@dataclass(frozen=True, slots=True)
class AuditConfig:
    default_read_path: tuple[str, ...]
    required_read_documents: tuple[str, ...]
    excluded_historical_records: tuple[str, ...]
    excluded_non_sot_references: tuple[str, ...]
    task_retention: TaskRetentionConfig
    section_hints: tuple[SectionHint, ...]
    role_overrides: tuple[RoleOverride, ...]
    ignore_patterns: tuple[str, ...]
    current_work_pointer: str | None
    config_path: Path | None


@dataclass(frozen=True, slots=True)
class TaskRetentionConfig:
    active_task_limit: int
    recent_completed_task_limit: int
    rollup_by: str


@dataclass(frozen=True, slots=True)
class ConfigError:
    message: str


def empty_config() -> AuditConfig:
    return AuditConfig((), (), (), (), default_task_retention(), (), (), (), None, None)


def default_task_retention() -> TaskRetentionConfig:
    return TaskRetentionConfig(active_task_limit=3, recent_completed_task_limit=3, rollup_by="version-or-milestone")


def load_config(root: Path, explicit_path: Path | None) -> AuditConfig | ConfigError:
    path = _config_path(root, explicit_path)
    if path is None:
        return empty_config()
    try:
        parsed: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        return ConfigError(f"config not readable: {path}: {error}")
    except json.JSONDecodeError as error:
        return ConfigError(f"config is not valid JSON: {path}: {error}")
    if not isinstance(parsed, dict):
        return ConfigError(f"config must be a JSON object: {path}")
    return AuditConfig(
        default_read_path=_string_tuple(parsed.get("defaultReadPath")),
        required_read_documents=_string_tuple(parsed.get("requiredReadDocuments")),
        excluded_historical_records=_string_tuple(parsed.get("excludedHistoricalRecords")),
        excluded_non_sot_references=_string_tuple(parsed.get("excludedNonSotReferences")),
        task_retention=_task_retention(parsed.get("taskRetention")),
        section_hints=_section_hints(parsed.get("sectionHints")),
        role_overrides=_role_overrides(parsed.get("roleOverrides")),
        ignore_patterns=_string_tuple(parsed.get("ignore")),
        current_work_pointer=_optional_string(parsed.get("currentWorkPointer")),
        config_path=path,
    )


def _config_path(root: Path, explicit_path: Path | None) -> Path | None:
    if explicit_path is not None:
        return explicit_path.resolve()
    for candidate in (root / ".cdd-audit.json", root / "cdd-audit.json", root / ".cdd" / "audit.json"):
        if candidate.is_file():
            return candidate
    return None


def _string_tuple(value: JsonValue | None) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, list):
        return ()
    result: list[str] = []
    for item in value:
        if isinstance(item, str):
            result.append(item)
    return tuple(result)


def _optional_string(value: JsonValue | None) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _task_retention(value: JsonValue | None) -> TaskRetentionConfig:
    default = default_task_retention()
    if not isinstance(value, dict):
        return default
    return TaskRetentionConfig(
        active_task_limit=_positive_int(value.get("activeTaskLimit"), default.active_task_limit),
        recent_completed_task_limit=_positive_int(
            value.get("recentCompletedTaskLimit"),
            default.recent_completed_task_limit,
        ),
        rollup_by=_optional_string(value.get("rollupBy")) or default.rollup_by,
    )


def _positive_int(value: JsonValue | None, default: int) -> int:
    if isinstance(value, int) and value > 0:
        return value
    return default


def _role_overrides(value: JsonValue | None) -> tuple[RoleOverride, ...]:
    if not isinstance(value, dict):
        return ()
    result: list[RoleOverride] = []
    for key, item in value.items():
        if isinstance(item, str):
            result.append(RoleOverride(key, item))
    return tuple(result)


def _section_hints(value: JsonValue | None) -> tuple[SectionHint, ...]:
    if not isinstance(value, dict):
        return ()
    result: list[SectionHint] = []
    for key, item in value.items():
        headings = _string_tuple(item)
        if headings:
            result.append(SectionHint(key, headings))
    return tuple(result)
