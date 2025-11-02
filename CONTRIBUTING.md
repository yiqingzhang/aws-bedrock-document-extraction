# Contributing to Document Extraction Learning Group

Thank you for your interest in contributing! This project welcomes contributions from the community.

## 🤝 How to Contribute

### Reporting Issues

- Check if the issue already exists in the [issue tracker](../../issues)
- Use a clear and descriptive title
- Provide detailed steps to reproduce the problem
- Include relevant logs, screenshots, or error messages
- Mention your environment (OS, Python version, AWS region)

### Suggesting Enhancements

- Use a clear and descriptive title
- Provide a detailed description of the proposed enhancement
- Explain why this enhancement would be useful
- Include examples of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for non-obvious logic
   - Update documentation if needed

3. **Test your changes**
   - Ensure existing functionality still works
   - Add tests for new features if applicable

4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Wait for review and address feedback

## 📝 Code Style Guidelines

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

Example:
```python
def extract_invoice_field(image_path: str, field_name: str) -> dict:
    """
    Extract a specific field from an invoice image.
    
    Args:
        image_path: Path to the invoice image file
        field_name: Name of the field to extract
        
    Returns:
        Dictionary containing the extracted field data
    """
    # Implementation here
    pass
```

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep README and docs up to date
- Use proper markdown formatting

## 🧪 Testing

Before submitting a PR:

1. Test your changes locally
2. Verify that existing scripts still work
3. Check for any broken links in documentation
4. Ensure code follows style guidelines

## 📋 Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/document-extraction-learning-group.git
   cd document-extraction-learning-group
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r src/bedrock/requirements.txt
   pip install -r src/dataset/requirements.txt
   ```

4. Make your changes and test

## 🎯 Areas for Contribution

We welcome contributions in these areas:

- **New extraction models**: Add support for other LLMs or OCR engines
- **Evaluation metrics**: Improve or add new evaluation methods
- **Documentation**: Improve guides, add tutorials, fix typos
- **Examples**: Add Jupyter notebooks or example scripts
- **Dataset utilities**: Tools for data exploration and visualization
- **Performance**: Optimize extraction speed or accuracy
- **Testing**: Add unit tests or integration tests
- **Bug fixes**: Fix reported issues

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## ❓ Questions?

If you have questions about contributing:

- Check the [documentation](docs/)
- Open a [discussion](../../discussions)
- Ask in an issue

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making document extraction more accessible! 🎉

