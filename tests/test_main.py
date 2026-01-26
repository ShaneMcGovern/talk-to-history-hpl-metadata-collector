"""Tests for main function."""

from unittest.mock import call, patch

from collector import GENRES, main


@patch("collector.fetch_and_save_documents")
def test_main(mock_fetch):
    """Test that main processes all genres in order."""
    main()

    assert mock_fetch.call_count == len(GENRES)
    mock_fetch.assert_has_calls([call(genre) for genre in GENRES])
