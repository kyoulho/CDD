from __future__ import annotations

from cdd_audit.model import AuditResult, JsonValue


def brief_task_cleanup_lines(result: AuditResult) -> list[str]:
    lines = task_cleanup_lines(result)
    if lines == ["- 없음"]:
        return []
    return ["", "TASK 정리 후보:", *lines]


def task_cleanup_lines(result: AuditResult) -> list[str]:
    retention = result.checks.get("taskRetention")
    if not isinstance(retention, dict):
        return ["- 없음"]
    lines: list[str] = []
    _append_rollup_lines(lines, retention.get("rollupCandidates"))
    _append_legacy_lines(lines, retention.get("legacyPolicyInTaskHistory"))
    _append_prune_lines(lines, retention.get("pruneCandidates"))
    return lines or ["- 없음"]


def _append_rollup_lines(lines: list[str], value: JsonValue | None) -> None:
    if not isinstance(value, list):
        return
    for item in value:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        count = item.get("completedTaskCount")
        limit = item.get("limit")
        if isinstance(path, str):
            lines.append(f"- {path}: 완료 TASK {count}개가 active 기준 {limit}개를 넘었습니다.")
            lines.append("  추천: 현재 기준으로 승격할 결정과 요약/보존/삭제 후보를 분류합니다.")


def _append_legacy_lines(lines: list[str], value: JsonValue | None) -> None:
    if not isinstance(value, list):
        return
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            lines.append(f"- {item['path']}: 과거 TASK 정책이 현재 기준처럼 읽힐 수 있습니다.")
            lines.append("  추천: 기준 승격 / history 제외 / 삭제 후보 / 보류 중 하나로 분류합니다.")


def _append_prune_lines(lines: list[str], value: JsonValue | None) -> None:
    if not isinstance(value, list):
        return
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            reason = item.get("reason")
            lines.append(f"- {item['path']}: {reason}")
            lines.append("  추천: 전문 보존 대신 version/milestone 요약 또는 최소 보존 후보로 검토합니다.")
