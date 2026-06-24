from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, current_work_pointer, run_direct, section, write
from cdd_audit.entrypoints import ENTRYPOINT_NAMES, located_entrypoint_guide


def main() -> None:
    tests = [
        test_entrypoint_option_prints_cdd_read_path,
        test_entrypoint_sections_include_line_ranges,
        test_entrypoint_sections_report_missing_heading_candidates,
        test_complete_work_sections_match_user_facing_headings,
        test_entrypoint_section_hints_cover_primary_documents,
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
        assert "  - plan-task.md > # Plan Task Skill (L1-" in result.stdout
        assert "## 최소 읽기 경로 (L" in result.stdout
        assert "  - _artifact-templates.md > # Artifact Templates V2.1 (L" in result.stdout
        assert "  - _user-facing-language.md > # User-Facing Language Layer (L" in result.stdout
        assert "- 필요하면 확장할 CDD 문서: _source-of-truth-manager.md, _approval-reference.md" in result.stdout
        assert entrypoint["entrypoint"] == "plan-task"
        assert entrypoint["purpose"] == "작업 기준서 작성"
        assert entrypoint["primaryDocuments"] == [
            "plan-task.md",
            "_readiness-gates.md",
            "_artifact-templates.md",
            "_user-facing-language.md",
        ]
        assert entrypoint["expansionDocuments"] == ["_source-of-truth-manager.md", "_approval-reference.md"]


def test_entrypoint_sections_include_line_ranges() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", "# Docs\n")

        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--entrypoint", "plan-task"))
        entrypoint = section(data, "entrypointReadPath")
        hints = entrypoint["sectionHints"]
        assert isinstance(hints, list)
        first_hint = hints[0]
        assert isinstance(first_hint, dict)
        sections = first_hint["sections"]
        assert isinstance(sections, list)

        assert sections[0]["heading"] == "# Plan Task Skill"
        assert sections[0]["startLine"] == 1
        assert isinstance(sections[0]["endLine"], int)
        assert sections[0]["exists"] is True
        assert all(item["exists"] is True for item in sections)


def test_entrypoint_sections_report_missing_heading_candidates() -> None:
    with TemporaryDirectory() as temp:
        skill_root = Path(temp)
        write(skill_root / "revise-work.md", "# Revise Work Skill\n\n## 최소 읽기 경로\n\n## 시작 조건\n\n## 중단 조건\n")
        write(skill_root / "verify-work.md", "# Verify Work Skill\n\n## 결과 상태\n\n## 다음 단계 후보\n")

        guide = located_entrypoint_guide("revise-work", skill_root)
        assert guide is not None
        verify_work_hint = guide.section_hints[1]
        missing = verify_work_hint.sections[2]

        assert missing.heading == "## 다음 단계"
        assert missing.exists is False
        assert missing.suggested_headings == ("## 다음 단계 후보",)


def test_complete_work_sections_match_user_facing_headings() -> None:
    guide = located_entrypoint_guide("complete-work")
    assert guide is not None
    user_facing_hint = guide.section_hints[3]
    sections = user_facing_hint.sections

    assert tuple(item.heading for item in sections) == (
        "# User-Facing Language Layer",
        "## 후속 작업 승인 요청 브리핑",
        "## 응답 종료 형식",
        "### 완료한 경우",
        "## 사용자 보고와 내부 보고 분리",
    )
    assert all(item.exists is True for item in sections)


def test_entrypoint_section_hints_cover_primary_documents() -> None:
    for name in ENTRYPOINT_NAMES:
        guide = located_entrypoint_guide(name)
        assert guide is not None
        hinted_paths = {item.path for item in guide.section_hints}

        assert set(guide.primary_documents) <= hinted_paths


def test_invalid_entrypoint_exits_one() -> None:
    result = run_direct("docs", "--entrypoint", "not-real")

    assert result.returncode == 1
    assert "--entrypoint must be one of:" in result.stderr


if __name__ == "__main__":
    main()
