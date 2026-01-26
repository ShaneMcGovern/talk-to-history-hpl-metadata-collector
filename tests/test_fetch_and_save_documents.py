"""Tests for fetch_and_save_documents function."""

from unittest.mock import MagicMock, patch

import requests

from collector import fetch_and_save_documents


@patch("collector.save_document")
@patch("collector.requests.get")
def test_fetch_and_save_documents_success(mock_get, mock_save):
    """Test that documents are fetched and saved with pagination."""
    page1 = MagicMock(status_code=200)
    page1.json.return_value = {
        "response": {"docs": [{"pid": "bdr:1"}, {"pid": "bdr:2"}]}
    }
    empty = MagicMock(status_code=200)
    empty.json.return_value = {"response": {"docs": []}}
    mock_get.side_effect = [page1, empty]

    fetch_and_save_documents("autograph letter")

    assert mock_save.call_count == 2
    assert mock_get.call_count == 2


@patch("collector.save_document")
@patch("collector.requests.get")
def test_fetch_and_save_documents_empty_response(mock_get, mock_save):
    """Test that loop stops when no documents are returned."""
    empty = MagicMock(status_code=200)
    empty.json.return_value = {"response": {"docs": []}}
    mock_get.return_value = empty

    fetch_and_save_documents("typed letter")

    mock_save.assert_not_called()


@patch("collector.save_document")
@patch("collector.requests.get")
def test_fetch_and_save_documents_http_error(mock_get, mock_save):
    """Test that HTTP errors are handled."""
    mock_get.return_value = MagicMock(status_code=500)

    fetch_and_save_documents("autograph letter")

    mock_save.assert_not_called()


@patch("collector.save_document")
@patch("collector.requests.get")
def test_fetch_and_save_documents_network_error(mock_get, mock_save):
    """Test that network and parsing errors are handled."""
    mock_get.side_effect = requests.RequestException("Connection error")

    fetch_and_save_documents("autograph letter")

    mock_save.assert_not_called()
