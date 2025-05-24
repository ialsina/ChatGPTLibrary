# ChatGPTLibrary

A Python package to compile, manage, and search conversations exported from ChatGPT.

## Features
- Load conversations from ChatGPT's exported JSON file
- Search conversations by message content
- Simple pandas-based interface

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
```
