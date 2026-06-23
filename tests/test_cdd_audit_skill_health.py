from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from cdd_audit_support import audit_json, finding_ids, run_direct, section, write


def main() -> None:
    tests = [
        test_valid_skill_health_is_reported_without_findings,
        test_invalid_skill_frontmatter_reports_blocking_finding,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} skill health tests passed")


def test_valid_skill_health_is_reported_without_findings() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "SKILL.md", valid_skill())
        write(root / "agents/openai.yaml", valid_openai_yaml())

        data = audit_json(run_direct("docs", "--root", str(root), "--format", "json"))
        checks = section(data, "checks")
        skill_health = checks["skillHealth"]
        assert isinstance(skill_health, dict)

        assert skill_health["isSkillRoot"] is True
        assert skill_health["frontmatterStartValid"] is True
        assert skill_health["frontmatterClosed"] is True
        assert skill_health["name"] == "example-skill"
        assert skill_health["descriptionPresent"] is True
        assert skill_health["unexpectedFrontmatterKeys"] == []
        assert skill_health["agentsOpenaiExists"] is True
        assert skill_health["agentsOpenaiHasDisplayName"] is True
        assert skill_health["agentsOpenaiHasShortDescription"] is True
        assert skill_health["agentsOpenaiHasDefaultPrompt"] is True
        assert skill_health["agentsOpenaiAllowsImplicitInvocation"] is True
        assert "SKILL_FRONTMATTER_INVALID" not in finding_ids(data)
        assert "SKILL_DESCRIPTION_MISSING" not in finding_ids(data)
        assert "SKILL_OPENAI_YAML_INCOMPLETE" not in finding_ids(data)


def test_invalid_skill_frontmatter_reports_blocking_finding() -> None:
    with TemporaryDirectory() as temp:
        root = Path(temp)
        write(root / "SKILL.md", "# Title Before Frontmatter\n---\nname: bad\n---\n")

        result = run_direct("docs", "--root", str(root), "--format", "json", "--fail-on", "never")
        data = audit_json(result)
        checks = section(data, "checks")
        skill_health = checks["skillHealth"]
        assert isinstance(skill_health, dict)

        assert result.returncode == 0
        assert skill_health["isSkillRoot"] is True
        assert skill_health["frontmatterStartValid"] is False
        assert "SKILL_FRONTMATTER_INVALID" in finding_ids(data)
        assert "SKILL_DESCRIPTION_MISSING" in finding_ids(data)
        assert "SKILL_OPENAI_YAML_INCOMPLETE" in finding_ids(data)


def valid_skill() -> str:
    return "\n".join(
        [
            "---",
            "name: example-skill",
            "description: 예시 skill 설명",
            "---",
            "# Example Skill",
            "",
        ]
    )


def valid_openai_yaml() -> str:
    return "\n".join(
        [
            "interface:",
            '  display_name: "Example"',
            '  short_description: "예시 skill"',
            '  default_prompt: "$example-skill를 사용해 작업해라."',
            "policy:",
            "  allow_implicit_invocation: true",
            "",
        ]
    )


if __name__ == "__main__":
    main()
