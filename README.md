# ChatGPTLibrary

A Python package to compile, manage, and search conversations exported from ChatGPT.

## Features
- Load conversations from ChatGPT's exported JSON file
- Search conversations by message content
- Simple pandas-based interface
- Interactive display of conversations in Jupyter Notebooks
- Individual chat access with rich formatting
- Export conversations in multiple formats (txt, md, html)

## Installation

```bash
pip install .
```

## Usage

```python
from chatgptlibrary import ChatLibrary

# Initialize from a ChatGPT JSON export
lib = ChatLibrary('conversations.json')

# Search for messages containing a string
results = lib.grep('python')

# Access titles
print(results.title)

# Access conversations
print(results.conversation)

# Get a single chat and display it in Jupyter Notebook
chat = lib[0]  # Get first chat by index
chat = lib["My Conversation"]  # Get chat by title
chat.show()    # Display with rich formatting

# Search with multiple terms
# All terms must match
results = lib.grepall('python', 'data')

# Any term can match
results = lib.grepany('python', 'data')

# Export conversations
chat.export('conversation.md')  # Export as markdown (default)
chat.export('conversation.html')  # Export as HTML
chat.export('conversation.txt')  # Export as plain text
chat.export('conversation', format='html')  # Explicitly specify format
```

## Export Formats

The library supports exporting conversations in three formats:

- **Markdown** (default): Preserves formatting and is readable in any text editor
- **HTML**: Includes styling and is perfect for web viewing
- **Plain Text**: Simple text format for basic viewing

The format is automatically detected from the file extension, but can also be explicitly specified using the `format` parameter.
