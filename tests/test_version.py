"""
Tests for version-related functionality.
"""

from chatgptlibrary import __version__


def test_version():
    """Test that version is a string."""
    assert isinstance(__version__, str)
    assert len(__version__) > 0
