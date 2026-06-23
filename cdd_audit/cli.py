from __future__ import annotations

from pathlib import Path
from typing import assert_never
import json
import sys

from cdd_audit.config import ConfigError, load_config
from cdd_audit.entrypoints import allowed_entrypoints, entrypoint_guide, is_allowed_entrypoint
from cdd_audit.model import (
    AuditOptions,
    AuditResult,
    EntrypointGuide,
    JsonValue,
    SectionHint,
    SectionLocation,
)
from cdd_audit.root import detect_project_root
from cdd_audit.scanner import audit

VERSION = "0.7.0"
USAGE = "\n".join(
    [
        "usage: cdd-audit docs [--root <path>] [--config <path>] [--format text|json|brief] [--fail-on blocking|never] [--entrypoint <name>]",
        "       cdd-audit docs --help",
        "       cdd-audit --version",
    ]
)


def run_cli(arguments: list[str]) -> int:
    parsed = _parse_arguments(arguments)
    if isinstance(parsed, str):
        print(parsed)
        return 0
    if isinstance(parsed, ConfigError):
        print(parsed.message, file=sys.stderr)
        return 1
    root = parsed.root or detect_project_root(Path.cwd())
    if not root.exists() or not root.is_dir():
        print(f"root not found: {root}", file=sys.stderr)
        return 1
    config = load_config(root, parsed.config_path)
    if isinstance(config, ConfigError):
        print(config.message, file=sys.stderr)
        return 1
    result = audit(root, config)
    exit_code = result.exit_code(parsed.fail_on)
    guide = entrypoint_guide(parsed.entrypoint)
    match parsed.output_format:
        case "json":
            print(json.dumps(result.to_json(exit_code, guide), ensure_ascii=False, indent=2))
        case "brief":
            print(_format_brief(result, exit_code, guide))
        case "text":
            print(_format_text(result, exit_code, guide))
        case unreachable:
            assert_never(unreachable)
    return exit_code


def _parse_arguments(arguments: list[str]) -> AuditOptions | ConfigError | str:
    if not arguments or arguments[0] in {"--help", "-h"}:
        return USAGE
    if arguments[0] == "--version":
        return VERSION
    if arguments[0] != "docs":
        return ConfigError(USAGE)
    if len(arguments) > 1 and arguments[1] in {"--help", "-h"}:
        return USAGE
    root: Path | None = None
    config_path: Path | None = None
    output_format = "text"
    fail_on = "blocking"
    entrypoint: str | None = None
    index = 1
    while index < len(arguments):
        arg = arguments[index]
        if arg not in {"--root", "--config", "--format", "--fail-on", "--entrypoint"}:
            return ConfigError(f"unknown option: {arg}\n{USAGE}")
        if index + 1 >= len(arguments):
            return ConfigError(f"missing value for {arg}")
        value = arguments[index + 1]
        index += 2
        if arg == "--root":
            root = Path(value).resolve()
        elif arg == "--config":
            config_path = Path(value).resolve()
        elif arg == "--format":
            if value not in {"text", "json", "brief"}:
                return ConfigError("--format must be text, json, or brief")
            output_format = value
        elif arg == "--fail-on":
            if value not in {"blocking", "never"}:
                return ConfigError("--fail-on must be blocking or never")
            fail_on = value
        elif arg == "--entrypoint":
            if not is_allowed_entrypoint(value):
                return ConfigError(f"--entrypoint must be one of: {allowed_entrypoints()}")
            entrypoint = value
    return AuditOptions(root, config_path, output_format, fail_on, entrypoint)


def _format_text(result: AuditResult, exit_code: int, guide: EntrypointGuide | None = None) -> str:
    blocking = sum(1 for item in result.findings if item.severity == "blocking")
    warning = sum(1 for item in result.findings if item.severity == "warning")
    oversized = _oversized_hot_path_documents(result)
    lines = [
        "문서 읽기 경로 점검:",
        f"- root: {result.root}",
        f"- 현재 작업 포인터: {result.current_pointer_path or '없음'}",
        f"- 현재 gate: {result.current_gate or '없음'}",
        f"- 다음 task: {result.next_task or '없음'}",
        *_entrypoint_lines(guide),
        f"- 반드시 읽을 문서: {_format_list(result.required_read_documents)}",
        *_section_hint_lines(result.section_hints),
        f"- 제외할 과거 기록: {_format_list(result.excluded_history)}",
        f"- 기본 읽기 경로에서 큰 문서: {_format_list(oversized)}",
        f"- 차단 항목: {blocking}",
        f"- 주의 항목: {warning}",
        f"- exit code: {exit_code}",
        "",
        "현재 판단:",
        _judgement_line(blocking),
        "",
        "분리 후보:",
        *_split_recommendation_lines(result),
        "",
        "findings:",
    ]
    if not result.findings:
        lines.append("- 없음")
    for item in result.findings:
        target = f" ({item.path})" if item.path else ""
        lines.append(f"- [{item.severity}] {item.id}{target}: {item.reason}")
        lines.append(f"  추천: {item.recommended_action}")
    lines.extend(["", "다음에 할 일:", _next_step_line(blocking), "", "자동 수정 여부: 없음"])
    return "\n".join(lines)


