import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qa_rag_agent.ingestion.reader import read_text_file
from qa_rag_agent.pii.masker import mask_pii


def test_read_text_file_reads_utf8(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Hello world", encoding="utf-8")

    assert read_text_file(str(sample_file)) == "Hello world"


def test_read_text_file_raises_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        read_text_file(str(missing_file))


def test_mask_pii_returns_serializable_result():
    text = "Contact Jane at jane.doe@example.com or +1 415 555 0147."

    result = mask_pii(text)

    assert result["masked_text"] != text
    assert result["entity_count"] >= 2
    assert isinstance(result["entities_detected"], list)
    assert json.loads(json.dumps(result)) == result
