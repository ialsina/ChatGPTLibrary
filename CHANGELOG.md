# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Core `Chat` class for handling individual ChatGPT conversations
- Support for reading and parsing ChatGPT conversation JSON files
- Support for reading conversations from ZIP archives
- Conversation filtering and search functionality with `grepall()` and `grepany()` methods
- Multiple export formats support (txt, md, html) with rich formatting
- Jupyter Notebook integration with `display()` method
- Modern Python packaging with pyproject.toml
- Automatic version management using setuptools_scm