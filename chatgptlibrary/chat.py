from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from IPython.display import display, Markdown


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

    def display(self):
        """Display the chat conversation in Jupyter Notebook."""
        # Display title and metadata
        display(Markdown(f"# {self.title}"))
        display(Markdown(f"*Created: {self.created.strftime('%Y-%m-%d %H:%M:%S')}*"))
        display(Markdown(f"*Updated: {self.updated.strftime('%Y-%m-%d %H:%M:%S')}*"))
        display(Markdown("---"))

        # Display conversation
        for role, messages in self.conversation:
            if not messages:  # Skip empty messages
                continue

            # Format role name
            role_display = role.capitalize()
            if role == "user":
                role_display = "👤 User"
            elif role == "assistant":
                role_display = "🤖 Assistant"
            elif role == "tool":
                role_display = "🛠️ Tool"

            # Display role and messages
            display(Markdown(f"### {role_display}"))
            for message in messages:
                display(Markdown(message))
            display(Markdown("---"))