def _format_brief(result: AuditResult, exit_code: int, guide: EntrypointGuide | None = None) -> str:
    blocking = sum(1 for item in result.findings if item.severity == "blocking")
    warning = sum(1 for item in result.findings if item.severity == "warning")
    return "\n".join(
        [
            "최소 읽기 경로:",
            f"- root: {result.root}",
            f"- 현재 작업 포인터: {result.current_pointer_path or '없음'}",
            f"- 현재 gate: {result.current_gate or '없음'}",
            f"- 다음 task: {result.next_task or '없음'}",
            *_entrypoint_lines(guide),
            f"- 먼저 읽을 문서: {_format_list(result.required_read_documents)}",
            *_section_hint_lines(result.section_hints),
            f"- 읽지 않을 기록: {_format_list(result.excluded_history)}",
            f"- 읽지 않을 보조 자료: {_format_list(result.excluded_non_sot)}",
            f"- 차단 항목: {blocking}",
            f"- 주의 항목: {warning}",
            f"- exit code: {exit_code}",
            "",
            "다음에 할 일:",
            _brief_next_step_line(blocking),
        ]
    )


def _entrypoint_lines(guide: EntrypointGuide | None) -> list[str]:
    if guide is None:
        return []
    return [
        f"- 요청 기준 entrypoint: {guide.name}",
        f"- CDD에서 먼저 볼 문서: {_format_list(guide.primary_documents)}",
        *_entrypoint_section_hint_lines(guide.section_hints),
        f"- 필요하면 확장할 CDD 문서: {_format_list(guide.expansion_documents)}",
    ]


def _entrypoint_section_hint_lines(section_hints: tuple[SectionHint, ...]) -> list[str]:
    if not section_hints:
        return ["- CDD에서 먼저 볼 섹션: 없음"]
    return [
        "- CDD에서 먼저 볼 섹션:",
        *(f"  - {item.path} > {_format_list(item.headings)}" for item in section_hints),
    ]


def _format_list(value: tuple[str, ...] | list[str]) -> str:
    if not value:
        return "없음"
    return ", ".join(value)


def _section_hint_lines(section_hints: tuple[SectionHint, ...]) -> list[str]:
    if not section_hints:
        return ["- 먼저 볼 섹션: 없음"]
    return [
        "- 먼저 볼 섹션:",
        *(f"  - {item.path} > {_format_section_hint(item)}" for item in section_hints),
    ]


def _format_section_hint(section_hint: SectionHint) -> str:
    if not section_hint.sections:
        return _format_list(section_hint.headings)
    return ", ".join(_format_section_location(item) for item in section_hint.sections)


def _format_section_location(section: SectionLocation) -> str:
    if not section.exists:
        if section.suggested_headings:
            return f"{section.heading} (missing; 후보: {_format_list(section.suggested_headings)})"
        return f"{section.heading} (missing)"
    return f"{section.heading} (L{section.start_line}-L{section.end_line})"


def _oversized_hot_path_documents(result: AuditResult) -> list[str]:
    read_cost = result.checks.get("readCost")
    if not isinstance(read_cost, dict):
        return []
    value: JsonValue | None = read_cost.get("oversizedHotPathDocuments")
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _split_recommendation_lines(result: AuditResult) -> list[str]:
    document_structure = result.checks.get("documentStructure")
    if not isinstance(document_structure, dict):
        return ["- 없음"]
    candidates = document_structure.get("splitCandidates")
    if not isinstance(candidates, list) or not candidates:
        return ["- 없음"]
    lines: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        path = candidate.get("path")
        structure = candidate.get("recommendedStructure")
        keep = candidate.get("keepInEntrypoint")
        move = candidate.get("moveToPacketOrHistory")
        if not isinstance(path, str) or not isinstance(structure, str):
            continue
        lines.append(f"- {path}: {structure}")
        if isinstance(keep, str):
            lines.append(f"  남길 것: {keep}")
        if isinstance(move, str):
            lines.append(f"  옮길 것: {move}")
    return lines or ["- 없음"]


def _judgement_line(blocking: int) -> str:
    if blocking:
        return "- 문서 기준과 읽기 경로를 정리하기 전에는 다음 작업 판단으로 넘어가면 안 됩니다."
    return "- 차단 항목은 없습니다. 주의 항목은 사용자 보고에 포함하고 다음 단계로 진행할 수 있습니다."


def _next_step_line(blocking: int) -> str:
    if blocking:
        return "- 현재 작업 포인터, 기본 읽기 경로, active/history 분리 중 필요한 선택지를 사용자에게 제시합니다."
    return "- 사용자 선택이 필요한 차단 항목은 없습니다. 요청 범위 안에서 다음 작업으로 이어갈 수 있습니다."


def _brief_next_step_line(blocking: int) -> str:
    if blocking:
        return "- 전체 감사 보고로 차단 이유를 확인합니다: cdd-audit docs --format text --fail-on never"
    return "- 위 문서만 먼저 읽고, 필요한 경우에만 상세 기준 문서나 과거 기록을 추가로 엽니다."
