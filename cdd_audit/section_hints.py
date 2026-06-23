from __future__ import annotations

from dataclasses import dataclass

from cdd_audit.model import DocumentInfo, SectionHint, SectionLocation


@dataclass(frozen=True, slots=True)
class HeadingPosition:
    heading: str
    level: int
    start_line: int
    end_line: int


def located_section_hint(hint: SectionHint, document: DocumentInfo | None) -> SectionHint:
    positions = _heading_positions(document) if document is not None else ()
    by_heading = {item.heading: item for item in positions}
    sections: list[SectionLocation] = []
    for heading in hint.headings:
        position = by_heading.get(heading)
        if position is None:
            sections.append(SectionLocation(heading, None, None, False))
        else:
            sections.append(SectionLocation(heading, position.start_line, position.end_line, True))
    return SectionHint(hint.path, hint.headings, tuple(sections))


def _heading_positions(document: DocumentInfo) -> tuple[HeadingPosition, ...]:
    lines = document.text.splitlines()
    total_lines = document.lines
    positions: list[HeadingPosition] = []
    for index, line in enumerate(lines, start=1):
        parsed = _parse_heading(line, index, total_lines)
        if parsed is not None:
            positions.append(parsed)
    return tuple(_with_section_end_lines(tuple(positions), total_lines))


def _parse_heading(line: str, line_number: int, total_lines: int) -> HeadingPosition | None:
    stripped = line.strip()
    level = len(stripped) - len(stripped.lstrip("#"))
    if level < 1 or level > 3:
        return None
    if len(stripped) <= level or stripped[level] != " ":
        return None
    return HeadingPosition(
        heading=f"{'#' * level} {stripped[level:].strip()}",
        level=level,
        start_line=line_number,
        end_line=total_lines,
    )


def _with_section_end_lines(
    positions: tuple[HeadingPosition, ...],
    total_lines: int,
) -> list[HeadingPosition]:
    result: list[HeadingPosition] = []
    for index, position in enumerate(positions):
        end_line = total_lines
        for next_position in positions[index + 1 :]:
            if next_position.level <= position.level:
                end_line = next_position.start_line - 1
                break
        result.append(HeadingPosition(position.heading, position.level, position.start_line, end_line))
    return result
