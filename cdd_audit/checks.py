from __future__ import annotations

from pathlib import Path

from cdd_audit.model import (
    ACCUMULATED_LINES,
    ACTIVE_SIGNALS,
    HISTORY_SIGNALS,
    HOT_PATH_BYTES,
    HOT_PATH_LINES,
    DocumentInfo,
    JsonObject,
)
from cdd_audit.skill_health import skill_health


def has_active_history_mix(item: DocumentInfo) -> bool:
    if "current-work" in item.path.lower():
        return False
    has_active = any(signal in ACTIVE_SIGNALS for signal in item.signals)
    has_history_path = any(signal in item.path.lower() for signal in HISTORY_SIGNALS)
    has_history = item.role == "history" or has_history_path or item.status in {"COMPLETE", "SUPERSEDED"}
    return has_active and has_history


def oversized_hot_path(docs: tuple[DocumentInfo, ...]) -> list[DocumentInfo]:
    return [item for item in docs if item.in_default_read_path and (item.lines > HOT_PATH_LINES or item.bytes_size > HOT_PATH_BYTES)]


def split_recommendations(docs: tuple[DocumentInfo, ...]) -> list[JsonObject]:
    return [_split_recommendation(item) for item in docs if _needs_split_recommendation(item)]


def _needs_split_recommendation(item: DocumentInfo) -> bool:
    if not item.in_default_read_path:
        return False
    oversized = item.lines > HOT_PATH_LINES or item.bytes_size > HOT_PATH_BYTES
    return oversized or item.lines >= ACCUMULATED_LINES or sot_entrypoint_too_detailed(item) or decision_log_unpartitioned(item)


def _split_recommendation(item: DocumentInfo) -> JsonObject:
    reason = f"{item.lines} lines, {item.bytes_size} bytes"
    if item.role == "task-contract":
        return {
            "path": item.path,
            "role": item.role,
            "reason": reason,
            "recommendedStructure": "현재 진행 가능한 task만 active index에 남기고 완료/검증/과거 task는 history로 분리합니다.",
            "keepInEntrypoint": "현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서",
            "moveToPacketOrHistory": "완료된 task, 과거 구현 지시서, 검증 결과, 완료 기록",
            "readmeOrIndexUpdateRequired": True,
        }
    if item.role == "current-criteria":
        return {
            "path": item.path,
            "role": item.role,
            "reason": reason,
            "recommendedStructure": "기준 문서는 얇은 진입점으로 유지하고 세부 기준 packet을 분리합니다.",
            "keepInEntrypoint": "현재 적용 원칙, 승인된 packet index, 반드시 읽을 최소 기준",
            "moveToPacketOrHistory": "화면/도메인/기능별 세부 기준, 과거 결정, 완료된 phase 설명",
            "readmeOrIndexUpdateRequired": True,
        }
    if item.role == "active-index":
        return {
            "path": item.path,
            "role": item.role,
            "reason": reason,
            "recommendedStructure": "현재 작업 포인터는 짧게 유지하고 상세 작업 기록은 별도 task/history 문서로 내립니다.",
            "keepInEntrypoint": "현재 gate, 다음 task, active task, required/excluded read path",
            "moveToPacketOrHistory": "완료 기록, 긴 검증 로그, 과거 task 설명",
            "readmeOrIndexUpdateRequired": True,
        }
    return {
        "path": item.path,
        "role": item.role,
        "reason": reason,
        "recommendedStructure": "자주 읽는 요약은 entrypoint에 남기고 상세 내용은 packet 또는 history로 분리합니다.",
        "keepInEntrypoint": "현재 판단에 매번 필요한 요약과 링크",
        "moveToPacketOrHistory": "반복해서 읽을 필요가 없는 세부 기록",
        "readmeOrIndexUpdateRequired": True,
    }


def sot_entrypoint_too_detailed(item: DocumentInfo) -> bool:
    if item.role != "current-criteria" or not item.in_default_read_path:
        return False
    too_large = item.lines > HOT_PATH_LINES or item.bytes_size > HOT_PATH_BYTES
    has_history = any(signal in HISTORY_SIGNALS for signal in item.signals)
    return too_large or has_history


def decision_log_unpartitioned(item: DocumentInfo) -> bool:
    path = item.path.lower()
    if not any(token in path for token in ("decision", "adr", "log")):
        return False
    partitioned = all(token in item.text_lower for token in ("current", "history", "superseded"))
    return not partitioned and (item.lines > HOT_PATH_LINES or any(signal in HISTORY_SIGNALS for signal in item.signals))


def checks_json(root: Path, docs: tuple[DocumentInfo, ...]) -> JsonObject:
    split_candidates = split_recommendations(docs)
    return {
        "readCost": {
            "oversizedHotPathDocuments": [item.path for item in oversized_hot_path(docs)],
            "accumulatedDocumentsOver1000Lines": [item.path for item in docs if item.lines >= ACCUMULATED_LINES],
        },
        "activeHistorySeparation": {
            "mixedDocuments": [item.path for item in docs if item.in_default_read_path and has_active_history_mix(item)],
            "activeIndexCandidates": [item.path for item in docs if item.role == "active-index"],
            "historyCandidates": [item.path for item in docs if item.role == "history"],
        },
        "sotEntryPoints": {
            "productSotTooDetailedCandidates": [
                item.path for item in docs if "product" in item.path.lower() and sot_entrypoint_too_detailed(item)
            ],
            "engineeringSotTooDetailedCandidates": [
                item.path for item in docs if "engineering" in item.path.lower() and sot_entrypoint_too_detailed(item)
            ],
            "domainPacketCandidates": [item.path for item in docs if sot_entrypoint_too_detailed(item)],
        },
        "decisionLog": {
            "currentDecisionCandidates": [
                item.path for item in docs if "current" in item.text_lower and "decision" in item.path.lower()
            ],
            "recentDecisionCandidates": [
                item.path for item in docs if "recent" in item.text_lower and "decision" in item.path.lower()
            ],
            "historyCandidates": [
                item.path for item in docs if "history" in item.text_lower and "decision" in item.path.lower()
            ],
            "supersededCandidates": [
                item.path for item in docs if "superseded" in item.text_lower and "decision" in item.path.lower()
            ],
        },
        "nonSotReferences": {
            "leakedIntoReadPath": [
                item.path for item in docs if item.in_default_read_path and item.role == "non-sot-reference"
            ],
        },
        "documentStructure": {
            "splitCandidates": split_candidates,
        },
        "indexMaintenance": {
            "readmeOrIndexUpdatesRequired": [str(item["path"]) for item in split_candidates],
        },
        "skillHealth": skill_health(root).to_json(),
    }
