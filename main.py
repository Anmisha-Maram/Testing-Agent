from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from qa_rag_agent.gherkin.generator import generate_gherkin
from qa_rag_agent.generation.playwright_generator import generate_playwright_test
from qa_rag_agent.ingestion.reader import read_text_file
from qa_rag_agent.pii.masker import mask_pii


def main() -> None:
    """Read a sample story, mask PII, generate Gherkin, and save the outputs."""
    input_path = ROOT / "uploads" / "sample_story.txt"
    pii_output_path = ROOT / "artifacts" / "reports" / "pii_masked_output.json"
    feature_output_path = ROOT / "artifacts" / "feature_files" / "generated.feature"
    gherkin_output_path = ROOT / "artifacts" / "reports" / "gherkin_output.json"
    playwright_output_path = ROOT / "artifacts" / "playwright_tests" / "generated.spec.ts"
    playwright_report_path = ROOT / "artifacts" / "reports" / "playwright_output.json"

    text = read_text_file(str(input_path))
    pii_result = mask_pii(text)
    gherkin_result = generate_gherkin(pii_result["masked_text"])
    playwright_result = generate_playwright_test(gherkin_result["raw_gherkin_text"])

    pii_output_path.parent.mkdir(parents=True, exist_ok=True)
    pii_output_path.write_text(json.dumps(pii_result, indent=2), encoding="utf-8")

    feature_output_path.parent.mkdir(parents=True, exist_ok=True)
    feature_output_path.write_text(gherkin_result["raw_gherkin_text"], encoding="utf-8")

    gherkin_output_path.write_text(json.dumps(gherkin_result, indent=2), encoding="utf-8")

    playwright_output_path.parent.mkdir(parents=True, exist_ok=True)
    playwright_output_path.write_text(playwright_result["test_code"], encoding="utf-8")
    playwright_report_path.write_text(json.dumps(playwright_result, indent=2), encoding="utf-8")

    print(gherkin_result["raw_gherkin_text"])
    print("\nGenerated Playwright draft:")
    print(playwright_result["test_code"])


if __name__ == "__main__":
    main()
