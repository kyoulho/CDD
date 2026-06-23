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
        assert "docs/README.md > # Docs, ## Explicit Contract" in result.stdout
        assert "## Current Work" not in result.stdout
        assert contract["sectionHints"] == [
            {"path": "docs/README.md", "headings": ["# Docs", "## Explicit Contract"]},
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
        assert "docs/README.md > # Docs, ## Current Work" in result.stdout
        assert "docs/project/task-contract.md > # Task Contract, ## TASK-002" in result.stdout
        assert contract["sectionHints"] == [
            {"path": "docs/README.md", "headings": ["# Docs", "## Current Work"]},
            {"path": "docs/project/task-contract.md", "headings": ["# Task Contract", "## TASK-002"]},
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
        assert "  - docs/README.md > # Docs, ## Current Work" in result.stdout


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
