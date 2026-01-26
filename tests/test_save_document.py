"""Tests for save_document function."""

import json

from collector import save_document


def test_save_document(tmp_path):
    """Test that save_document creates a JSON file with correct name and content."""
    doc = {"pid": "bdr:12345", "title": "Test Document"}

    filepath = save_document(doc, str(tmp_path))

    assert filepath == f"{tmp_path}/12345.json"
    with open(filepath, encoding="utf-8") as f:
        assert json.load(f) == doc
