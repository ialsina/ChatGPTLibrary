"""
Tests for the ChatLibrary class.
"""

import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path
from chatgptlibrary.chatlibrary import ChatLibrary


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame(
        {
            "title": ["Chat 1", "Chat 2"],
            "conversation": [
                [("user", ["Hello"]), ("assistant", ["Hi"])],
                [("user", ["How are you?"]), ("assistant", ["I'm good!"])],
            ],
            "created": [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            "updated": [datetime(2024, 1, 1), datetime(2024, 1, 2)],
        }
    )


def test_chatlibrary_initialization(sample_data):
    """Test ChatLibrary initialization with DataFrame."""
    library = ChatLibrary(sample_data)
    assert len(library) == 2
    assert library.title == ["Chat 1", "Chat 2"]


def test_chatlibrary_getitem(sample_data):
    """Test ChatLibrary indexing."""
    library = ChatLibrary(sample_data)

    # Test integer indexing
    chat = library[0]
    assert chat.title == "Chat 1"

    # Test string indexing
    chat = library["Chat 2"]
    assert chat.title == "Chat 2"

    # Test slice indexing
    subset = library[0:1]
    if isinstance(subset, ChatLibrary):
        assert len(subset) == 1
        assert subset.title == ["Chat 1"]
    else:
        assert subset.title == "Chat 1"

    # Test list indexing
    subset = library[[0, 1]]
    if isinstance(subset, ChatLibrary):
        assert len(subset) == 2
        assert subset.title == ["Chat 1", "Chat 2"]
    else:
        assert subset.title in ["Chat 1", "Chat 2"]


def test_chatlibrary_grep(sample_data):
    """Test ChatLibrary grep functionality."""
    library = ChatLibrary(sample_data)

    # Test single grep
    result = library.grep("Hello")
    assert len(result) == 1
    assert result.title == ["Chat 1"]

    # Test grepall
    result = library.grepall("Hello", "Hi")
    assert len(result) == 1
    assert result.title == ["Chat 1"]

    # Test grepany
    result = library.grepany("Hello", "How are you?")
    assert len(result) == 2
    assert sorted(result.title) == ["Chat 1", "Chat 2"]


def test_chatlibrary_invalid_initialization():
    """Test ChatLibrary initialization with invalid data."""
    with pytest.raises(TypeError):
        ChatLibrary(123)  # Invalid type

    with pytest.raises(ValueError):
        # Invalid DataFrame columns
        ChatLibrary(pd.DataFrame({"invalid": [1, 2]}))


def test_chatlibrary_invalid_indexing(sample_data):
    """Test ChatLibrary invalid indexing."""
    library = ChatLibrary(sample_data)

    with pytest.raises(TypeError):
        library[1.5]  # Invalid index type

    with pytest.raises(KeyError):
        library["Non-existent Chat"]  # Non-existent title
