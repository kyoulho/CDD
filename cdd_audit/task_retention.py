from __future__ import annotations

import re

from cdd_audit.config import TaskRetentionConfig
from cdd_audit.model import DocumentInfo, JsonObject

TASK_HEADING_PATTERN = re.compile(r"(?im)^#{1,4}\s+.*\bTASK[-_A-Z0-9]*\b.*$")
TASK_TOKEN_PATTERN = re.compile(r"\bTASK[-_A-Z0-9]*\b", re.IGNORECASE)
COMPLETE_PATTERN = re.compile(r"(?im)\b(status\s*[:=]\s*complete|완료|complete(?:d)?)\b")
TASK_ARTIFACT_PATH_SIGNALS = ("old-prompt", "prompt", "verification", "completion")
LEGACY_POLICY_SIGNALS = (
    "must",
    "required",
    "policy",
    "api",
    "db",
    "table",
    "column",
    "status",
    "enum",
    "권한",
    "정책",
    "저장",
    "상태",
    "api",
)


def task_rollup_candidates(
    docs: tuple[DocumentInfo, ...],
    retention: TaskRetentionConfig,
) -> list[JsonObject]:
    result: list[JsonObject] = []
    for item in docs:
        count = completed_task_count(item)
        if item.in_default_read_path and count > retention.recent_completed_task_limit:
            result.append(
                {
                    "path": item.path,
                    "completedTaskCount": count,
                    "limit": retention.recent_completed_task_limit,
                    "recommendedAction": "현재 기준으로 승격할 결정만 남기고 완료 TASK 전문은 version/milestone 요약으로 압축합니다.",
                }
            )
    return result


def completed_task_hot_path_candidates(docs: tuple[DocumentInfo, ...]) -> list[JsonObject]:
    result: list[JsonObject] = []
    for item in docs:
        count = completed_task_count(item)
        if item.in_default_read_path and count:
            result.append(
                {
                    "path": item.path,
                    "completedTaskCount": count,
                    "recommendedAction": "active에는 현재 작업, 다음 작업, 최근 완료 요약, 후속 의존성 요약만 남깁니다.",
                }
            )
    return result


def legacy_policy_history_candidates(docs: tuple[DocumentInfo, ...]) -> list[JsonObject]:
    result: list[JsonObject] = []
    for item in docs:
        if not item.in_default_read_path or not _is_task_history_artifact(item):
            continue
        if _has_legacy_policy_signal(item):
            result.append(
                {
                    "path": item.path,
                    "recommendedAction": "과거 TASK의 정책성 문구를 현재 기준으로 쓸지 승격/폐기/보류로 분류합니다.",
                }
            )
    return result


def task_artifact_prune_candidates(docs: tuple[DocumentInfo, ...]) -> list[JsonObject]:
    result: list[JsonObject] = []
    for item in docs:
        if _needs_task_artifact_prune(item):
            result.append(
                {
                    "path": item.path,
                    "reason": _task_artifact_prune_reason(item),
                    "recommendedAction": "요약으로 압축할지, 최소 보존할지, 삭제 후보로 둘지 사용자에게 브리핑합니다.",
                }
            )
    return result


def completed_task_count(item: DocumentInfo) -> int:
    sections = _task_sections(item)
    if sections:
        return sum(1 for section in sections if COMPLETE_PATTERN.search(section))
    if item.status == "COMPLETE" and TASK_TOKEN_PATTERN.search(item.text):
        return 1
    return 0


def _task_sections(item: DocumentInfo) -> list[str]:
    matches = list(TASK_HEADING_PATTERN.finditer(item.text))
    sections: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(item.text)
        sections.append(item.text[start:end])
    return sections


def _is_task_history_artifact(item: DocumentInfo) -> bool:
    path = item.path.lower()
    return item.role == "history" or any(token in path for token in TASK_ARTIFACT_PATH_SIGNALS)


def _has_legacy_policy_signal(item: DocumentInfo) -> bool:
    return TASK_TOKEN_PATTERN.search(item.text) is not None and any(signal in item.text_lower for signal in LEGACY_POLICY_SIGNALS)


def _needs_task_artifact_prune(item: DocumentInfo) -> bool:
    path = item.path.lower()
    if not item.in_default_read_path:
        return False
    if not any(signal in path for signal in TASK_ARTIFACT_PATH_SIGNALS):
        return False
    return TASK_TOKEN_PATTERN.search(item.text) is not None


def _task_artifact_prune_reason(item: DocumentInfo) -> str:
    if item.lines > 100:
        return f"{item.lines} lines task artifact in hot path"
    return "task artifact is in hot path"
