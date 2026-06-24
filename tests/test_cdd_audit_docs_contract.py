from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tests = [
        test_cdd_audit_path_fallback_is_user_optional,
        test_user_facing_examples_are_discoverable_from_main_rule,
        test_user_facing_work_mode_examples_are_split_from_hot_path,
        test_follow_up_approval_briefing_blocks_bare_action_lists,
        test_self_verification_command_is_standardized,
        test_forward_testing_covers_briefing_and_environment_regressions,
        test_cdd_commands_do_not_write_python_bytecode,
        test_cdd_audit_warning_gate_is_documented,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} docs contract tests passed")


def test_cdd_audit_path_fallback_is_user_optional() -> None:
    required = {
        "SKILL.md": ("PATH 등록은 사람의 편의용 선택 사항", "<cdd-root>/bin/cdd-audit"),
        "README.md": ("PATH에 직접 등록해야 CDD를 쓸 수 있는 것은 아니다", "<cdd-root>/bin/cdd-audit"),
        "start-here.md": ("사용자가 `cdd-audit`를 PATH에 등록했다고 가정하지", "<cdd-root>/bin/cdd-audit"),
        "plan-task.md": ("사용자가 PATH를 설정했다고 가정하지", "bin/cdd-audit"),
        "write-implementation-prompt.md": ("사용자가 PATH를 설정했다고 가정하지", "bin/cdd-audit"),
        "_source-of-truth-manager.md": ("사용자에게 설치를 요구하지 않는다", "<cdd-root>/bin/cdd-audit"),
    }
    for path, snippets in required.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for snippet in snippets:
            assert snippet in text, path


def test_user_facing_examples_are_discoverable_from_main_rule() -> None:
    text = (ROOT / "_user-facing-language.md").read_text(encoding="utf-8")
    reference = (ROOT / "references/user-facing-report-examples.md").read_text(encoding="utf-8")

    assert "## 대표 응답 3종" in text
    assert "references/user-facing-report-examples.md" in text
    assert "## 1. 아직 진행하면 안 되는 경우" in reference
    assert "## 2. 사용자 개입 없이 진행 가능한 경우" in reference
    assert "## 3. 완료한 경우" in reference


def test_user_facing_work_mode_examples_are_split_from_hot_path() -> None:
    text = (ROOT / "_user-facing-language.md").read_text(encoding="utf-8")
    split = (ROOT / "_user-facing-work-modes.md").read_text(encoding="utf-8")
    briefing = (ROOT / "_approval-briefing-language.md").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "_user-facing-work-modes.md" in text
    assert "- `_user-facing-work-modes.md`" in skill
    assert "_approval-briefing-language.md" in text
    assert "- `_approval-briefing-language.md`" in skill
    assert len(text.splitlines()) < 850
    assert "## Project Context 질문 표현" not in text
    assert "## Project Context 질문 표현" in split
    assert "## 승인 전 브리핑 형식" not in text
    assert "## 승인 전 브리핑 형식" in briefing
    assert "## ANALYSIS_ONLY" in split
    assert "## PATCH_AUTHORIZED" in split


def test_follow_up_approval_briefing_blocks_bare_action_lists() -> None:
    text = (ROOT / "_user-facing-language.md").read_text(encoding="utf-8")
    briefing = (ROOT / "_approval-briefing-language.md").read_text(encoding="utf-8")
    approval = (ROOT / "_approval-reference.md").read_text(encoding="utf-8")
    complete = (ROOT / "complete-work.md").read_text(encoding="utf-8")
    work_mode = (ROOT / "_work-mode.md").read_text(encoding="utf-8")

    for snippet in (
        "이번 승인의 목적",
        "현재 기준",
        "포함되는 것",
        "제외되는 것",
        "승인하면 고정되는 결정",
        "주의할 점",
        "승인 후 내가 진행할 일",
        "바로 답할 수 있는 문장",
    ):
        assert snippet in briefing
        assert snippet in complete

    assert "승인 여부를 판단하는 검토 표면" in briefing
    assert "사람도 과거 task 히스토리와 현재 기준을 모두 기억하지 못할 수 있으므로" in briefing
    assert "사람이 과거 작업 흐름을 기억하지 않아도 승인 범위를 판단" in approval
    assert "같은 다음 작업 요청을 반복해도 브리핑을 승인 문장 중심으로 축약하지 않는다" in briefing
    assert "반복된 같은 요청이어도 브리핑 필수 항목을 승인 문장만 남기는 방식으로 줄이지 않는다" in work_mode
    assert "반복 요청이라는 이유로 \"승인 대상은 하나입니다\"와 승인 문장만 남기고" in briefing
    assert "일반 사용자 보고에서 `PROMPT_DRAFT_APPROVAL`, `PROMPT_EXECUTION_APPROVAL`, `PATCH_APPROVAL`, `APPLY_APPROVAL` 같은 내부 approval enum" in briefing
    assert "구현 지시서 초안 작성 승인 요청" in briefing
    assert "구현 지시서에 담길 주요 섹션" in briefing
    assert "각 섹션에서 고정할 판단" in briefing
    assert "구현자에게 금지할 행동" in briefing
    assert "초안 작성 중 다시 멈출 조건" in briefing
    assert "승인하면 내가 진행할 일\"만 나열하는 것은 승인 전 브리핑이 아니다" in approval
    assert "승인하면 내가 진행할 일:\" 또는 \"승인하면 진행할 일:\"만 나열" in briefing
    assert "일반 선택지 목록을 승인 전 브리핑 대신 사용할 수 없다" in approval
    assert "현재 포인터가 단일 다음 task를 가리키는데 \"선택지\" 목록을 먼저 보여주고 승인 대상 브리핑을 생략" in briefing
    assert "나쁜 예:" in briefing
    assert "좋은 예:" in briefing


def test_self_verification_command_is_standardized() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "./bin/cdd-verify" in readme
    assert "python3.12 tests/test_cdd_audit.py" not in readme
    assert "표준 자체 검증" in skill
    assert "bin/cdd-verify" in skill


def test_forward_testing_covers_briefing_and_environment_regressions() -> None:
    forward = (ROOT / "references/forward-testing.md").read_text(encoding="utf-8")

    assert "구현 지시서 초안 승인 브리핑" in forward
    assert "구현 지시서를 어떻게 작성할지" in forward
    assert "검증 환경이 PATH 또는 Python 버전에 의존하는 경우" in forward
    assert "bin/cdd-verify" in forward


def test_cdd_commands_do_not_write_python_bytecode() -> None:
    for path in ("bin/cdd-audit", "bin/cdd-test", "bin/cdd-verify"):
        text = (ROOT / path).read_text(encoding="utf-8")

        assert "PYTHONDONTWRITEBYTECODE=1" in text, path


def test_cdd_audit_warning_gate_is_documented() -> None:
    required = {
        "SKILL.md": ("warning은 무시하지 않는다", "해결 / 보류 / 진행 사유"),
        "README.md": ("주의 항목은 조용히 무시하지 않는다", "주의 항목 처리"),
        "start-here.md": ("warning을 조용히 무시하지 않는다", "해결 / 보류 / 진행 사유"),
        "_source-of-truth-manager.md": ("warning은 무시하지 않는다", "해결 / 보류 / 진행 사유"),
    }
    for path, snippets in required.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for snippet in snippets:
            assert snippet in text, path


if __name__ == "__main__":
    main()
