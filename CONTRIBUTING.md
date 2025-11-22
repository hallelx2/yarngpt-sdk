# Contributing to YarnGPT SDK

Thank you for your interest in contributing to the YarnGPT SDK!

## Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/your-username/yarngpt-sdk.git
cd yarngpt-sdk
```

2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install development dependencies
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=yarngpt --cov-report=html

# Run specific test file
pytest tests/test_yarngpt.py -v
```

## Code Style

We use `black` for code formatting and `ruff` for linting:

```bash
# Format code
black yarngpt/ tests/ examples/

# Check linting
ruff check yarngpt/ tests/ examples/

# Type checking
mypy yarngpt/
```

## Pull Request Process

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Make your changes
3. Add/update tests as needed
4. Ensure all tests pass
5. Format your code with `black`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code of Conduct

Be respectful and inclusive. We're building this for the community!
