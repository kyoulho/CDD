from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, documents_by_path, run_direct, section, write


def main() -> None:
    tests = [
        test_cdd_skill_documents_keep_harness_roles,
        test_non_cdd_project_history_role_still_wins,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} role tests passed")


def test_cdd_skill_documents_keep_harness_roles() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "SKILL.md", "---\nname: cdd\ndescription: CDD\n---\n# CDD Skill\n")
        write(root / "README.md", "# CDD\n")
        write(root / "start-here.md", "# Start Here Skill\n\nhistory archive completion\n")
        write(root / "complete-work.md", "# Complete Work Skill\n\nstatus: COMPLETE\n")
        write(root / "_source-of-truth-manager.md", "# Source\n\nhistory completion\n")
        write(root / "references/forward-testing.md", "# Cases\n\narchive 완료 기록\n")

        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--fail-on", "never"))
        documents = documents_by_path(data)
        active_history = section(data, "checks")["activeHistorySeparation"]
        assert isinstance(active_history, dict)

        assert documents["start-here.md"]["role"] == "cdd-public-entrypoint"
        assert documents["complete-work.md"]["role"] == "cdd-public-entrypoint"
        assert documents["_source-of-truth-manager.md"]["role"] == "cdd-internal-module"
        assert documents["references/forward-testing.md"]["role"] == "cdd-reference"
        assert "complete-work.md" not in active_history["historyCandidates"]


def test_non_cdd_project_history_role_still_wins() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "SKILL.md", "---\nname: other\ndescription: Other\n---\n# Other\n")
        write(root / "complete-work.md", "# Complete Work\n\nstatus: COMPLETE\n")

        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json", "--fail-on", "never"))
        documents = documents_by_path(data)

        assert documents["complete-work.md"]["role"] == "history"


if __name__ == "__main__":
    main()
