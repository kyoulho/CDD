from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, current_work_pointer, run_direct, section, write


def main() -> None:
    tests = [
        test_entrypoint_option_prints_cdd_read_path,
        test_invalid_entrypoint_exits_one,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} entrypoint tests passed")


def test_entrypoint_option_prints_cdd_read_path() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", "# Docs\n")

        result = run_direct("docs", "--root", str(root), "--format", "brief", "--entrypoint", "plan-task")
        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--entrypoint", "plan-task"))
        entrypoint = section(data, "entrypointReadPath")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "- 요청 기준 entrypoint: plan-task" in result.stdout
        assert "- CDD에서 먼저 볼 문서: plan-task.md, _readiness-gates.md, _artifact-templates.md, _user-facing-language.md" in result.stdout
        assert "  - plan-task.md > # Plan Task Skill, ## 최소 읽기 경로, ## 시작 조건, ## 작업 기준서 필수 항목" in result.stdout
        assert "- 필요하면 확장할 CDD 문서: _source-of-truth-manager.md, _approval-reference.md" in result.stdout
        assert entrypoint == {
            "entrypoint": "plan-task",
            "purpose": "작업 기준서 작성",
            "primaryDocuments": [
                "plan-task.md",
                "_readiness-gates.md",
                "_artifact-templates.md",
                "_user-facing-language.md",
            ],
            "sectionHints": [
                {
                    "path": "plan-task.md",
                    "headings": [
                        "# Plan Task Skill",
                        "## 최소 읽기 경로",
                        "## 시작 조건",
                        "## 작업 기준서 필수 항목",
                    ],
                    "sections": [],
                },
                {
                    "path": "_readiness-gates.md",
                    "headings": [
                        "# Readiness Gates",
                        "## 제품 기준 준비 상태",
                        "## 기술 설계 준비 상태",
                        "## 구조 제안 전 의미 확인",
                    ],
                    "sections": [],
                },
            ],
            "expansionDocuments": ["_source-of-truth-manager.md", "_approval-reference.md"],
        }


def test_invalid_entrypoint_exits_one() -> None:
    result = run_direct("docs", "--entrypoint", "not-real")

    assert result.returncode == 1
    assert "--entrypoint must be one of:" in result.stderr


if __name__ == "__main__":
    main()
