# QA RAG Agent

A Python-based QA RAG Agent that converts Jira-style user stories or requirement text into:
- masked requirement text,
- structured Gherkin scenarios,
- and generated Playwright test code.

This project is built as a practical QA automation portfolio project focused on turning requirement inputs into traceable, executable test assets.

## Features

- Accepts requirement text through a FastAPI endpoint.
- Detects and masks sensitive PII such as email addresses and phone numbers before downstream processing.
- Extracts acceptance criteria into structured Gherkin scenarios.
- Supports both single-scenario and multi-scenario stories.
- Generates rule-based Playwright tests from the extracted scenarios.
- Produces route-aware and assertion-aware Playwright output for common flows like login, signup, logout, password reset, and validation messaging.

## Tech stack

- Python
- FastAPI
- Pydantic
- Microsoft Presidio
- Playwright
- Uvicorn

## Project structure

```text
src/qa_rag_agent/
├── api/                  # FastAPI app, routes, schemas
├── generation/           # Playwright test generation
├── gherkin/              # Requirement-to-Gherkin transformation
├── ingestion/            # Jira story or raw requirement ingestion
├── pii/                  # PII masking with Presidio
├── prompts/              # Prompt templates for future LLM-based generation
├── reports/              # Report assembly
└── retrieval/            # Retrieval and future RAG components

artifacts/
├── feature_files/        # Generated .feature outputs
├── playwright_tests/     # Generated Playwright tests
├── logs/                 # Runtime logs
├── screenshots/          # Screenshots for debugging or reporting
├── traces/               # Playwright traces
└── reports/              # Final reports and summaries
```

## Current status

The MVP is working end to end for the following flow:

1. Input story text.
2. Mask PII.
3. Generate Gherkin scenarios.
4. Generate Playwright test code.

Validated story patterns include:
- password reset navigation,
- login success flow,
- signup validation for missing email,
- logout flow,
- multi-scenario password reset stories.

## Run locally

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI app

From the project root:

```powershell
$env:PYTHONPATH="src"; uvicorn qa_rag_agent.api.app:app --reload
```

### 4. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

## Example request

Use this in Swagger for `/api/process-story`:

```json
{
  "story_text": "Story ID: QA-105\nTitle: User should be able to reset password and recover account access\nAcceptance Criteria:\n1. Given the user is on the login page, when the user clicks Forgot Password, then the user should be navigated to the password reset page.\n2. Given the user is on the password reset page, when the user enters a registered email and submits the form, then the user should see a confirmation message that the reset email was sent.\n3. Given the user is on the password reset page, when the user submits an unregistered email, then the user should see an email not found validation message.\nReporter Email: rahul.sharma@example.com"
}
```

## Example output

The API returns JSON with:
- `masking`
- `gherkin`
- `playwright`

Example generated outcomes include:
- multiple Gherkin scenarios from one story,
- one Playwright test per scenario,
- route-aware navigation such as `/login`, `/signup`, `/dashboard`, and `/reset-password`,
- assertions for visible headings, redirects, and validation messages.

## Why this project matters

This project demonstrates:
- requirements-to-test automation,
- deterministic rule-based QA generation,
- PII-safe preprocessing,
- structured scenario extraction,
- and executable browser test generation.

It is designed as a stepping stone toward a richer agentic QA system with retrieval, traceability, and LLM-assisted test generation.

## Next improvements

- Add Jira API ingestion.
- Save generated Gherkin and Playwright outputs as files in `artifacts/`.
- Add execution support for generated Playwright tests.
- Add retrieval-based context grounding for requirements and existing test assets.
- Add LLM-backed fallback generation for more complex story patterns.

## License

MIT