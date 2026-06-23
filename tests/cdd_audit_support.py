from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / "bin" / "cdd-audit"
sys.path.insert(0, str(ROOT))

from cdd_audit.model import JsonObject, JsonValue


def run_audit(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return run_direct("docs", "--root", str(root), *arguments)


def run_direct(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(COMMAND), *arguments], capture_output=True, check=False, text=True)


def audit_json(result: subprocess.CompletedProcess[str]) -> JsonObject:
    parsed: JsonValue = json.loads(result.stdout)
    assert isinstance(parsed, dict), result.stdout
    data = parsed["readOnlyDocumentAudit"]
    assert isinstance(data, dict), result.stdout
    return data


def section(data: JsonObject, key: str) -> JsonObject:
    value = data[key]
    assert isinstance(value, dict)
    return value


def finding_ids(data: JsonObject) -> set[str]:
    findings = data["findings"]
    assert isinstance(findings, list)
    result: set[str] = set()
    for finding in findings:
        assert isinstance(finding, dict)
        id_value = finding["id"]
        assert isinstance(id_value, str)
        result.add(id_value)
    return result


def documents_by_path(data: JsonObject) -> dict[str, JsonObject]:
    documents = data["documents"]
    assert isinstance(documents, list)
    result: dict[str, JsonObject] = {}
    for document in documents:
        assert isinstance(document, dict)
        path = document["path"]
        assert isinstance(path, str)
        result[path] = document
    return result


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def current_work_pointer() -> str:
    return "\n".join(
        [
            "# Current Work",
            "",
            "현재 gate: planning",
            "다음 task: TASK-001",
            "현재 진행 가능한 task: TASK-001",
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
