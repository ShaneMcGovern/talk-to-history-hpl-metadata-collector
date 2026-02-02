"""Tests for has_single_matching_creator function."""

from collector import has_single_matching_creator


def test_has_single_matching_creator_success():
    """Test that function returns True for single matching creator."""
    doc = {"creator": ["Lovecraft, H.P. (Howard Phillips)"]}

    assert has_single_matching_creator(doc, "Lovecraft, H.P. (Howard Phillips)") is True


def test_has_single_matching_creator_no_match():
    """Test that function returns False for non-matching or missing creator."""
    # Missing creator field
    assert has_single_matching_creator({}, "Lovecraft, H.P. (Howard Phillips)") is False

    # Wrong name
    assert (
        has_single_matching_creator(
            {"creator": ["Smith, John"]}, "Lovecraft, H.P. (Howard Phillips)"
        )
        is False
    )

    # Multiple creators
    assert (
        has_single_matching_creator(
            {"creator": ["Lovecraft, H.P. (Howard Phillips)", "Smith, John"]},
            "Lovecraft, H.P. (Howard Phillips)",
        )
        is False
    )
