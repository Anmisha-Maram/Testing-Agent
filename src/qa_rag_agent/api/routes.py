from fastapi import APIRouter
from qa_rag_agent.api.schemas import StoryInput
from qa_rag_agent.gherkin.generator import generate_gherkin
from qa_rag_agent.generation.playwright_generator import generate_playwright_test
from qa_rag_agent.pii.masker import mask_pii


router = APIRouter(prefix="/api", tags=["qa-rag-agent"])


@router.post("/process-story")
def process_story(payload: StoryInput):
    text = payload.story_text

    masked = mask_pii(text)
    gherkin = generate_gherkin(masked["masked_text"])
    playwright = generate_playwright_test(
        gherkin["feature"],
        gherkin["scenarios"],
    )

    return {
        "story_text": text,
        "masking": masked,
        "gherkin": gherkin,
        "playwright": playwright,
    }