from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, run_direct, section, write


def main() -> None:
    tests = [
        test_config_section_hints_override_heading_guess,
        test_current_work_section_hints_feed_brief_output,
        test_text_format_prints_section_hints,
        test_section_hints_include_line_ranges,
        test_missing_section_hint_heading_blocks_progress,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} section hint tests passed")


def test_config_section_hints_override_heading_guess() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", docs_readme())
        write(
            root / ".cdd-audit.json",
            json.dumps(
                {
                    "sectionHints": {
                        "docs/README.md": ["# Docs", "## Explicit Contract"],
                    },
                }
            ),
        )

        result = run_direct("docs", "--root", str(root), "--format", "brief")
        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json"))
        contract = section(data, "readPathContract")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "docs/README.md > # Docs (L1-L7), ## Explicit Contract (L7-L7)" in result.stdout
        assert "## Current Work" not in result.stdout
        assert contract["sectionHints"] == [
            {
                "path": "docs/README.md",
                "headings": ["# Docs", "## Explicit Contract"],
                "sections": [
                    {"heading": "# Docs", "startLine": 1, "endLine": 7, "exists": True},
                    {"heading": "## Explicit Contract", "startLine": 7, "endLine": 7, "exists": True},
                ],
            },
        ]


def test_current_work_section_hints_feed_brief_output() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(
            root / "docs/project/current-work.md",
            current_work_pointer(
                [
                    "- docs/README.md > # Docs, ## Current Work",
                    "- docs/project/task-contract.md > # Task Contract, ## TASK-002",
                ]
            ),
        )
        write(root / "docs/README.md", docs_readme())
        write(root / "docs/project/task-contract.md", "# Task Contract\n\n## TASK-002\n")

        result = run_direct("docs", "--root", str(root), "--format", "brief")
        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json"))
        contract = section(data, "readPathContract")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "docs/README.md > # Docs (L1-L7), ## Current Work (L3-L4)" in result.stdout
        assert "docs/project/task-contract.md > # Task Contract (L1-L3), ## TASK-002 (L3-L3)" in result.stdout
        assert contract["sectionHints"] == [
            {
                "path": "docs/README.md",
                "headings": ["# Docs", "## Current Work"],
                "sections": [
                    {"heading": "# Docs", "startLine": 1, "endLine": 7, "exists": True},
                    {"heading": "## Current Work", "startLine": 3, "endLine": 4, "exists": True},
                ],
            },
            {
                "path": "docs/project/task-contract.md",
                "headings": ["# Task Contract", "## TASK-002"],
                "sections": [
                    {"heading": "# Task Contract", "startLine": 1, "endLine": 3, "exists": True},
                    {"heading": "## TASK-002", "startLine": 3, "endLine": 3, "exists": True},
                ],
            },
        ]


def test_text_format_prints_section_hints() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(
            root / "docs/project/current-work.md",
            current_work_pointer(["- docs/README.md > # Docs, ## Current Work"]),
        )
        write(root / "docs/README.md", docs_readme())
        write(root / "docs/project/task-contract.md", "# Task Contract\n")

        result = run_direct("docs", "--root", str(root), "--format", "text", "--fail-on", "never")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "- 먼저 볼 섹션:" in result.stdout
        assert "  - docs/README.md > # Docs (L1-L7), ## Current Work (L3-L4)" in result.stdout


def test_section_hints_include_line_ranges() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", docs_readme())
        write(
            root / ".cdd-audit.json",
            json.dumps(
                {
                    "sectionHints": {
                        "docs/README.md": ["# Docs", "## Explicit Contract"],
                    },
                }
            ),
        )

        result = run_direct("docs", "--root", str(root), "--format", "brief")
        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json"))
        contract = section(data, "readPathContract")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "docs/README.md > # Docs (L1-L7), ## Explicit Contract (L7-L7)" in result.stdout
        assert contract["sectionHints"] == [
            {
                "path": "docs/README.md",
                "headings": ["# Docs", "## Explicit Contract"],
                "sections": [
                    {"heading": "# Docs", "startLine": 1, "endLine": 7, "exists": True},
                    {"heading": "## Explicit Contract", "startLine": 7, "endLine": 7, "exists": True},
                ],
            },
        ]


def test_missing_section_hint_heading_blocks_progress() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/README.md", docs_readme())
        write(
            root / ".cdd-audit.json",
            json.dumps(
                {
                    "sectionHints": {
                        "docs/README.md": ["# Docs", "## Missing Heading"],
                    },
                    "roleOverrides": {"docs/readme.md": "active-index"},
                }
            ),
        )

        blocking_result = run_direct("docs", "--root", str(root), "--format", "text")
        result = run_direct("docs", "--root", str(root), "--format", "text", "--fail-on", "never")
        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--fail-on", "never"))
        contract = section(data, "readPathContract")
        findings = data["findings"]

        assert blocking_result.returncode == 2, blocking_result.stdout + blocking_result.stderr
        assert result.returncode == 0, result.stdout + result.stderr
        assert isinstance(findings, list)
        assert "docs/README.md > # Docs (L1-L7), ## Missing Heading (missing)" in result.stdout
        assert "SECTION_HINT_MISSING_HEADING" in result.stdout
        assert contract["sectionHints"][0]["sections"][1] == {
            "heading": "## Missing Heading",
            "startLine": None,
            "endLine": None,
            "exists": False,
        }
        assert findings == [
            {
                "id": "SECTION_HINT_MISSING_HEADING",
                "severity": "blocking",
                "path": "docs/README.md",
                "reason": "먼저 볼 섹션으로 지정된 heading을 문서에서 찾을 수 없습니다.",
                "evidence": "## Missing Heading",
                "recommendedAction": "섹션 힌트를 현재 문서 heading에 맞게 고치거나 current-work/read path 계약을 갱신합니다.",
                "prohibitedAutoAction": "autoModifyReadmeOrIndexWithoutApproval",
            },
            {
                "id": "README_INDEX_UPDATE_REQUIRED",
                "severity": "info",
                "path": None,
                "reason": "문서 배치나 읽기 경로 변경 시 README/index 갱신 여부 확인이 필요합니다.",
                "evidence": "audit produced document-structure findings",
                "recommendedAction": "수정 전 보고에 README/index 갱신 필요 여부를 포함합니다.",
                "prohibitedAutoAction": "autoModifyReadmeOrIndexWithoutApproval",
            },
        ]


def current_work_pointer(section_hint_lines: list[str] | None = None) -> str:
    lines = [
        "# Current Work",
        "",
        "현재 gate: planning",
        "다음 task: TASK-002",
        "현재 진행 가능한 task: TASK-002",
        "반드시 읽을 문서:",
        "- docs/README.md",
        "- docs/project/task-contract.md",
    ]
    if section_hint_lines is not None:
        lines.extend(["먼저 볼 섹션:", *section_hint_lines])
    lines.extend(
        [
            "읽지 않을 과거 기록:",
            "- docs/archive/*",
            "현재 기준과 충돌:",
            "- 없음",
            "README/index 갱신 필요 여부: 없음",
            "",
        ]
    )
    return "\n".join(lines)


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


if __name__ == "__main__":
    main()
