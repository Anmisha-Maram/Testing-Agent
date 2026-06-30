"""Rule-based Gherkin generation from requirement text."""

from __future__ import annotations

import re
from typing import Any


STOP_MARKERS = (
    "Reporter",
    "Assignee",
    "Priority",
    "Story ID",
    "Title",
    "Description",
    "Labels",
    "Status",
)


def _extract_title(requirement_text: str) -> str:
    title_match = re.search(
        r"^\s*Title:\s*(.+)$",
        requirement_text,
        re.IGNORECASE | re.MULTILINE,
    )
    if title_match:
        return title_match.group(1).strip()
    return "Generated feature"


def _extract_acceptance_lines(requirement_text: str) -> list[str]:
    lines = requirement_text.splitlines()
    collected: list[str] = []
    capture = False

    for line in lines:
        stripped = line.strip()

        if re.match(r"^Acceptance Criteria\s*:\s*$", stripped, re.IGNORECASE):
            capture = True
            continue

        if not capture:
            continue

        if not stripped:
            continue

        if any(stripped.startswith(marker) for marker in STOP_MARKERS):
            break

        cleaned = re.sub(r"^\d+\.\s*", "", stripped).strip()
        if cleaned:
            collected.append(cleaned)

    return collected


def _parse_given_when_then(line: str) -> dict[str, str] | None:
    pattern = re.compile(
        r"given\s+(?P<given>.+?),\s*when\s+(?P<when>.+?),\s*then\s+(?P<then>.+?)[\.\s]*$",
        re.IGNORECASE,
    )
    match = pattern.search(line)
    if not match:
        return None

    return {
        "given": match.group("given").strip(),
        "when": match.group("when").strip(),
        "then": match.group("then").strip(),
    }


def generate_gherkin(requirement_text: str) -> dict[str, Any]:
    """Generate deterministic Gherkin scenarios from requirement text."""
    if not isinstance(requirement_text, str) or not requirement_text.strip():
        raise ValueError("requirement_text must be a non-empty string")

    feature_title = _extract_title(requirement_text)
    acceptance_lines = _extract_acceptance_lines(requirement_text)

    scenarios: list[dict[str, str]] = []

    for index, line in enumerate(acceptance_lines, start=1):
        parsed = _parse_given_when_then(line)

        if parsed:
            scenario = {
                "title": f"Scenario {index}: {feature_title}",
                "given": parsed["given"],
                "when": parsed["when"],
                "then": parsed["then"],
            }
        else:
            scenario = {
                "title": f"Scenario {index}: {line}",
                "given": "the system is in a valid state",
                "when": line,
                "then": "the expected behavior should occur",
            }

        scenarios.append(scenario)

    if not scenarios:
        scenarios.append(
            {
                "title": "Scenario 1: Generated fallback scenario",
                "given": "the system is in a valid state",
                "when": "the user performs the described action",
                "then": "the expected behavior should occur",
            }
        )

    gherkin_lines = [
        f"Feature: {feature_title}",
        "  As a user",
        "  I want the described behavior",
        "  So that the product works as expected",
        "",
    ]

    for scenario in scenarios:
        gherkin_lines.extend(
            [
                f"  Scenario: {scenario['title']}",
                f"    Given {scenario['given']}",
                f"    When {scenario['when']}",
                f"    Then {scenario['then']}",
                "",
            ]
        )

    raw_gherkin_text = "\n".join(gherkin_lines).rstrip() + "\n"

    return {
        "feature": {"title": feature_title},
        "scenarios": scenarios,
        "scenario_count": len(scenarios),
        "raw_gherkin_text": raw_gherkin_text,
    }