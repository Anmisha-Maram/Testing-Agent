import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qa_rag_agent.gherkin.generator import generate_gherkin


def test_generate_gherkin_from_acceptance_criteria():
    requirement_text = """Story Title: Login Flow

Description:
As a user, I want to log in so that I can access my account.

Acceptance Criteria:
1. The user can enter valid credentials.
2. The system displays a welcome message after login.
"""

    result = generate_gherkin(requirement_text)

    assert result["feature"]["title"] == "Login Flow"
    assert result["scenario_count"] == 2
    assert len(result["scenarios"]) == 2
    assert "Feature:" in result["raw_gherkin_text"]
    assert "Scenario:" in result["raw_gherkin_text"]


def test_generate_gherkin_fallback_when_no_acceptance_criteria():
    requirement_text = """Story Title: Password Reset

Description:
As a customer, I want to reset my password so that I can regain access to my account.
"""

    result = generate_gherkin(requirement_text)

    assert result["scenario_count"] == 1
    assert len(result["scenarios"]) == 1
    assert result["scenarios"][0]["title"] == "Password reset request"


def test_generate_gherkin_extracts_title_from_jira_style_story():
    requirement_text = """Story ID: QA-101
Title: Password reset email flow should work for registered users

Description:
The system should allow a registered user to request a password reset link from the login page.

Acceptance Criteria:
1. Given the user is on the login page, when the user clicks \"Forgot Password\", then the user should be navigated to the password reset page.
"""

    result = generate_gherkin(requirement_text)

    assert result["feature"]["title"] == "Password reset email flow should work for registered users"
    assert result["scenario_count"] == 1
    assert "Given the user is on the login page" in result["raw_gherkin_text"]
    assert "Given Given" not in result["raw_gherkin_text"]
