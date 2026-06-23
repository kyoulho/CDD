from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from cdd_audit_support import (
    COMMAND,
    audit_json,
    current_work_pointer,
    documents_by_path,
    finding_ids,
    run_audit,
    run_direct,
    section,
    snapshot,
    write,
)


def main() -> None:
    tests: list[Callable[[], None]] = [
        test_complete_pointer_exits_zero_and_does_not_write,
        test_direct_command_runs_with_supported_python,
        test_symlinked_command_runs_from_any_directory,
        test_root_is_detected_from_nested_directory,
        test_current_work_pointer_fields_are_extracted,
        test_brief_format_prints_only_minimal_read_path,
        test_config_overrides_document_roles_and_default_read_path,
        test_history_path_beats_active_keywords,
        test_oversized_hot_path_blocks_without_pointer,
        test_large_documents_report_actionable_split_recommendations,
        test_task_contract_split_recommendation_prefers_active_index_and_history,
        test_fail_on_never_keeps_findings_but_exits_zero,
        test_help_exits_zero,
        test_missing_root_exits_one,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")


def test_complete_pointer_exits_zero_and_does_not_write() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/README.md", "# Docs\n")
        write(root / "docs/project/current-work.md", current_work_pointer())
        before = snapshot(root)
        result = run_audit(root, "--format", "json")
        data = audit_json(result)
        summary = section(data, "summary")
        current = section(data, "currentWorkPointer")

        assert result.returncode == 0, result.stdout + result.stderr
        assert summary["blockingCount"] == 0
        assert current["path"] == "docs/project/current-work.md"
        assert snapshot(root) == before


def test_direct_command_runs_with_supported_python() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        result = run_direct("docs", "--root", str(root), "--format", "json")
        data = audit_json(result)
        summary = section(data, "summary")

        assert result.returncode == 0, result.stdout + result.stderr
        assert summary["blockingCount"] == 0


def test_symlinked_command_runs_from_any_directory() -> None:
    with TemporaryDirectory() as temp:
        workspace = Path(temp)
        root = workspace / "project"
        link = workspace / "cdd-audit"
        write(root / "docs/project/current-work.md", current_work_pointer())
        link.symlink_to(COMMAND)

        result = subprocess.run(
            [str(link), "docs", "--root", str(root), "--format", "json"],
            cwd=workspace,
            capture_output=True,
            check=False,
            text=True,
        )
        data = audit_json(result)

        assert result.returncode == 0, result.stdout + result.stderr
        assert section(data, "currentWorkPointer")["path"] == "docs/project/current-work.md"


def test_root_is_detected_from_nested_directory() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        nested = root / "docs/project/nested"
        write(root / "docs/project/current-work.md", current_work_pointer())
        nested.mkdir(parents=True)

        result = subprocess.run(
            [str(COMMAND), "docs", "--format", "json"],
            cwd=nested,
            capture_output=True,
            check=False,
            text=True,
        )
        data = audit_json(result)

        assert result.returncode == 0, result.stdout + result.stderr
        assert data["root"] == str(root.resolve())


def test_current_work_pointer_fields_are_extracted() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        result = run_direct("docs", "--root", str(root), "--format", "json")
        data = audit_json(result)
        current = section(data, "currentWorkPointer")
        contract = section(data, "readPathContract")

        assert current["currentGate"] == "planning"
        assert current["nextTask"] == "TASK-001"
        assert current["activeTasks"] == ["TASK-001"]
        assert contract["requiredReadDocuments"] == ["docs/README.md"]
        assert contract["excludedHistoricalRecords"] == ["docs/archive/*"]


def test_brief_format_prints_only_minimal_read_path() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        result = run_direct("docs", "--root", str(root), "--format", "brief")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "최소 읽기 경로:" in result.stdout
        assert "- 먼저 읽을 문서: docs/README.md" in result.stdout
        assert "- 읽지 않을 기록: docs/archive/*" in result.stdout
        assert "findings:" not in result.stdout
        assert "분리 후보:" not in result.stdout


def test_config_overrides_document_roles_and_default_read_path() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "DESIGN.md", "# Design\n")
        write(
            root / ".cdd-audit.json",
            json.dumps(
                {
                    "defaultReadPath": ["DESIGN.md"],
                    "roleOverrides": {"DESIGN.md": "current-criteria"},
                    "ignore": ["docs/archive/**"],
                }
            ),
        )
        result = run_direct("docs", "--root", str(root), "--format", "json")
        data = audit_json(result)
        documents = documents_by_path(data)

        assert result.returncode == 0, result.stdout + result.stderr
        assert documents["DESIGN.md"]["role"] == "current-criteria"
        assert documents["DESIGN.md"]["inDefaultReadPath"] is True


