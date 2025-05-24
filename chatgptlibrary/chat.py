from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Union
import html
from textwrap import dedent
import pandas as pd

from IPython.display import display, Markdown


class ChatFormatter:
    """Handles formatting of chat content for different output formats."""

    # pylint: disable=W0622

    def __init__(self, chat: "Chat"):
        self.chat = chat

    def _format_role(self, role: str) -> str:
        """Format role name with appropriate emoji."""
        role_display = role.capitalize()
        if role == "user":
            role_display = "👤 User"
        elif role == "assistant":
            role_display = "🤖 Assistant"
        elif role == "tool":
            role_display = "🛠️ Tool"
        return role_display

    def _format_metadata(self, format: str = "md") -> List[str]:
        """Format title and metadata according to the specified format."""
        if format == "html":
            return [
                f"<h1>{html.escape(self.chat.title)}</h1>",
                f"<p><em>Created: {self.chat.created.strftime('%Y-%m-%d %H:%M:%S')}</em></p>",
                f"<p><em>Updated: {self.chat.updated.strftime('%Y-%m-%d %H:%M:%S')}</em></p>",
                "<hr>",
            ]
        return [
            f"# {self.chat.title}",
            f"*Created: {self.chat.created.strftime('%Y-%m-%d %H:%M:%S')}*",
            f"*Updated: {self.chat.updated.strftime('%Y-%m-%d %H:%M:%S')}*",
            "---",
        ]

    def _format_message(
        self, role: str, messages: List[str], format: str = "md"
    ) -> List[str]:
        """Format a single message block according to the specified format."""
        if not messages:  # Skip empty messages
            return []

        role_display = self._format_role(role)
        formatted = []

        if format == "html":
            formatted.append(f"<h3>{html.escape(role_display)}</h3>")
            for message in messages:
                formatted.append(f"<div>{message}</div>")
            formatted.append("<hr>")
        else:
            formatted.append(f"### {role_display}")
            formatted.extend(messages)
            formatted.append("---")

        return formatted

    def get_formatted_content(self, format: str = "md") -> List[str]:
        """Get the complete formatted content of the chat."""
        content = self._format_metadata(format)

        for role, messages in self.chat.conversation:
            content.extend(self._format_message(role, messages, format))

        return content

    def get_html_template(self, content: List[str]) -> str:
        """Get the complete HTML document with the formatted content."""
        return dedent(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{html.escape(self.chat.title)}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    hr {{
                        border: none;
                        border-top: 1px solid #ccc;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
            {chr(10).join(content)}
            </body>
            </html>
        """
        ).strip()


class Chat:
    def __init__(
        self,
        title: str,
        conversation: List[Tuple[str, List[str]]],
        created: datetime,
        updated: datetime,
    ):
        self.title = title
        self.conversation = conversation
        self.created = created
        self.updated = updated

    def __repr__(self):
        return f"Chat('{self.title}')"

    @classmethod
    def from_series(cls, row: pd.Series) -> "Chat":
        """Create a Chat instance from a library row.

        Args:
            row: A pandas Series containing 'title', 'conversation',
                 'created', and 'updated' fields.

        Returns:
            A new Chat instance.
        """
        return cls(
            row["title"],
            row["conversation"],
            row["created"],
            row["updated"],
        )

    def display(self):
        """Display the chat conversation in Jupyter Notebook."""
        formatter = ChatFormatter(self)
        content = formatter.get_formatted_content("md")
        for line in content:
            display(Markdown(line))

    def export(
        self, filepath: Union[str, Path], format: str = None
    ) -> None:  # pylint: disable=W0622
        """Export the chat conversation to a file in the specified format.

        Args:
            filepath: Path where the file should be saved (string or Path object)
            format: Export format, one of "txt", "md", or "html".
                    If None, format is inferred from filepath extension.
        """
        # Convert string to Path if necessary
        path = Path(filepath) if isinstance(filepath, str) else filepath

        # Infer format from extension if not provided
        if format is None:
            format = path.suffix.lstrip(".").lower()
            if not format:  # If no extension, default to md
                format = "md"
                path = path.with_suffix(".md")

        if format not in ["txt", "md", "html"]:
            raise ValueError("Format must be one of: txt, md, html")

        formatter = ChatFormatter(self)
        content = formatter.get_formatted_content(format)

        # Write to file
        with open(path, "w", encoding="utf-8") as f:
            if format == "html":
                f.write(formatter.get_html_template(content))
            else:
                f.write(chr(10).join(content))
