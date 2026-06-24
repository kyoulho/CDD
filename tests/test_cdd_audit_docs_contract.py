from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tests = [
        test_cdd_audit_path_fallback_is_user_optional,
        test_user_facing_examples_are_discoverable_from_main_rule,
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


if __name__ == "__main__":
    main()
