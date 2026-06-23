from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final
import re

from cdd_audit.model import Finding, JsonObject

ALLOWED_FRONTMATTER_KEYS: Final[frozenset[str]] = frozenset({"name", "description"})


@dataclass(frozen=True, slots=True)
class SkillHealth:
    is_skill_root: bool
    frontmatter_start_valid: bool
    frontmatter_closed: bool
    name: str | None
    description_present: bool
    unexpected_frontmatter_keys: tuple[str, ...]
    agents_openai_exists: bool
    agents_openai_has_display_name: bool
    agents_openai_has_short_description: bool
    agents_openai_has_default_prompt: bool
    agents_openai_allows_implicit_invocation: bool

    def to_json(self) -> JsonObject:
        return {
            "isSkillRoot": self.is_skill_root,
            "frontmatterStartValid": self.frontmatter_start_valid,
            "frontmatterClosed": self.frontmatter_closed,
            "name": self.name,
            "descriptionPresent": self.description_present,
            "unexpectedFrontmatterKeys": list(self.unexpected_frontmatter_keys),
            "agentsOpenaiExists": self.agents_openai_exists,
            "agentsOpenaiHasDisplayName": self.agents_openai_has_display_name,
            "agentsOpenaiHasShortDescription": self.agents_openai_has_short_description,
            "agentsOpenaiHasDefaultPrompt": self.agents_openai_has_default_prompt,
            "agentsOpenaiAllowsImplicitInvocation": self.agents_openai_allows_implicit_invocation,
        }


def skill_health(root: Path) -> SkillHealth:
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return SkillHealth(False, False, False, None, False, (), False, False, False, False, False)
    text = skill_path.read_text(encoding="utf-8")
    start_valid, closed, metadata = _frontmatter(text)
    openai = _openai_yaml(root / "agents" / "openai.yaml")
    return SkillHealth(
        is_skill_root=True,
        frontmatter_start_valid=start_valid,
        frontmatter_closed=closed,
        name=metadata.get("name"),
        description_present=bool(metadata.get("description")),
        unexpected_frontmatter_keys=tuple(sorted(set(metadata) - ALLOWED_FRONTMATTER_KEYS)),
        agents_openai_exists=openai.exists,
        agents_openai_has_display_name=openai.display_name,
        agents_openai_has_short_description=openai.short_description,
        agents_openai_has_default_prompt=openai.default_prompt,
        agents_openai_allows_implicit_invocation=openai.implicit_invocation,
    )


def skill_health_findings(health: SkillHealth) -> tuple[Finding, ...]:
    if not health.is_skill_root:
        return ()
    result: list[Finding] = []
    if not health.frontmatter_start_valid or not health.frontmatter_closed:
        result.append(
            _finding(
                "SKILL_FRONTMATTER_INVALID",
                "blocking",
                "SKILL.md",
                "SKILL.md frontmatter 형식이 Codex skill 규격에 맞지 않습니다.",
                "frontmatter must start on line 1 and close with ---",
                "SKILL.md 첫 줄을 ---로 두고 name/description frontmatter를 닫습니다.",
            )
        )
    if health.name is None:
        result.append(
            _finding(
                "SKILL_NAME_MISSING",
                "blocking",
                "SKILL.md",
                "SKILL.md frontmatter에 name이 없습니다.",
                "missing name",
                "frontmatter에 name을 추가합니다.",
            )
        )
    if not health.description_present:
        result.append(
            _finding(
                "SKILL_DESCRIPTION_MISSING",
                "blocking",
                "SKILL.md",
                "SKILL.md frontmatter에 description이 없습니다.",
                "missing description",
                "frontmatter에 skill trigger가 드러나는 description을 추가합니다.",
            )
        )
    if health.unexpected_frontmatter_keys:
        result.append(
            _finding(
                "SKILL_FRONTMATTER_EXTRA_KEYS",
                "warning",
                "SKILL.md",
                "SKILL.md frontmatter에 name/description 외 key가 있습니다.",
                ", ".join(health.unexpected_frontmatter_keys),
                "Codex trigger에 필요한 name과 description만 남길지 검토합니다.",
            )
        )
    if _openai_yaml_incomplete(health):
        result.append(
            _finding(
                "SKILL_OPENAI_YAML_INCOMPLETE",
                "warning",
                "agents/openai.yaml",
                "agents/openai.yaml UI metadata가 없거나 필수 표시 항목이 부족합니다.",
                "display_name, short_description, default_prompt, allow_implicit_invocation",
                "SKILL.md와 맞는 display_name, short_description, default_prompt를 확인합니다.",
            )
        )
    return tuple(result)


@dataclass(frozen=True, slots=True)
class OpenAiYaml:
    exists: bool
    display_name: bool
    short_description: bool
    default_prompt: bool
    implicit_invocation: bool


def _frontmatter(text: str) -> tuple[bool, bool, dict[str, str]]:
    lines = text.splitlines()
    start_valid = bool(lines) and lines[0].strip() == "---"
    if not start_valid:
        return False, False, {}
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return True, True, metadata
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip("\"'")
    return True, False, metadata


def _openai_yaml(path: Path) -> OpenAiYaml:
    if not path.is_file():
        return OpenAiYaml(False, False, False, False, False)
    text = path.read_text(encoding="utf-8")
    return OpenAiYaml(
        exists=True,
        display_name=_has_yaml_value(text, "display_name"),
        short_description=_has_yaml_value(text, "short_description"),
        default_prompt=_has_yaml_value(text, "default_prompt"),
        implicit_invocation=bool(re.search(r"(?m)^\s*allow_implicit_invocation\s*:\s*true\s*$", text)),
    )


def _has_yaml_value(text: str, key: str) -> bool:
    return bool(re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*.+\S\s*$", text))


def _openai_yaml_incomplete(health: SkillHealth) -> bool:
    return not (
        health.agents_openai_exists
        and health.agents_openai_has_display_name
        and health.agents_openai_has_short_description
        and health.agents_openai_has_default_prompt
        and health.agents_openai_allows_implicit_invocation
    )


def _finding(
    id_value: str,
    severity: str,
    path: str,
    reason: str,
    evidence: str,
    action: str,
) -> Finding:
    return Finding(id_value, severity, path, reason, evidence, action, "autoModifySkillMetadataWithoutApproval")
