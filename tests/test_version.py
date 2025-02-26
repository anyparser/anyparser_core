"""
Test version information
"""

from anyparser_core import __version__


def test_version():
    """Test version is a string."""
    assert isinstance(__version__, str)
    assert __version__ == "1.0.2"
