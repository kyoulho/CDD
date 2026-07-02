from __future__ import annotations

from cdd_audit.config import TaskRetentionConfig
from cdd_audit.model import DocumentInfo, Finding
from cdd_audit.task_retention import (
    completed_task_hot_path_candidates,
    legacy_policy_history_candidates,
    task_artifact_prune_candidates,
    task_rollup_candidates,
)


def task_retention_findings(
    docs: tuple[DocumentInfo, ...],
    retention: TaskRetentionConfig,
) -> list[Finding]:
    findings: list[Finding] = []
    for candidate in task_rollup_candidates(docs, retention):
        path = candidate["path"]
        count = candidate["completedTaskCount"]
        limit = candidate["limit"]
        assert isinstance(path, str)
        findings.append(
            Finding(
                "TASK_ROLLUP_DUE",
                "warning",
                path,
                "기본 읽기 경로에 완료 TASK 전문이 기준보다 많이 남아 있습니다.",
                f"{count} completed tasks, limit {limit}",
                "현재 기준으로 승격할 결정, 요약으로 압축할 기록, 최소 보존할 기록, 삭제 후보를 분류합니다.",
                "autoDeleteStaleDocs",
            )
        )
    for candidate in completed_task_hot_path_candidates(docs):
        path = candidate["path"]
        count = candidate["completedTaskCount"]
        assert isinstance(path, str)
        findings.append(
            Finding(
                "COMPLETED_TASK_IN_HOT_PATH",
                "warning",
                path,
                "완료 TASK 전문이 기본 읽기 경로에 남아 있습니다.",
                f"{count} completed tasks in hot path",
                "active에는 현재 작업, 다음 작업, 최근 완료 요약, 후속 의존성 요약만 남기는 방안을 보고합니다.",
                "autoSplitFiles",
            )
        )
    for candidate in legacy_policy_history_candidates(docs):
        path = candidate["path"]
        assert isinstance(path, str)
        findings.append(
            Finding(
                "LEGACY_POLICY_IN_TASK_HISTORY",
                "blocking",
                path,
                "과거 TASK 문서의 정책성 문구가 현재 기준처럼 기본 읽기 경로에 노출되어 있습니다.",
                "legacy task policy is in default read path",
                "현재 기준으로 승격할지, history로 제외할지, 삭제 후보로 둘지 사용자 확인을 받습니다.",
                "autoPromoteHistoryToCurrentCriteria",
            )
        )
    for candidate in task_artifact_prune_candidates(docs):
        path = candidate["path"]
        reason = candidate["reason"]
        assert isinstance(path, str)
        findings.append(
            Finding(
                "TASK_ARTIFACT_PRUNE_CANDIDATE",
                "info",
                path,
                "old prompt, verification, completion 전문이 기본 읽기 경로에 남아 있습니다.",
                str(reason),
                "요약 압축, 최소 보존, 삭제 후보, 보류 중 하나로 분류하는 브리핑을 만듭니다.",
                "autoDeleteStaleDocs",
            )
        )
    return findings
