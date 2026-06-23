from __future__ import annotations

from pathlib import Path
from typing import Final

from cdd_audit.config import empty_config
from cdd_audit.documents import read_documents
from cdd_audit.model import EntrypointGuide, SectionHint
from cdd_audit.section_hints import located_section_hint

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
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 기본 사용자 보고 형식", "## 응답 종료 형식")),
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
            SectionHint("_artifact-templates.md", ("# Artifact Templates V2.1", "## Document Placement Check Template", "## Task Contract Template")),
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 승인 전 브리핑 형식", "## 문서 정합성 / 분리 검토 보고 형식")),
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
            SectionHint("_artifact-templates.md", ("# Artifact Templates V2.1", "## 5. Prompt Artifact Template", "## Document Placement Check Template")),
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 승인 전 브리핑 형식", "## 기본 사용자 보고 금지 표현")),
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
            SectionHint("_approval-reference.md", ("# Approval Reference Standard", "## 승인 요청 전 브리핑", "## 확인 질문 예시")),
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 사용자 개입 필요 여부 판정", "## 응답 종료 형식")),
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
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 기본 사용자 보고 형식", "## 내부 진단표 기본 노출 금지")),
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
            SectionHint("_implementation-rules.md", ("# Implementation Rules Module", "## 충돌 발견 시 보고 형식", "## 완료 보고")),
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 응답 종료 형식", "## 권장 표현")),
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
            SectionHint("_artifact-templates.md", ("# Artifact Templates V2.1", "## 6. Verification Result Metadata Template", "## Completion Report Example")),
            SectionHint("_user-facing-language.md", ("# User-Facing Language Layer", "## 완료한 경우", "## 사용자 보고와 내부 보고 분리")),
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


def located_entrypoint_guide(name: str | None, skill_root: Path | None = None) -> EntrypointGuide | None:
    guide = entrypoint_guide(name)
    if guide is None:
        return None
    root = skill_root or Path(__file__).resolve().parents[1]
    documents = {item.path: item for item in read_documents(root, empty_config())}
    return EntrypointGuide(
        name=guide.name,
        purpose=guide.purpose,
        primary_documents=guide.primary_documents,
        section_hints=tuple(located_section_hint(item, documents.get(item.path)) for item in guide.section_hints),
        expansion_documents=guide.expansion_documents,
    )
