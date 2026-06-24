from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tests = [
        test_cdd_audit_path_fallback_is_user_optional,
        test_user_facing_examples_are_discoverable_from_main_rule,
        test_user_facing_work_mode_examples_are_split_from_hot_path,
        test_follow_up_approval_briefing_blocks_bare_action_lists,
        test_combined_task_contract_and_prompt_draft_approval_requires_two_briefings,
        test_prompt_briefing_execution_approval_can_continue_without_second_stop,
        test_self_verification_command_is_standardized,
        test_forward_testing_covers_briefing_and_environment_regressions,
        test_cdd_commands_do_not_write_python_bytecode,
        test_cdd_audit_warning_gate_is_documented,
        test_gate_terms_are_hidden_in_user_facing_reports,
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


def test_combined_task_contract_and_prompt_draft_approval_requires_two_briefings() -> None:
    briefing = (ROOT / "_approval-briefing-language.md").read_text(encoding="utf-8")
    plan = (ROOT / "plan-task.md").read_text(encoding="utf-8")
    approval = (ROOT / "_approval-reference.md").read_text(encoding="utf-8")

    for text in (briefing, plan, approval):
        assert "몇 번째 승인 요청이든" in text
        assert "브리핑 없이 승인 요청 금지" in text
        assert "작업 기준서 승인과 구현 지시서 초안 작성 승인을 한 문장으로 묶는 경우" in text
        assert "두 개의 승인 대상" in text
        assert "작업 기준서 승인 브리핑" in text
        assert "구현 지시서 초안 작성 브리핑" in text
        assert "결합 승인 문장만" in text

    assert "작업 기준서가 무엇을 고정하는지" in briefing
    assert "구현 지시서를 어떻게 작성할지" in briefing


def test_prompt_briefing_execution_approval_can_continue_without_second_stop() -> None:
    approval = (ROOT / "_approval-reference.md").read_text(encoding="utf-8")
    briefing = (ROOT / "_approval-briefing-language.md").read_text(encoding="utf-8")
    implementation_prompt = (ROOT / "write-implementation-prompt.md").read_text(encoding="utf-8")
    user_facing = (ROOT / "_user-facing-language.md").read_text(encoding="utf-8")

    assert "구현 지시서 브리핑 후에 사용자가 구현까지 승인했다면" in approval
    assert "브리핑 승인 후 실행 연계" in approval
    assert "초안 작성 후 실행 연계" not in approval
    assert "초안 작성만 승인받은 경우에는 실행 승인으로 해석하지 않는다" in approval
    assert "`구현 지시서 초안 작성을 승인합니다`, `브리핑 확인했습니다`, `다음 단계 진행`, `진행 후보 확인` 같은 표현은 실제 실행 승인으로 보지 않는다" in approval
    assert "구현 지시서 초안 작성과 실제 구현을 함께 승인합니다" in approval
    assert "승인 문장이 구현 지시서 초안 작성만 허용하고 실제 실행을 허용하지 않았다" in approval
    assert "실제 실행 승인 문장에는 구현, 문서 수정, cleanup/delete 실행, revision 실행 중 무엇을 허용하는지 명시되어야 한다" in approval
    assert "`구현 지시서 초안 작성을 승인합니다`는 초안 작성만 허용한다" in briefing
    assert "사용자가 실제 실행까지 승인했고 새로 결정할 사항이 없습니다." in approval
    assert "사용자가 실제 실행까지 승인했고 새로 결정할 사항이 없습니다." in implementation_prompt
    assert "사용자가 실제 실행까지 승인했고 새로 결정할 사항이 없습니다." in user_facing
    assert "작업 지시서는 내부 실행 기준으로 작성하고, 새로 결정할 사항이 없으므로 같은 요청 범위 안에서 바로 실행합니다." not in approval
    assert "작업 지시서는 내부 실행 기준으로 작성하고, 새로 결정할 사항이 없으므로 같은 요청 범위 안에서 바로 실행합니다." not in implementation_prompt
    assert "작업 지시서는 내부 실행 기준으로 작성하고, 새로 결정할 사항이 없으므로 같은 요청 범위 안에서 바로 실행합니다." not in user_facing
    assert "구현 지시서 브리핑 후 사용자가 실제 구현까지 승인했고" in implementation_prompt
    assert "사용자가 구현 지시서 초안 작성만 승인했고 실제 실행은 승인하지 않았다" in implementation_prompt
    assert "`구현 지시서 초안 작성을 승인합니다`, `브리핑 확인`, `다음 단계 진행`은 실제 실행 승인으로 승격하지 않는다" in implementation_prompt
    assert "구현 지시서 브리핑 후 사용자가 실제 구현까지 승인했고 새 미확정 결정이나 위험 변경이 없으면" in user_facing
    assert "구현 지시서 초안 작성만 승인받았고 실제 실행 승인은 받지 않았다" in user_facing
    assert "조회형 응답의 \"진행하려면 이렇게 말할 수 있습니다\" 문장은 진행 후보를 안내하는 선택 문장이지 실제 실행 승인 요청이 아니다" in user_facing


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


def test_gate_terms_are_hidden_in_user_facing_reports() -> None:
    user_facing = (ROOT / "_user-facing-language.md").read_text(encoding="utf-8")
    briefing = (ROOT / "_approval-briefing-language.md").read_text(encoding="utf-8")
    complete = (ROOT / "complete-work.md").read_text(encoding="utf-8")
    implementation_prompt = (ROOT / "write-implementation-prompt.md").read_text(encoding="utf-8")

    assert "일반 사용자 보고에서 `gate`를 상태명이나 제목으로 쓰지 않는다" in user_facing
    assert "| current gate / 현재 gate | 현재 상태 |" in user_facing
    assert "| next gate / 다음 gate | 다음 단계 / 다음에 필요한 승인 |" in user_facing
    assert "| gate passed / gate 통과 | 기준 충족 |" in user_facing
    assert "| gate blocked / gate 차단 | 아직 진행하면 안 됨 |" in user_facing
    assert "| readiness gate | 진행 전 확인 기준 |" in user_facing
    assert "현재 작업 포인터:\n- 위치:\n- 현재 상태:" in user_facing
    assert "현재 gate`, `다음 gate`, `gate 통과`, `gate 차단`, `readiness gate`" in briefing
    assert "현재 gate" in complete
    assert "다음 gate" in implementation_prompt


if __name__ == "__main__":
    main()
