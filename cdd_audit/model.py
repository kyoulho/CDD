from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

JsonValue = str | int | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject = dict[str, JsonValue]

HOT_PATH_LINES: Final[int] = 400
HOT_PATH_BYTES: Final[int] = 40 * 1024
ACCUMULATED_LINES: Final[int] = 1000

CURRENT_POINTER_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    "currentGate": ("currentgate", "current gate", "현재 gate", "현재 게이트"),
    "nextTask": ("nexttask", "next task", "다음 task", "다음 작업"),
    "activeTasks": ("activetasks", "active tasks", "현재 진행 가능한 task", "진행 가능한 작업"),
    "requiredReadDocuments": ("requiredreaddocuments", "반드시 읽을 문서", "읽어야 할 문서"),
    "excludedHistoricalRecords": ("excludedhistoricalrecords", "읽지 않을 과거 기록", "제외할 과거 기록"),
    "currentConflicts": ("currentconflicts", "현재 기준과 충돌", "충돌하는 문서"),
    "readmeOrIndexUpdatesRequired": ("readmeorindexupdatesrequired", "readme/index", "index 갱신"),
}

NON_SOT_SIGNALS: Final[tuple[str, ...]] = (
    "codesight",
    "agentmemory",
    "search index",
    "recall output",
    "archive branch",
    "generated map",
)

HISTORY_SIGNALS: Final[tuple[str, ...]] = (
    "completion",
    "verification",
    "old prompt",
    "history",
    "archive",
    "superseded",
    "완료 기록",
    "검증 기록",
    "과거 기록",
)

ACTIVE_SIGNALS: Final[tuple[str, ...]] = (
    "current gate",
    "next task",
    "active task",
    "현재 gate",
    "다음 task",
    "현재 진행 가능한",
)

SEVERITY_ORDER: Final[dict[str, int]] = {"blocking": 0, "warning": 1, "info": 2}

PROHIBITED_ACTIONS: Final[tuple[str, ...]] = (
    "autoSplitFiles",
    "autoDeleteStaleDocs",
    "autoPromoteHistoryToCurrentCriteria",
    "autoDeclareCurrentCriteria",
    "autoModifyReadmeOrIndexWithoutApproval",
)


@dataclass(frozen=True, slots=True)
class DocumentInfo:
    path: str
    role: str
    lines: int
    bytes_size: int
    in_default_read_path: bool
    status: str | None
    signals: tuple[str, ...]
    headings: tuple[str, ...]
    text: str
    text_lower: str

    def to_json(self) -> JsonObject:
        return {
            "path": self.path,
            "role": self.role,
            "lines": self.lines,
            "bytes": self.bytes_size,
            "inDefaultReadPath": self.in_default_read_path,
            "status": self.status,
            "signals": list(self.signals),
            "headings": list(self.headings),
        }


@dataclass(frozen=True, slots=True)
class SectionLocation:
    heading: str
    start_line: int | None
    end_line: int | None
    exists: bool
    suggested_headings: tuple[str, ...] = ()

    def to_json(self) -> JsonObject:
        result: JsonObject = {
            "heading": self.heading,
            "startLine": self.start_line,
            "endLine": self.end_line,
            "exists": self.exists,
        }
        if self.suggested_headings:
            result["suggestedHeadings"] = list(self.suggested_headings)
        return result


@dataclass(frozen=True, slots=True)
class SectionHint:
    path: str
    headings: tuple[str, ...]
    sections: tuple[SectionLocation, ...] = ()

    def to_json(self) -> JsonObject:
        return {
            "path": self.path,
            "headings": list(self.headings),
            "sections": [item.to_json() for item in self.sections],
        }


@dataclass(frozen=True, slots=True)
class Finding:
    id: str
    severity: str
    path: str | None
    reason: str
    evidence: str
    recommended_action: str
    prohibited_auto_action: str

    def to_json(self) -> JsonObject:
        return {
            "id": self.id,
            "severity": self.severity,
            "path": self.path,
            "reason": self.reason,
            "evidence": self.evidence,
            "recommendedAction": self.recommended_action,
            "prohibitedAutoAction": self.prohibited_auto_action,
        }


@dataclass(frozen=True, slots=True)
class AuditOptions:
    root: Path | None
    config_path: Path | None
    output_format: str
    fail_on: str


@dataclass(frozen=True, slots=True)
class AuditResult:
    root: Path
    documents: tuple[DocumentInfo, ...]
    findings: tuple[Finding, ...]
    current_pointer_path: str | None
    missing_pointer_fields: tuple[str, ...]
    required_read_documents: tuple[str, ...]
    excluded_history: tuple[str, ...]
    excluded_non_sot: tuple[str, ...]
    section_hints: tuple[SectionHint, ...]
    checks: JsonObject
    oversized_hot_path_count: int
    current_gate: str | None
    next_task: str | None
    active_tasks: tuple[str, ...]

    def exit_code(self, fail_on: str) -> int:
        if fail_on == "never":
            return 0
        return 2 if any(item.severity == "blocking" for item in self.findings) else 0

    def to_json(self, exit_code: int) -> JsonObject:
        blocking = [item for item in self.findings if item.severity == "blocking"]
        warning = [item for item in self.findings if item.severity == "warning"]
        info = [item for item in self.findings if item.severity == "info"]
        return {
            "readOnlyDocumentAudit": {
                "schemaVersion": 1,
                "commandCandidate": "cdd-audit docs",
                "mode": "read-only",
                "root": str(self.root),
                "checkedAt": datetime.now(UTC).isoformat(),
                "exitCode": exit_code,
                "summary": {
                    "blockingCount": len(blocking),
                    "warningCount": len(warning),
                    "infoCount": len(info),
                    "requiredReadDocumentCount": len(self.required_read_documents),
                    "excludedDocumentCount": len(self.excluded_history) + len(self.excluded_non_sot),
                    "oversizedHotPathCount": self.oversized_hot_path_count,
                },
                "currentWorkPointer": {
                    "path": self.current_pointer_path,
                    "exists": self.current_pointer_path is not None,
                    "requiredFields": list(CURRENT_POINTER_FIELDS.keys()),
                    "missingFields": list(self.missing_pointer_fields),
                    "currentGate": self.current_gate,
                    "nextTask": self.next_task,
                    "activeTasks": list(self.active_tasks),
                },
                "readPathContract": {
                    "requiredReadDocuments": list(self.required_read_documents),
                    "sectionHints": [item.to_json() for item in self.section_hints],
                    "excludedHistoricalRecords": list(self.excluded_history),
                    "excludedNonSotReferences": list(self.excluded_non_sot),
                    "unknownRoleDocuments": [
                        item.path for item in self.documents if item.in_default_read_path and item.role == "unknown"
                    ],
                },
                "documents": [item.to_json() for item in self.documents],
                "checks": self.checks,
                "findings": [item.to_json() for item in self.findings],
                "prohibitedActions": list(PROHIBITED_ACTIONS),
            }
        }
