# Contributing to Marketing Agent

Thank you for your interest in contributing to Marketing Agent! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- API keys for testing (Groq, OpenAI, Tavily)

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR_USERNAME/Marketing-Agent.git
   cd Marketing-Agent
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r code/requirements.txt
   pip install -r code/requirements-dev.txt  # Development tools
   ```

4. **Configure Environment**

   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

5. **Run Tests**
   ```bash
   pytest code/tests/
   ```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Changes

- Write clear, concise code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 3. Code Quality

**Format Code**

```bash
black code/
ruff check code/ --fix
```

**Run Tests**

```bash
pytest code/tests/ -v
```

**Type Checking**

```bash
mypy code/
```

### 4. Commit Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add video quality validation"
git commit -m "fix: resolve JSON parsing error in ideation"
git commit -m "docs: update API documentation"
```

Commit types:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- Clear title and description
- Reference any related issues
- Screenshots/examples if applicable

## 🧪 Testing Guidelines

### Writing Tests

```python
# code/tests/test_your_feature.py
import pytest
from api.services.your_service import YourService

def test_your_feature():
    service = YourService()
    result = service.do_something()
    assert result == expected_value
```

### Test Categories

- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete workflows

### Running Specific Tests

```bash
# Run specific test file
pytest code/tests/test_brand_context.py

# Run specific test
pytest code/tests/test_brand_context.py::test_color_palette

# Run with coverage
pytest --cov=code/api code/tests/
```

## 📚 Documentation

### Code Documentation

Use docstrings for all public functions/classes:

```python
def generate_campaign(project_id: str, num_ideas: int = 15) -> CampaignResult:
    """
    Generate marketing campaign ideas.

    Args:
        project_id: Unique project identifier
        num_ideas: Number of ideas to generate (default: 15)

    Returns:
        CampaignResult with generated ideas and metadata

    Raises:
        ValueError: If num_ideas < 1
        AIProviderError: If AI generation fails
    """
    pass
```

### README Updates

Update README.md when adding:

- New features
- Configuration options
- API changes
- Usage examples

## 🎨 Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use descriptive variable names

### Example

```python
from typing import List, Dict, Optional

async def process_ideas(
    ideas: List[Dict[str, str]],
    brand_context: Optional[BrandContext] = None
) -> List[ProcessedIdea]:
    """Process raw ideas with brand context."""
    processed = []

    for idea in ideas:
        if brand_context:
            idea = apply_branding(idea, brand_context)
        processed.append(ProcessedIdea(**idea))

    return processed
```

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Verify it's reproducible
3. Test with latest version

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**

1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**

- OS: [e.g., Windows 11]
- Python: [e.g., 3.11.5]
- Version: [e.g., 1.0.0]

**Additional Context**
Logs, screenshots, etc.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other approaches considered

**Additional Context**
Examples, mockups, etc.
```

## 🔍 Code Review Process

### What We Look For

- ✅ Code quality and style
- ✅ Test coverage
- ✅ Documentation
- ✅ Performance impact
- ✅ Breaking changes
- ✅ Security considerations

### Review Timeline

- Initial review: 1-3 business days
- Follow-up reviews: 1-2 business days

## 📦 Release Process

1. Version bump in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release PR
4. Merge to main
5. Tag release
6. Publish to PyPI (if applicable)

## 🙏 Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Questions?

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs and features
- **Email**: dev@ai-whisperers.com

---

Thank you for contributing to Marketing Agent! 🎉
