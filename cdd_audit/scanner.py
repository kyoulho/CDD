from __future__ import annotations

from pathlib import Path

from cdd_audit.checks import (
    checks_json,
    decision_log_unpartitioned,
    has_active_history_mix,
    oversized_hot_path,
    sot_entrypoint_too_detailed,
)
from cdd_audit.config import AuditConfig
from cdd_audit.documents import read_documents
from cdd_audit.model import ACCUMULATED_LINES, SEVERITY_ORDER, AuditResult, DocumentInfo, Finding
from cdd_audit.pointer import missing_pointer_fields, pointer_details


def audit(root: Path, config: AuditConfig) -> AuditResult:
    docs = tuple(read_documents(root, config))
    pointer = _current_pointer(docs, config)
    missing = missing_pointer_fields(pointer)
    details = pointer_details(pointer)
    required = _required_documents(docs, config, details.required_read_documents)
    excluded_history = _excluded_history(config, details.excluded_historical_records)
    excluded_non_sot = _excluded_non_sot(config, details.excluded_non_sot_references)
    checks = checks_json(docs)
    oversized_count = len(oversized_hot_path(docs))
    findings = tuple(_sorted_findings(_findings(docs, pointer, missing, excluded_history, excluded_non_sot)))
    return AuditResult(
        root=root,
        documents=docs,
        findings=findings,
        current_pointer_path=pointer.path if pointer else None,
        missing_pointer_fields=missing,
        required_read_documents=required,
        excluded_history=excluded_history,
        excluded_non_sot=excluded_non_sot,
        checks=checks,
        oversized_hot_path_count=oversized_count,
        current_gate=details.current_gate,
        next_task=details.next_task,
        active_tasks=details.active_tasks,
    )


def _current_pointer(docs: tuple[DocumentInfo, ...], config: AuditConfig) -> DocumentInfo | None:
    candidates = []
    if config.current_work_pointer is not None:
        candidates.extend(item for item in docs if item.path == config.current_work_pointer)
    candidates.extend(item for item in docs if "current-work" in item.path.lower())
    candidates.extend(item for item in docs if item.path in {"docs/README.md", "README.md"})
    for item in candidates:
        if len(missing_pointer_fields(item)) < 4:
            return item
    return None


def _required_documents(
    docs: tuple[DocumentInfo, ...],
    config: AuditConfig,
    pointer_required: tuple[str, ...],
) -> tuple[str, ...]:
    if pointer_required:
        return pointer_required
    if config.required_read_documents:
        return config.required_read_documents
    return tuple(item.path for item in docs if item.in_default_read_path)


def _excluded_history(config: AuditConfig, pointer_excluded: tuple[str, ...]) -> tuple[str, ...]:
    if pointer_excluded:
        return pointer_excluded
    return config.excluded_historical_records


def _excluded_non_sot(config: AuditConfig, pointer_excluded: tuple[str, ...]) -> tuple[str, ...]:
    if pointer_excluded:
        return pointer_excluded
    return config.excluded_non_sot_references


