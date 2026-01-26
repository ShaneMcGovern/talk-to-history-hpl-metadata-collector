"""Tests for build_search_query function."""

from collector import build_search_query


def test_build_search_query():
    """Test that build_search_query returns a properly formatted query string."""
    result = build_search_query("bdr:test123", "autograph letter")

    assert 'rel_is_member_of_collection_ssim:"bdr:test123"' in result
    assert 'genre_local:"autograph letter"' in result
    assert 'mods_role_creator_ssim:"Lovecraft, H.P. (Howard Phillips)"' in result
    assert (
        'mods_access_condition_rights_text_tsim:"No Copyright - United States."'
        in result
    )
    assert (
        'mods_access_condition_restriction_text_tsim:"Collection is open for research."'
        in result
    )
    assert result.count(" AND ") == 4
