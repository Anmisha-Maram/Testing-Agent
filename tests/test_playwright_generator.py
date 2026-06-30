import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qa_rag_agent.generation.playwright_generator import generate_playwright_test


def test_generate_playwright_test_from_gherkin():
    gherkin_text = """Feature: Password reset

Scenario: Reset link is sent
  Given the user is on the login page
  When the user requests a reset link
  Then the system sends a reset email
"""

    result = generate_playwright_test(gherkin_text)

    assert result["test_name"] == "password_reset"
    assert result["line_count"] > 5
    assert "test('password_reset'" in result["test_code"]
    assert "page.goto" in result["test_code"]
