# Contributing to Homeus

Thank you for your interest in contributing to Homeus! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Operating system and Python version
   - Configuration details (without sensitive data)
   - Error messages and logs
   - Steps to reproduce

### Suggesting Features

1. **Check the roadmap** in README.md
2. **Open a discussion** before creating an issue
3. **Explain the use case** and benefits
4. **Consider implementation complexity**

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/homeus.git
cd homeus

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Copy example config
cp config/config.example.yaml config/config.yaml
```

## 📝 Code Style

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### Example:

```python
def extract_property_price(price_text: str) -> Optional[int]:
    """
    Extract numeric price from text string.

    Args:
        price_text: Raw price text from webpage

    Returns:
        Extracted price as integer, or None if not found
    """
    if not price_text:
        return None

    match = re.search(r'(\d+(?:,\d{3})*)', price_text.replace(' ', ''))
    return int(match.group(1).replace(',', '')) if match else None
```

### Configuration

- Use **YAML** for configuration files
- Provide **example configurations**
- Document all configuration options
- Use **environment variables** for sensitive data

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_scrapers.py

# Run with coverage
python -m pytest --cov=src
```

### Writing Tests

- Write tests for **new functionality**
- Include **edge cases** and **error conditions**
- Use **descriptive test names**
- Mock external dependencies

### Example Test:

```python
def test_extract_property_price():
    """Test price extraction from various formats."""
    assert extract_property_price("$75,000") == 75000
    assert extract_property_price("75000 USD") == 75000
    assert extract_property_price("invalid") is None
    assert extract_property_price("") is None
```

## 🏗️ Architecture Guidelines

### Adding New Scrapers

1. **Inherit from BaseScraper**
2. **Implement required methods**
3. **Handle errors gracefully**
4. **Respect rate limits**
5. **Add comprehensive tests**

```python
class NewSiteScraper(BaseScraper):
    def scrape_listings(self, search_url: str) -> List[Property]:
        # Implementation
        pass

    def scrape_property_details(self, property_url: str) -> Optional[Property]:
        # Implementation
        pass
```

### Database Changes

- Use **migrations** for schema changes
- Maintain **backward compatibility**
- Document schema changes
- Test with existing data

### Configuration Changes

- Update **example configuration**
- Document new options
- Provide **sensible defaults**
- Maintain backward compatibility

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Configuration examples updated
- [ ] No sensitive data in commits

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] Configuration tested

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data included
```

## 🚨 Security Guidelines

### Sensitive Data

- **Never commit** API keys, passwords, or credentials
- Use **environment variables** or config files (gitignored)
- **Sanitize logs** to avoid exposing sensitive data
- **Review PRs** for accidental data exposure

### Web Scraping Ethics

- **Respect robots.txt** when possible
- **Implement rate limiting**
- **Handle errors gracefully**
- **Don't overwhelm servers**
- **Follow website terms of service**

## 📞 Getting Help

- **GitHub Discussions**: For questions and ideas
- **GitHub Issues**: For bugs and feature requests
- **Code Review**: Ask for feedback on complex changes

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **New website scrapers** (Georgian real estate sites)
2. **Improved error handling** and resilience
3. **Performance optimizations**
4. **Documentation improvements**
5. **Test coverage expansion**
6. **Docker and deployment improvements**

## 📜 Code of Conduct

- Be **respectful** and **inclusive**
- **Help others** learn and contribute
- **Focus on constructive feedback**
- **Respect different perspectives**

Thank you for contributing to Homeus! 🏠
