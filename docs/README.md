# Documentation

Welcome to the Document Extraction Learning Group documentation!

## 📚 Documentation Index

### Getting Started

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 3 simple steps
- **[Configuration Guide](CONFIG_GUIDE.md)** - Configure models and system settings
- **[Main README](../README.md)** - Project overview and features

### Core Components

- **[Bedrock Extraction System](../src/bedrock/README.md)** - AWS Bedrock Claude Vision API integration
- **[Dataset Utilities](../src/dataset/README.md)** - Tools for working with the invoice dataset
- **[Examples](../examples/README.md)** - Code examples and demos

### Development

- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to this project
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[Evaluation Improvements](EVALUATION_IMPROVEMENTS.md)** - Evaluation metrics and improvements

## 🎯 Quick Links

### For Users

- **First time here?** Start with the [Quick Start Guide](QUICKSTART.md)
- **Want to use the dataset?** See [Dataset Utilities](../src/dataset/README.md)
- **Need to extract invoices?** Check [Bedrock System](../src/bedrock/README.md)
- **Looking for examples?** Browse [Examples](../examples/)

### For Developers

- **Want to contribute?** Read [Contributing Guide](../CONTRIBUTING.md)
- **Understanding the code?** See [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- **Improving accuracy?** Check [Evaluation Improvements](EVALUATION_IMPROVEMENTS.md)

## 📖 Documentation Structure

```
docs/
├── README.md                      # This file - documentation index
├── QUICKSTART.md                  # Quick start guide (3 steps)
├── CONFIG_GUIDE.md                # Configuration guide
├── IMPLEMENTATION_SUMMARY.md      # Technical implementation details
└── EVALUATION_IMPROVEMENTS.md     # Evaluation metrics documentation
```

## 🔍 Common Tasks

### Loading the Dataset

```python
import json
from PIL import Image

# Load an invoice
image = Image.open('data/test/invoice/invoice_0000.png')
with open('data/test/label/invoice_0000.json', 'r') as f:
    annotations = json.load(f)
```

See [Dataset Utilities](../src/dataset/README.md) for more details.

### Running Extraction

```bash
cd src/bedrock
python run_extraction.py --model claude_4_5
```

See [Bedrock System](../src/bedrock/README.md) for more details.

### Contributing

```bash
# Fork the repository
git clone https://github.com/yourusername/document-extraction-learning-group.git
cd document-extraction-learning-group

# Create a branch
git checkout -b feature/your-feature

# Make changes and commit
git commit -m "Add: your feature description"

# Push and create PR
git push origin feature/your-feature
```

See [Contributing Guide](../CONTRIBUTING.md) for more details.

## 💡 Tips

- **Start simple**: Begin with the basic examples before diving into advanced features
- **Read the code**: The codebase is well-documented with inline comments
- **Ask questions**: Open an issue or discussion if you need help
- **Share your work**: Contribute back improvements and examples

## 📞 Getting Help

- **Issues**: [GitHub Issues](../../issues) - Report bugs or request features
- **Discussions**: [GitHub Discussions](../../discussions) - Ask questions or share ideas
- **Documentation**: You're reading it! Browse the links above

## 🔄 Keeping Up to Date

This documentation is continuously improved. Check back for:
- New examples and tutorials
- Updated configuration guides
- Performance optimization tips
- Best practices and patterns

---

**Ready to start?** Pick a link above and dive in! 🚀

