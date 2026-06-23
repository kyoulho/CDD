from __future__ import annotations

from typing import Final

from cdd_audit.model import EntrypointGuide, SectionHint

ENTRYPOINT_NAMES: Final[tuple[str, ...]] = (
    "start-here",
    "plan-task",
    "write-implementation-prompt",
    "cleanup-delete",
    "verify-work",
    "revise-work",
    "complete-work",
)

ENTRYPOINT_GUIDES: Final[dict[str, EntrypointGuide]] = {
    "start-here": EntrypointGuide(
        name="start-here",
        purpose="새 작업 시작과 라우팅",
        primary_documents=("start-here.md", "_work-mode.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("start-here.md", ("# Start Here Skill", "## 최소 읽기 경로", "## Routing Table", "## 즉시 적용할 규칙")),
            SectionHint("_work-mode.md", ("# Work Mode Gate Skill", "## 사용자 개입 필요 여부", "## 작업 모드")),
        ),
        expansion_documents=("_source-of-truth-manager.md", "_approval-reference.md"),
    ),
    "plan-task": EntrypointGuide(
        name="plan-task",
        purpose="작업 기준서 작성",
        primary_documents=("plan-task.md", "_readiness-gates.md", "_artifact-templates.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("plan-task.md", ("# Plan Task Skill", "## 최소 읽기 경로", "## 시작 조건", "## 작업 기준서 필수 항목")),
            SectionHint("_readiness-gates.md", ("# Readiness Gates", "## 제품 기준 준비 상태", "## 기술 설계 준비 상태", "## 구조 제안 전 의미 확인")),
        ),
        expansion_documents=("_source-of-truth-manager.md", "_approval-reference.md"),
    ),
    "write-implementation-prompt": EntrypointGuide(
        name="write-implementation-prompt",
        purpose="구현 지시서 작성",
        primary_documents=("write-implementation-prompt.md", "_implementation-rules.md", "_artifact-templates.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("write-implementation-prompt.md", ("# Write Implementation Prompt Skill", "## 최소 읽기 경로", "## 시작 조건", "## 금지 조건")),
            SectionHint("_implementation-rules.md", ("# Implementation Rules Module", "## 시작 조건", "## 구현 규칙", "## 임의 결정 금지 항목")),
        ),
        expansion_documents=("_readiness-gates.md", "_approval-reference.md"),
    ),
    "cleanup-delete": EntrypointGuide(
        name="cleanup-delete",
        purpose="삭제와 정리 판단",
        primary_documents=("cleanup-delete.md", "_authority-boundary.md", "_approval-reference.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("cleanup-delete.md", ("# Cleanup / Delete Playbook", "## 최소 읽기 경로", "## 작업 전 확인", "## 사람 확인 지점")),
            SectionHint("_authority-boundary.md", ("# Authority Boundary Skill", "## AI가 판단할 수 있는 것", "## AI가 임의 판단하면 안 되는 것")),
        ),
        expansion_documents=("_source-of-truth-manager.md",),
    ),
    "verify-work": EntrypointGuide(
        name="verify-work",
        purpose="작업 결과 검증",
        primary_documents=("verify-work.md", "_implementation-rules.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("verify-work.md", ("# Verify Work Skill", "## 최소 읽기 경로", "## 최소 guard checklist", "## 검증 항목")),
            SectionHint("_implementation-rules.md", ("# Implementation Rules Module", "## 구현 규칙", "## 충돌 발견 시 보고 형식")),
        ),
        expansion_documents=("_readiness-gates.md", "_approval-reference.md"),
    ),
    "revise-work": EntrypointGuide(
        name="revise-work",
        purpose="검증 실패 후 수정 지시",
        primary_documents=("revise-work.md", "verify-work.md", "_implementation-rules.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("revise-work.md", ("# Revise Work Skill", "## 최소 읽기 경로", "## 시작 조건", "## 중단 조건")),
            SectionHint("verify-work.md", ("# Verify Work Skill", "## 결과 상태", "## 다음 단계")),
        ),
        expansion_documents=("_approval-reference.md",),
    ),
    "complete-work": EntrypointGuide(
        name="complete-work",
        purpose="완료 기록과 완료 보고",
        primary_documents=("complete-work.md", "verify-work.md", "_artifact-templates.md", "_user-facing-language.md"),
        section_hints=(
            SectionHint("complete-work.md", ("# Complete Work Skill", "## 최소 읽기 경로", "## 완료 조건", "## 완료 기록에 포함할 내용")),
            SectionHint("verify-work.md", ("# Verify Work Skill", "## 결과 상태", "## User-Facing Reporting")),
        ),
        expansion_documents=("_approval-reference.md", "_source-of-truth-manager.md"),
    ),
}


def allowed_entrypoints() -> str:
    return ", ".join(ENTRYPOINT_NAMES)


def is_allowed_entrypoint(name: str) -> bool:
    return name in ENTRYPOINT_GUIDES


def entrypoint_guide(name: str | None) -> EntrypointGuide | None:
    if name is None:
        return None
    return ENTRYPOINT_GUIDES[name]
