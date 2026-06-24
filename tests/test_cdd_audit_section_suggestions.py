from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, run_direct, section, write


def main() -> None:
    tests = [
        test_missing_heading_suggests_similar_existing_heading,
        test_missing_heading_text_output_prints_suggestions,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} section suggestion tests passed")


def test_missing_heading_suggests_similar_existing_heading() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", docs_readme())
        write(root / ".cdd-audit.json", config_with_missing_heading())

        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--fail-on", "never"))
        contract = section(data, "readPathContract")
        findings = data["findings"]

        assert isinstance(findings, list)
        assert contract["sectionHints"][0]["sections"][1] == {
            "heading": "## Required Read Document",
            "startLine": None,
            "endLine": None,
            "exists": False,
            "suggestedHeadings": ["## Required Read Documents"],
        }
        assert findings[0]["id"] == "SECTION_HINT_MISSING_HEADING"
        assert findings[0]["severity"] == "blocking"
        assert findings[0]["evidence"] == "## Required Read Document -> 후보: ## Required Read Documents"


def test_missing_heading_text_output_prints_suggestions() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", docs_readme())
        write(root / ".cdd-audit.json", config_with_missing_heading())

        result = run_direct("docs", "--root", str(root), "--format", "text", "--fail-on", "never")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "## Required Read Document (missing; 후보: ## Required Read Documents)" in result.stdout
        assert "evidence" not in result.stdout
        assert "후보: ## Required Read Documents" in result.stdout


def current_work_pointer() -> str:
    return "\n".join(
        [
            "# Current Work",
            "",
            "현재 gate: planning",
            "다음 task: TASK-002",
            "현재 진행 가능한 task: TASK-002",
            "반드시 읽을 문서:",
            "- docs/README.md",
            "읽지 않을 과거 기록:",
            "- docs/archive/*",
            "현재 기준과 충돌:",
            "- 없음",
            "README/index 갱신 필요 여부: 없음",
            "",
        ]
    )


def docs_readme() -> str:
    return "\n".join(
        [
            "# Docs",
            "",
            "## Current Work",
            "",
            "## Required Read Documents",
            "",
            "## Explicit Contract",
            "",
        ]
    )


def config_with_missing_heading() -> str:
    return json.dumps(
        {
            "sectionHints": {
                "docs/README.md": ["# Docs", "## Required Read Document"],
            },
            "roleOverrides": {"docs/readme.md": "active-index"},
        }
    )


if __name__ == "__main__":
    main()
