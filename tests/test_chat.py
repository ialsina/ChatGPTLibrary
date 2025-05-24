"""
Tests for the Chat class and ChatFormatter.
"""

import pytest
from datetime import datetime
from pathlib import Path
from chatgptlibrary.chat import Chat, ChatFormatter


@pytest.fixture
def sample_chat():
    """Create a sample chat for testing."""
    return Chat(
        title="Test Chat",
        conversation=[
            ("user", ["Hello"]),
            ("assistant", ["Hi there!"]),
            ("tool", ["Tool response"]),
        ],
        created=datetime(2024, 1, 1),
        updated=datetime(2024, 1, 2),
    )


def test_chat_initialization(sample_chat):
    """Test Chat initialization and basic properties."""
    assert sample_chat.title == "Test Chat"
    assert len(sample_chat.conversation) == 3
    assert sample_chat.created == datetime(2024, 1, 1)
    assert sample_chat.updated == datetime(2024, 1, 2)


def test_chat_repr(sample_chat):
    """Test Chat string representation."""
    assert repr(sample_chat) == "Chat('Test Chat')"


def test_chat_formatter_markdown(sample_chat):
    """Test ChatFormatter markdown output."""
    formatter = ChatFormatter(sample_chat)
    content = formatter.get_formatted_content("md")

    # Check metadata
    assert "# Test Chat" in content
    assert "*Created: 2024-01-01 00:00:00*" in content
    assert "*Updated: 2024-01-02 00:00:00*" in content

    # Check conversation
    assert "### 👤 User" in content
    assert "Hello" in content
    assert "### 🤖 Assistant" in content
    assert "Hi there!" in content
    assert "### 🛠️ Tool" in content
    assert "Tool response" in content


def test_chat_formatter_html(sample_chat):
    """Test ChatFormatter HTML output."""
    formatter = ChatFormatter(sample_chat)
    content = formatter.get_formatted_content("html")

    # Check metadata
    assert "<h1>Test Chat</h1>" in content
    assert "<p><em>Created: 2024-01-01 00:00:00</em></p>" in content
    assert "<p><em>Updated: 2024-01-02 00:00:00</em></p>" in content

    # Check conversation
    assert "<h3>👤 User</h3>" in content
    assert "<div>Hello</div>" in content
    assert "<h3>🤖 Assistant</h3>" in content
    assert "<div>Hi there!</div>" in content
    assert "<h3>🛠️ Tool</h3>" in content
    assert "<div>Tool response</div>" in content


def test_chat_export(sample_chat, tmp_path):
    """Test Chat export functionality."""
    # Test markdown export
    md_path = tmp_path / "test.md"
    sample_chat.export(md_path)
    assert md_path.exists()
    content = md_path.read_text()
    assert "# Test Chat" in content

    # Test HTML export
    html_path = tmp_path / "test.html"
    sample_chat.export(html_path)
    assert html_path.exists()
    content = html_path.read_text()
    assert "<!DOCTYPE html>" in content
    assert "<h1>Test Chat</h1>" in content

    # Test invalid format
    with pytest.raises(ValueError):
        sample_chat.export(tmp_path / "test.xyz", format="xyz")
