"""Rule-based Playwright test generation from Gherkin scenarios."""

from __future__ import annotations

import re
from typing import Any


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return slug or "generated_test"


def _escape_js_string(text: str) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'")


def _normalize_phrase(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _route_regex_from_then(then_text: str) -> str:
    lowered = then_text.lower()

    if "password reset" in lowered or "reset password" in lowered:
        return "reset-password|forgot-password"

    if "login page" in lowered or "login" in lowered:
        return "login"

    if "dashboard" in lowered:
        return "dashboard"

    if "home page" in lowered or "homepage" in lowered or "home" in lowered:
        return "home"

    return ".+"


def _heading_regex_from_then(then_text: str) -> str | None:
    lowered = then_text.lower()

    if "password reset" in lowered or "reset password" in lowered:
        return "reset password|forgot password"

    if "login page" in lowered or "login" in lowered:
        return "login|sign in"

    if "dashboard" in lowered:
        return "dashboard"

    if "home page" in lowered or "homepage" in lowered or "home" in lowered:
        return "home"

    return None


def _validation_text_regex_from_then(then_text: str) -> str | None:
    lowered = then_text.lower()

    if "email required" in lowered or "email is required" in lowered:
        return "email required|email is required"

    if "email not found" in lowered:
        return "email not found"

    if "confirmation message" in lowered and "reset email" in lowered:
        return "reset email was sent|confirmation"

    if "validation message" in lowered and "email" in lowered:
        return "email required|email is required|email not found"

    return None


def _start_url_from_given(given_text: str) -> str:
    lowered = given_text.lower()

    if "signup page" in lowered or "sign up page" in lowered or "signup" in lowered:
        return "http://localhost:3000/signup"

    if "dashboard page" in lowered or "dashboard" in lowered:
        return "http://localhost:3000/dashboard"

    if "password reset page" in lowered or "reset password page" in lowered:
        return "http://localhost:3000/reset-password"

    if "login page" in lowered or "login" in lowered:
        return "http://localhost:3000/login"

    if "home page" in lowered or "homepage" in lowered or "home" in lowered:
        return "http://localhost:3000/"

    return "http://localhost:3000"


def _action_lines_from_when(when_text: str) -> list[str]:
    lowered = when_text.lower()
    original = _normalize_phrase(when_text)

    if "clicks forgot password" in lowered:
        return [
            "  await page.getByRole('link', { name: /forgot password/i }).click();"
        ]

    if "without entering an email" in lowered and ("clicks sign up" in lowered or "clicks signup" in lowered):
        return [
            "  await page.getByRole('button', { name: /sign up|signup/i }).click();"
        ]

    if "clicks logout" in lowered:
        return [
            "  await page.getByRole('button', { name: /logout/i }).click();"
        ]

    if "clicks login" in lowered:
        if "enters valid credentials" in lowered:
            return [
                "  await page.getByLabel(/email/i).fill('test@example.com');",
                "  await page.getByLabel(/password/i).fill('ValidPassword123!');",
                "  await page.getByRole('button', { name: /login|sign in/i }).click();",
            ]
        return [
            "  await page.getByRole('button', { name: /login|sign in/i }).click();"
        ]

    if "enters a registered email and submits the form" in lowered:
        return [
            "  await page.getByLabel(/email/i).fill('registered@example.com');",
            "  await page.getByRole('button', { name: /reset password|submit/i }).click();",
        ]

    if "submits an unregistered email" in lowered:
        return [
            "  await page.getByLabel(/email/i).fill('unknown@example.com');",
            "  await page.getByRole('button', { name: /reset password|submit/i }).click();",
        ]

    if "submits" in lowered and "password reset" in lowered:
        return [
            "  await page.getByRole('button', { name: /reset password|submit/i }).click();"
        ]

    click_match = re.search(r"clicks?\s+(.+)$", original, re.IGNORECASE)
    if click_match:
        target = click_match.group(1).strip().strip(".")
        target = re.sub(r"\s+without.+$", "", target, flags=re.IGNORECASE).strip()
        target_escaped = _escape_js_string(target)
        return [
            f"  await page.getByRole('button', {{ name: /{target_escaped}/i }}).click();"
        ]

    return []


def _assertion_lines_from_then(then_text: str) -> list[str]:
    validation_regex = _validation_text_regex_from_then(then_text)
    if validation_regex:
        return [
            f"  await expect(page.getByText(/{validation_regex}/i)).toBeVisible();"
        ]

    route_regex = _route_regex_from_then(then_text)
    heading_regex = _heading_regex_from_then(then_text)

    lines = [f"  await expect(page).toHaveURL(/{route_regex}/i);"]

    if heading_regex:
        lines.append(
            f"  await expect(page.getByRole('heading', {{ name: /{heading_regex}/i }})).toBeVisible();"
        )

    return lines


def _scenario_test_name(index: int, feature_title: str, scenario: dict[str, str]) -> str:
    scenario_title = scenario.get("title") or f"{feature_title}_scenario_{index + 1}"
    return _slugify(scenario_title)


def generate_playwright_test(feature: dict[str, Any], scenarios: list[dict[str, str]]) -> dict[str, Any]:
    """Generate deterministic Playwright test code from one or more Gherkin scenarios."""
    feature_title = feature.get("title", "Generated feature")
    test_name = _slugify(feature_title)

    code_lines = [
        "import { test, expect } from '@playwright/test';",
        "",
    ]

    scenario_count = 0

    for index, scenario in enumerate(scenarios):
        given = scenario.get("given", "")
        when = scenario.get("when", "")
        then = scenario.get("then", "")

        scenario_test_name = _scenario_test_name(index, feature_title, scenario)
        start_url = _start_url_from_given(given)
        action_lines = _action_lines_from_when(when)
        assertion_lines = _assertion_lines_from_then(then)

        code_lines.append(f"test('{scenario_test_name}', async ({{ page }}) => {{")
        code_lines.append(f"  await page.goto('{start_url}');")
        code_lines.extend(action_lines)
        code_lines.extend(assertion_lines)
        code_lines.append("});")
        code_lines.append("")

        scenario_count += 1

    if scenario_count == 0:
        code_lines.append(f"test('{test_name}', async ({{ page }}) => {{")
        code_lines.append("  await page.goto('http://localhost:3000');")
        code_lines.append("});")
        code_lines.append("")

    test_code = "\n".join(code_lines)

    return {
        "test_name": test_name,
        "test_code": test_code,
        "line_count": len(test_code.splitlines()),
    }