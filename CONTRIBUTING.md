# Contributing to Anyparser Core

First off, thank you for considering contributing to Anyparser Core! It's people like you that make Anyparser Core such a great tool for AI data preparation.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include any error messages or stack traces**

> **Note:** When reporting bugs, do not include any sensitive information or API keys.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the behavior you expected to see**
* **Explain why this enhancement would be useful for AI data preparation**

### Pull Requests

* Fork the repo and create your branch from `main`
* If you've added code that should be tested, add tests
* If you've changed APIs, update the documentation
* Ensure the test suite passes
* Make sure your code lints
* Issue that pull request!

## Development Process

1. Fork the repository
2. Create a new branch for your feature or bugfix: `git checkout -b feature-name`
3. Make your changes
4. Write or update tests as needed
5. Run the test suite
6. Push to your fork and submit a pull request

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/anyparser_core.git
cd anyparser_core

# Prerequisites
# Make sure you have Poetry installed on your system
# Visit https://python-poetry.org/docs for installation instructions

# Install dependencies (including dev dependencies)
make install-dev

# Or alternatively using Poetry directly:
poetry install --with dev
```

### Running Tests

```bash
# Run tests with verbose output
make test

# Run tests with coverage report
make coverage

# View coverage report in browser
make coverage-view
```

### Code Style

We use the following tools to maintain code quality:

* **Black** for code formatting

Please ensure your code passes all linting checks:

```bash
# Format code with Black
make lint
```

## Documentation

* Keep docstrings up to date
* Follow Google-style docstring format
* Update README.md if needed
* Add examples for new features

## Core Focus Areas

We especially welcome contributions in these areas:

1. **AI Data Preparation Enhancements**
   - Improvements to RAG-focused features
   - Better support for AI model training data extraction
   - Enhanced structured data extraction

2. **Performance Optimizations**
   - Speed improvements for large document processing
   - Memory usage optimizations
   - Batch processing enhancements

3. **New Model Support**
   - Integration with new OCR models
   - Support for additional document types
   - Enhanced language support

4. **Documentation and Examples**
   - Better examples for AI/ML use cases
   - Improved API documentation
   - Tutorial content

## Community

* Join our [Community Discussions](https://github.com/anyparser/anyparser_core/discussions)
* Follow our [GitHub repository](https://github.com/anyparser/anyparser_core)
* Check out our [Documentation](https://docs.anyparser.com)

## License

By contributing to Anyparser Core, you agree that your contributions will be licensed under its Apache-2.0 license.
