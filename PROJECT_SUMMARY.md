# Project Summary

## 📄 Document Extraction Learning Group

A professional, open-source repository for learning and experimenting with document extraction and OCR techniques.

---

## 🎯 Project Overview

This repository provides:
- **501 annotated invoice images** from the Sparrow Invoice Dataset
- **AWS Bedrock integration** for Claude Vision API extraction
- **Comprehensive evaluation framework** with accuracy metrics
- **Interactive visualization tools** for results analysis
- **Extensive documentation** and examples

---

## 📊 Repository Statistics

- **Total Invoices**: 501 (425 train, 26 test, 50 validation)
- **Total Line Items**: 1,928 across all invoices
- **Code Files**: 10 Python modules
- **Documentation**: 10+ markdown files
- **Examples**: 3 demo files including interactive viewer
- **License**: MIT

---

## 🏗️ Architecture

### Core Components

1. **Dataset Module** (`src/dataset/`)
   - Invoice dataset utilities
   - Data exploration tools
   - Parquet file extraction
   - Sample data and examples

2. **Bedrock Module** (`src/bedrock/`)
   - AWS Bedrock Vision client
   - Invoice extraction pipeline
   - Evaluation framework
   - Multi-model support (Claude 3.5 & 4.5)

3. **Documentation** (`docs/`)
   - Quick start guide
   - Configuration guide
   - Implementation details
   - Evaluation improvements

4. **Examples** (`examples/`)
   - Basic usage scripts
   - Interactive web viewer
   - Analysis tools

---

## 🔧 Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **AWS Bedrock**: Cloud-based LLM inference
- **Claude Vision**: Document understanding models
- **PIL/Pillow**: Image processing
- **Pandas**: Data manipulation

### Development Tools
- **GitHub Actions**: CI/CD automation
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting

---

## 📈 Key Features

### 1. Complete Dataset
- Pre-processed and organized invoice images
- Structured JSON annotations
- Train/test/validation splits
- High-quality PNG images (2481×3508 pixels)

### 2. AWS Bedrock Integration
- Claude Sonnet 3.5 and 4.5 support
- Automatic retry with exponential backoff
- Checkpoint/resume capability
- Comprehensive error handling

### 3. Evaluation Framework
- Field-level accuracy metrics
- Overall accuracy calculation
- Detailed performance reports
- Failed extraction logging

### 4. Interactive Tools
- Web-based results viewer
- Side-by-side comparison
- Ground truth validation
- Navigation and filtering

### 5. Professional Documentation
- Clear getting started guide
- Comprehensive API documentation
- Code examples and tutorials
- Contributing guidelines

---

## 📁 File Structure

```
document-extraction-learning-group/
├── .github/workflows/          # CI/CD configuration
├── data/                       # Invoice dataset (501 samples)
├── docs/                       # Documentation
├── examples/                   # Usage examples and demos
├── src/                        # Source code
│   ├── bedrock/               # AWS Bedrock extraction
│   └── dataset/               # Dataset utilities
├── tests/                      # Unit tests
├── CHANGELOG.md               # Version history
├── CODE_OF_CONDUCT.md         # Community guidelines
├── CONTRIBUTING.md            # Contribution guide
├── LICENSE                    # MIT License
├── README.md                  # Main documentation
├── requirements.txt           # Python dependencies
└── setup.py                   # Package installation
```

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/document-extraction-learning-group.git
cd document-extraction-learning-group

# Install dependencies
pip install -r requirements.txt

# Load dataset
python examples/basic_usage.py

# Run extraction (requires AWS credentials)
cd src/bedrock
python run_extraction.py --model claude_4_5
```

---

## 📊 Performance Metrics

### Extraction Performance
- **Processing Time**: ~15-30 minutes for 501 invoices
- **Cost**: ~$0.50-1.00 USD (AWS Bedrock)
- **Accuracy**: 70-80% overall (all fields correct)

### Field-Level Accuracy (Claude 4.5)
- Invoice Number: 90-95%
- Invoice Date: 85-92%
- Total Amount: 85-90%
- Seller/Client: 80-85%

---

## 🎓 Use Cases

1. **Learning**: Understand document extraction techniques
2. **Research**: Experiment with different models and approaches
3. **Benchmarking**: Evaluate model performance
4. **Training**: Fine-tune custom models
5. **Production**: Build invoice processing systems

---

## 🔮 Roadmap

### Version 1.1 (Planned)
- [ ] OpenAI GPT-4V integration
- [ ] Google Gemini Vision support
- [ ] Jupyter notebook tutorials
- [ ] Docker containerization
- [ ] Unit test coverage

### Version 1.2 (Planned)
- [ ] Fine-tuning scripts
- [ ] Data augmentation tools
- [ ] Additional document types
- [ ] REST API service
- [ ] Performance optimizations

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Development setup
- Testing requirements

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

### Dataset Attribution
- **Dataset**: Sparrow Invoice Dataset by Katana ML
- **Original Data**: Mendeley Data - Electronic Invoices
- **Citation**: Kozłowski & Weichbroth (2021), doi: 10.17632/tnj49gpmtz.2

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/document-extraction-learning-group/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/document-extraction-learning-group/discussions)
- **Documentation**: [docs/](docs/)

---

## 🙏 Acknowledgments

- Katana ML for the Sparrow Invoice Dataset
- AWS for Bedrock platform
- Anthropic for Claude models
- Open-source community

---

## ⭐ Star History

If you find this project useful, please give it a star! ⭐

---

**Last Updated**: November 2, 2025  
**Version**: 1.0.0  
**Status**: Active Development

