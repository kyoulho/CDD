from __future__ import annotations

from dataclasses import dataclass

from cdd_audit.model import CURRENT_POINTER_FIELDS, DocumentInfo


@dataclass(frozen=True, slots=True)
class PointerDetails:
    current_gate: str | None
    next_task: str | None
    active_tasks: tuple[str, ...]
    required_read_documents: tuple[str, ...]
    excluded_historical_records: tuple[str, ...]
    excluded_non_sot_references: tuple[str, ...]


def empty_pointer_details() -> PointerDetails:
    return PointerDetails(None, None, (), (), (), ())


def missing_pointer_fields(pointer: DocumentInfo | None) -> tuple[str, ...]:
    if pointer is None:
        return tuple(CURRENT_POINTER_FIELDS.keys())
    return tuple(
        field
        for field, patterns in CURRENT_POINTER_FIELDS.items()
        if not any(pattern in pointer.text_lower for pattern in patterns)
    )


def pointer_details(pointer: DocumentInfo | None) -> PointerDetails:
    if pointer is None:
        return empty_pointer_details()
    return PointerDetails(
        current_gate=_field_scalar(pointer.text, CURRENT_POINTER_FIELDS["currentGate"]),
        next_task=_field_scalar(pointer.text, CURRENT_POINTER_FIELDS["nextTask"]),
        active_tasks=_field_values(pointer.text, CURRENT_POINTER_FIELDS["activeTasks"]),
        required_read_documents=_field_values(pointer.text, CURRENT_POINTER_FIELDS["requiredReadDocuments"]),
        excluded_historical_records=_field_values(pointer.text, CURRENT_POINTER_FIELDS["excludedHistoricalRecords"]),
        excluded_non_sot_references=_field_values(pointer.text, ("excluded non-sot", "excludednonsot", "비-sot", "보조 자료")),
    )


def _field_scalar(text: str, patterns: tuple[str, ...]) -> str | None:
    values = _field_values(text, patterns)
    if not values:
        return None
    return values[0]


def _field_values(text: str, patterns: tuple[str, ...]) -> tuple[str, ...]:
    lines = text.splitlines()
    result: list[str] = []
    collecting = False
    for line in lines:
        normalized = _normalize(line)
        if _starts_field(normalized, patterns):
            collecting = True
            inline = _inline_value(line)
            if inline:
                result.extend(_split_values(inline))
            continue
        if collecting:
            if _looks_like_other_field(normalized):
                break
            bullet = _bullet_value(line)
            if bullet:
                result.append(bullet)
    return tuple(item for item in result if item and item != "없음")


def _starts_field(normalized_line: str, patterns: tuple[str, ...]) -> bool:
    return any(normalized_line.startswith(_normalize(pattern)) for pattern in patterns)


def _looks_like_other_field(normalized_line: str) -> bool:
    if not normalized_line:
        return False
    for patterns in CURRENT_POINTER_FIELDS.values():
        if _starts_field(normalized_line, patterns):
            return True
    return ":" in normalized_line and not normalized_line.startswith("-")


def _inline_value(line: str) -> str | None:
    if ":" not in line:
        return None
    value = line.split(":", 1)[1].strip()
    return value or None


def _bullet_value(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith(("- ", "* ")):
        return stripped[2:].strip()
    return None


def _split_values(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _normalize(value: str) -> str:
    return "".join(value.lower().split())
