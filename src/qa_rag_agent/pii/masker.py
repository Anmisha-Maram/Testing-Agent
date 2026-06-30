"""Minimal PII detection and masking utilities using Microsoft Presidio."""

from __future__ import annotations

from typing import Any

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

ALLOWED_ENTITY_TYPES = {
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
}

ALLOW_LIST = [
    "login",
    "signup",
    "sign up",
    "dashboard",
    "forgot password",
    "reset password",
    "email",
    "phone",
    "reporter",
]

FIELD_LABELS_TO_IGNORE = {
    "email",
    "phone",
    "reporter",
}


def _is_valid_entity(result: Any, text: str) -> bool:
    entity_text = text[result.start:result.end].strip()
    entity_type = result.entity_type

    if entity_type not in ALLOWED_ENTITY_TYPES:
        return False

    if entity_text.lower() in FIELD_LABELS_TO_IGNORE:
        return False

    return True


def mask_pii(text: str) -> dict[str, Any]:
    """Detect and mask selected PII entities in the provided text.

    Returns a JSON-serializable dictionary with the original text, masked text,
    detected entities, and the total count of detected entities.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    results = analyzer.analyze(
        text=text,
        language="en",
        allow_list=ALLOW_LIST,
    )

    filtered_results = [result for result in results if _is_valid_entity(result, text)]

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=filtered_results,
    )

    entities_detected = [
        {
            "entity_type": result.entity_type,
            "start": result.start,
            "end": result.end,
            "score": result.score,
            "text": text[result.start:result.end],
        }
        for result in filtered_results
    ]

    return {
        "original_text": text,
        "masked_text": anonymized_result.text,
        "entities_detected": entities_detected,
        "entity_count": len(entities_detected),
    }