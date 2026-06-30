# QA RAG Agent

A Python-based QA RAG Agent that converts Jira-style user stories or requirement text into:

- masked requirement text,
- structured Gherkin scenarios,
- generated Playwright test code.

This project is built as a practical QA automation portfolio project focused on turning requirement inputs into traceable, executable test assets.

## Features

- Accepts requirement text through a FastAPI endpoint.
- Detects and masks sensitive PII such as email addresses and phone numbers before downstream processing.
- Extracts acceptance criteria into structured Gherkin scenarios.
- Supports both single-scenario and multi-scenario stories.
- Generates rule-based Playwright tests from the extracted scenarios.
- Produces route-aware and assertion-aware Playwright output for common flows like login, signup, logout, password reset, and validation messaging.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Microsoft Presidio
- Playwright
- Uvicorn

## Project Structure

```text
src/qa_rag_agent/
├── api/                # FastAPI app, routes, schemas
├── generation/         # Playwright test generation
├── gherkin/            # Requirement-to-Gherkin transformation
├── ingestion/          # Jira story or raw requirement ingestion
├── pii/                # PII masking with Presidio
├── prompts/            # Prompt templates for future LLM-based generation
├── reports/            # Report assembly
└── retrieval/          # Retrieval and future RAG components

artifacts/
├── feature_files/      # Generated .feature outputs
├── playwright_tests/   # Generated Playwright tests
├── logs/               # Runtime logs
├── screenshots/        # Screenshots for debugging or reporting
├── traces/             # Playwright traces
└── reports/            # Final reports and summaries
```

## Current Status

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

## Run Locally

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
$env:PYTHONPATH="src"
uvicorn qa_rag_agent.api.app:app --reload
```

### 4. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

## Example Request

Use this in Swagger for `/api/process-story`:

```json
{
  "story_text": "Story ID: QA-105\nTitle: User should be able to reset password and recover account access\nAcceptance Criteria:\n1. Given the user is on the login page, when the user clicks Forgot Password, then the user should be navigated to the password reset page.\n2. Given the user is on the password reset page, when the user enters a registered email and submits the form, then the user should see a confirmation message that the reset email was sent.\n3. Given the user is on the password reset page, when the user submits an unregistered email, then the user should see an email not found validation message.\nReporter Email: rahul.sharma@example.com"
}
```

## Sample Requests

Ready-to-use sample request bodies are available in the `samples/` folder:

- `samples/qa-103.json`
- `samples/qa-104.json`
- `samples/qa-105.json`

## Example Output

The API returns a structured JSON response containing:

- the original story text,
- masked text,
- detected PII entities,
- generated Gherkin scenarios,
- and Playwright test code.

## Screenshots

<img width="1335" height="949" alt="image" src="https://github.com/user-attachments/assets/101ca6a7-a287-442d-8368-0bd248c0a018" />


## Next Phase

Planned next improvements:

- Add ChromaDB-backed retrieval for requirement and test context.
- Generate richer Playwright scripts using retrieved examples.
- Add execution pipeline support for running generated tests on real demo applications.
- Expand toward a full agentic QA workflow with reporting and traceability.

## License

This project is for portfolio and learning purposes.
