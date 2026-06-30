from typing import Any, List

from pydantic import BaseModel, Field


class StoryInput(BaseModel):
    """Input payload for a story or requirement text."""
    

    story_text: str = Field(..., description="Raw Jira story or requirement text")


class MaskingOutput(BaseModel):
    """Output of the PII masking step."""

    original_text: str
    masked_text: str
    entities_detected: List[dict[str, Any]]
    entity_count: int


class GherkinOutput(BaseModel):
    """Output of the Gherkin generation step."""

    feature: dict[str, str]
    scenarios: List[dict[str, str]]
    scenario_count: int
    raw_gherkin_text: str


class PlaywrightOutput(BaseModel):
    """Output of the Playwright draft generation step."""

    test_name: str
    test_code: str
    line_count: int