def test_history_path_beats_active_keywords() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/project/task-001-completion.md", "# Completion\n\nnext task: TASK-002\n")
        result = run_direct("docs", "--root", str(root), "--format", "json")
        data = audit_json(result)
        documents = documents_by_path(data)
        active_history = section(data, "checks")["activeHistorySeparation"]
        assert isinstance(active_history, dict)

        assert result.returncode == 0, result.stdout + result.stderr
        assert documents["docs/project/task-001-completion.md"]["role"] == "history"
        assert documents["docs/project/task-001-completion.md"]["inDefaultReadPath"] is False
        assert "docs/project/task-001-completion.md" not in active_history["activeIndexCandidates"]
        assert "ACTIVE_HISTORY_MIXED" not in finding_ids(data)


def test_oversized_hot_path_blocks_without_pointer() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/implementation-task-contract.md", "\n".join(f"- task line {index}" for index in range(405)))
        before = snapshot(root)
        result = run_audit(root, "--format", "json")
        data = audit_json(result)
        ids = finding_ids(data)

        assert result.returncode == 2, result.stdout + result.stderr
        assert "CURRENT_WORK_POINTER_MISSING" in ids
        assert "HOT_PATH_OVERSIZED" in ids
        assert snapshot(root) == before


def test_large_documents_report_actionable_split_recommendations() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(root / "docs/project/engineering-sot.md", "\n".join(f"- criterion {index}" for index in range(405)))
        result = run_audit(root, "--format", "text", "--fail-on", "never")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "분리 후보:" in result.stdout
        assert "docs/project/engineering-sot.md" in result.stdout
        assert "얇은 진입점" in result.stdout
        assert "세부 기준 packet" in result.stdout


def test_task_contract_split_recommendation_prefers_active_index_and_history() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/current-work.md", current_work_pointer())
        write(
            root / "docs/project/implementation-task-contract.md",
            "\n".join(f"- completed task detail {index}" for index in range(405)),
        )
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        document_structure = section(data, "checks")["documentStructure"]
        assert isinstance(document_structure, dict)
        split_candidates = document_structure["splitCandidates"]
        assert isinstance(split_candidates, list)

        assert result.returncode == 0, result.stdout + result.stderr
        assert split_candidates == [
            {
                "path": "docs/project/implementation-task-contract.md",
                "role": "task-contract",
                "reason": "405 lines, 11229 bytes",
                "recommendedStructure": "현재 진행 가능한 task만 active index에 남기고 완료/검증/과거 task는 history로 분리합니다.",
                "keepInEntrypoint": "현재 gate, 다음 task, 현재 진행 가능한 task, 반드시 읽을 문서",
                "moveToPacketOrHistory": "완료된 task, 과거 구현 지시서, 검증 결과, 완료 기록",
                "readmeOrIndexUpdateRequired": True,
            }
        ]


def test_fail_on_never_keeps_findings_but_exits_zero() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/implementation-task-contract.md", "\n".join(f"- task line {index}" for index in range(405)))
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        summary = section(data, "summary")

        assert result.returncode == 0, result.stdout + result.stderr
        assert summary["blockingCount"] != 0


def test_help_exits_zero() -> None:
    result = run_direct("docs", "--help")

    assert result.returncode == 0
    assert "usage: cdd-audit docs" in result.stdout


def test_missing_root_exits_one() -> None:
    with TemporaryDirectory() as temp:
        missing = Path(temp) / "missing"
        result = run_audit(missing, "--format", "json")

        assert result.returncode == 1
        assert "root not found" in result.stderr

if __name__ == "__main__":
    main()
