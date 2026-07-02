from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, finding_ids, run_audit, section, write


def main() -> None:
    tests: list[Callable[[], None]] = [
        test_completed_tasks_in_active_contract_trigger_rollup_warning,
        test_completed_tasks_in_archive_do_not_trigger_hot_path_warning,
        test_legacy_policy_in_task_history_blocks_when_in_default_read_path,
        test_old_prompt_in_hot_path_is_prune_candidate,
        test_task_retention_config_changes_thresholds,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} task retention tests passed")


def test_completed_tasks_in_active_contract_trigger_rollup_warning() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/project/implementation-task-contract.md", _completed_task_contract(4))
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        task_retention = section(data["checks"], "taskRetention")
        candidates = task_retention["rollupCandidates"]

        assert result.returncode == 0, result.stdout + result.stderr
        assert "TASK_ROLLUP_DUE" in finding_ids(data)
        assert "COMPLETED_TASK_IN_HOT_PATH" in finding_ids(data)
        assert isinstance(candidates, list)
        assert candidates[0]["path"] == "docs/project/implementation-task-contract.md"
        assert candidates[0]["completedTaskCount"] == 4
        assert candidates[0]["limit"] == 3


def test_completed_tasks_in_archive_do_not_trigger_hot_path_warning() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "docs/archive/implementation-task-contract.md", _completed_task_contract(5))
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        ids = finding_ids(data)

        assert "TASK_ROLLUP_DUE" not in ids
        assert "COMPLETED_TASK_IN_HOT_PATH" not in ids


def test_legacy_policy_in_task_history_blocks_when_in_default_read_path() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(
            root / ".cdd-audit.json",
            json.dumps({"defaultReadPath": ["docs/history/task-history.md"]}),
        )
        write(
            root / "docs/history/task-history.md",
            "\n".join(
                [
                    "# Task History",
                    "",
                    "## TASK-OLD",
                    "",
                    "status: COMPLETE",
                    "API path must stay `/legacy`.",
                    "",
                ]
            ),
        )
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)

        assert "LEGACY_POLICY_IN_TASK_HISTORY" in finding_ids(data)
        assert section(data, "summary")["blockingCount"] == 1


def test_old_prompt_in_hot_path_is_prune_candidate() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(
            root / ".cdd-audit.json",
            json.dumps({"defaultReadPath": ["docs/project/task-old-prompt.md"]}),
        )
        write(root / "docs/project/task-old-prompt.md", "# TASK-OLD Prompt\n\nstatus: COMPLETE\n")
        result = run_audit(root, "--format", "brief", "--fail-on", "never")

        assert result.returncode == 0, result.stdout + result.stderr
        assert "TASK 정리 후보:" in result.stdout
        assert "docs/project/task-old-prompt.md" in result.stdout


def test_task_retention_config_changes_thresholds() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(
            root / ".cdd-audit.json",
            json.dumps(
                {
                    "taskRetention": {
                        "activeTaskLimit": 2,
                        "recentCompletedTaskLimit": 1,
                        "rollupBy": "milestone",
                    }
                }
            ),
        )
        write(root / "docs/project/implementation-task-contract.md", _completed_task_contract(2))
        result = run_audit(root, "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        task_retention = section(data["checks"], "taskRetention")
        policy = section(task_retention, "policy")
        candidates = task_retention["rollupCandidates"]

        assert policy["activeTaskLimit"] == 2
        assert policy["recentCompletedTaskLimit"] == 1
        assert policy["rollupBy"] == "milestone"
        assert isinstance(candidates, list)
        assert candidates[0]["completedTaskCount"] == 2


def _completed_task_contract(count: int) -> str:
    sections = ["# Implementation Task Contract", ""]
    for index in range(1, count + 1):
        sections.extend(
            [
                f"## TASK-{index:03d}",
                "",
                "status: COMPLETE",
                "완료 기록입니다.",
                "",
            ]
        )
    return "\n".join(sections)


if __name__ == "__main__":
    main()