def _findings(
    docs: tuple[DocumentInfo, ...],
    pointer: DocumentInfo | None,
    missing_fields: tuple[str, ...],
    excluded_history: tuple[str, ...],
    excluded_non_sot: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    oversized = oversized_hot_path(docs)
    mixed = [item for item in docs if item.in_default_read_path and has_active_history_mix(item)]
    needs_pointer = bool(oversized or mixed)
    if needs_pointer and pointer is None:
        findings.append(_finding("CURRENT_WORK_POINTER_MISSING", "blocking", None, "문서가 커졌거나 active/history가 섞였지만 현재 작업 포인터가 없습니다.", "current work pointer not detected", "현재 작업 포인터 역할을 만들거나 기존 index에 추가합니다.", "autoDeclareCurrentCriteria"))
    if pointer is not None and missing_fields:
        severity = "blocking" if needs_pointer else "warning"
        findings.append(_finding("CURRENT_WORK_POINTER_INCOMPLETE", severity, pointer.path, "현재 작업 포인터 필드가 부족합니다.", ", ".join(missing_fields), "누락 필드를 채웁니다.", "autoModifyReadmeOrIndexWithoutApproval"))
    if needs_pointer and ("requiredReadDocuments" in missing_fields or "excludedHistoricalRecords" in missing_fields):
        findings.append(_finding("READ_PATH_CONTRACT_MISSING", "blocking", pointer.path if pointer else None, "반드시 읽을 문서와 제외할 기록이 분리되어 있지 않습니다.", ", ".join(missing_fields), "기본 읽기 경로 계약을 명시합니다.", "autoDeclareCurrentCriteria"))
    findings.extend(_size_and_mix_findings(docs, oversized, mixed))
    findings.extend(_classification_findings(docs, excluded_history, excluded_non_sot))
    if findings:
        findings.append(_finding("README_INDEX_UPDATE_REQUIRED", "info", None, "문서 배치나 읽기 경로 변경 시 README/index 갱신 여부 확인이 필요합니다.", "audit produced document-structure findings", "수정 전 보고에 README/index 갱신 필요 여부를 포함합니다.", "autoModifyReadmeOrIndexWithoutApproval"))
    return findings


def _size_and_mix_findings(
    docs: tuple[DocumentInfo, ...],
    oversized: list[DocumentInfo],
    mixed: list[DocumentInfo],
) -> list[Finding]:
    findings: list[Finding] = []
    for item in oversized:
        findings.append(_finding("HOT_PATH_OVERSIZED", "warning", item.path, "기본 읽기 경로 문서가 400줄 또는 40KB를 넘습니다.", f"{item.lines} lines, {item.bytes_size} bytes", "분리 후보 또는 유지 근거를 보고합니다.", "autoSplitFiles"))
    for item in docs:
        if item.lines >= ACCUMULATED_LINES:
            findings.append(_finding("ACCUMULATED_HISTORY_OVERSIZED", "warning", item.path, "누적 문서가 1000줄 이상입니다.", f"{item.lines} lines", "active index와 history 분리를 검토합니다.", "autoSplitFiles"))
        if item in mixed:
            findings.append(_finding("ACTIVE_HISTORY_MIXED", "blocking", item.path, "현재 task와 과거 기록이 기본 읽기 경로에서 섞여 있습니다.", ", ".join(item.signals), "active index와 history를 분리합니다.", "autoSplitFiles"))
        if sot_entrypoint_too_detailed(item):
            findings.append(_finding("SOT_ENTRYPOINT_TOO_DETAILED", "warning", item.path, "기준 진입점이 원칙과 index보다 세부 작업 기록처럼 커졌습니다.", f"{item.lines} lines, {item.bytes_size} bytes", "기준 문서는 얇은 진입점으로 유지하고 세부 기준은 domain packet 후보로 보고합니다.", "autoSplitFiles"))
        if decision_log_unpartitioned(item):
            findings.append(_finding("DECISION_LOG_UNPARTITIONED", "warning", item.path, "decision log가 current/recent/history/superseded로 나뉘지 않았을 수 있습니다.", ", ".join(item.signals) or f"{item.lines} lines", "현재 적용 결정과 과거 결정을 분리할 후보로 보고합니다.", "autoSplitFiles"))
    return findings


def _classification_findings(
    docs: tuple[DocumentInfo, ...],
    excluded_history: tuple[str, ...],
    excluded_non_sot: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    for item in docs:
        if item.in_default_read_path and item.role == "non-sot-reference":
            findings.append(_finding("NON_SOT_IN_READ_PATH", "blocking", item.path, "비-SOT 자료가 기본 읽기 경로에 있습니다.", ", ".join(item.signals), "보조 자료로 분리하고 기본 읽기 경로에서 제외합니다.", "autoPromoteHistoryToCurrentCriteria"))
        if item.in_default_read_path and item.role == "unknown":
            findings.append(_finding("UNKNOWN_DOCUMENT_ROLE", "warning", item.path, "기본 읽기 경로 문서의 역할을 판단할 근거가 부족합니다.", item.path, "current/history/non-SOT 중 어떤 역할인지 index나 문서에 명시합니다.", "autoDeclareCurrentCriteria"))
    if not excluded_history and any(item.role == "history" for item in docs):
        findings.append(_finding("READ_PATH_CONTRACT_MISSING", "warning", None, "과거 기록 제외 목록이 명확하지 않습니다.", "history documents exist", "기본 읽기 경로 계약에 제외 목록을 기록합니다.", "autoDeclareCurrentCriteria"))
    if not excluded_non_sot and any(item.role == "non-sot-reference" for item in docs):
        findings.append(_finding("READ_PATH_CONTRACT_MISSING", "warning", None, "보조 자료 제외 목록이 명확하지 않습니다.", "non-SOT references exist", "비-SOT 자료 제외 목록을 기록합니다.", "autoDeclareCurrentCriteria"))
    return findings


def _finding(id_value: str, severity: str, path: str | None, reason: str, evidence: str, action: str, prohibited: str) -> Finding:
    return Finding(id_value, severity, path, reason, evidence, action, prohibited)


def _sorted_findings(findings: list[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda item: (SEVERITY_ORDER[item.severity], item.id, item.path or ""))
