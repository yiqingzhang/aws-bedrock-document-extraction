# Repository Structure

This document provides a complete overview of the repository structure.

## 📁 Directory Tree

```
document-extraction-learning-group/
│
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions CI/CD workflow
│
├── data/                                   # Invoice Dataset (501 samples)
│   ├── test/                              # 26 test samples
│   │   ├── invoice/                       # Invoice images (PNG)
│   │   └── label/                         # Annotations (JSON)
│   ├── train/                             # 425 training samples
│   │   ├── invoice/
│   │   └── label/
│   └── validation/                        # 50 validation samples
│       ├── invoice/
│       └── label/
│
├── docs/                                   # Documentation
│   ├── README.md                          # Documentation index
│   ├── QUICKSTART.md                      # Quick start guide
│   ├── CONFIG_GUIDE.md                    # Configuration guide
│   ├── IMPLEMENTATION_SUMMARY.md          # Technical details
│   └── EVALUATION_IMPROVEMENTS.md         # Evaluation metrics
│
├── examples/                               # Examples and Demos
│   ├── README.md                          # Examples overview
│   ├── basic_usage.py                     # Basic usage demo
│   ├── ANALYSIS_VIEWER.md                 # Viewer documentation
│   ├── index.html                         # Interactive viewer
│   ├── viewer.js                          # Viewer JavaScript
│   └── styles.css                         # Viewer styles
│
├── src/                                    # Source Code
│   ├── __init__.py                        # Root package
│   │
│   ├── bedrock/                           # AWS Bedrock Extraction
│   │   ├── __init__.py                    # Module exports
│   │   ├── README.md                      # Bedrock documentation
│   │   ├── requirements.txt               # Bedrock dependencies
│   │   ├── config.json                    # Model configuration
│   │   ├── bedrock_vision_client.py       # AWS Bedrock client
│   │   ├── extract_invoices.py            # Extraction pipeline
│   │   ├── evaluate_extraction.py         # Evaluation framework
│   │   ├── run_extraction.py              # Main entry point
│   │   └── compare_models.py              # Model comparison
│   │
│   └── dataset/                           # Dataset Utilities
│       ├── __init__.py                    # Module exports
│       ├── README.md                      # Dataset documentation
│       ├── requirements.txt               # Dataset dependencies
│       ├── invoice_dataset.py             # Dataset helper class
│       ├── explore_data.py                # Data exploration
│       ├── extract_all_data.py            # Parquet extraction
│       ├── use_extracted_data_example.py  # Usage examples
│       └── sample-data/                   # Sample files
│           ├── sample_invoice.png
│           └── sample_invoice_annotations.json
│
├── tests/                                  # Unit Tests
│   ├── README.md                          # Testing guide
│   └── test_dataset.py                    # Dataset tests
│
├── .env.example                           # AWS config template
├── .gitignore                             # Git ignore patterns
├── CHANGELOG.md                           # Version history
├── CODE_OF_CONDUCT.md                     # Community guidelines
├── CONTRIBUTING.md                        # Contribution guide
├── LICENSE                                # MIT License
├── PROJECT_SUMMARY.md                     # Project overview
├── README.md                              # Main documentation
├── REFACTORING_SUMMARY.md                 # Refactoring details
├── requirements.txt                       # All dependencies
└── setup.py                               # Package installation
```

## 📊 File Count by Type

- **Python Files**: 10 modules
- **Documentation**: 15+ markdown files
- **Configuration**: 3 files (config.json, .gitignore, .env.example)
- **Web Files**: 3 files (HTML, JS, CSS)
- **Dataset**: 501 images + 501 JSON annotations

## 🎯 Key Directories

### `/data`
Contains the complete Sparrow Invoice Dataset with train/test/validation splits.

### `/src/bedrock`
AWS Bedrock integration for invoice extraction using Claude Vision API.

### `/src/dataset`
Utilities for working with the dataset, including exploration and processing tools.

### `/docs`
Comprehensive documentation including guides, tutorials, and technical details.

### `/examples`
Usage examples and interactive demos for visualizing results.

### `/tests`
Unit tests and testing framework (work in progress).

## 🔧 Configuration Files

- `.github/workflows/ci.yml` - CI/CD automation
- `.gitignore` - Git ignore patterns
- `.env.example` - AWS configuration template
- `requirements.txt` - Python dependencies
- `setup.py` - Package installation
- `src/bedrock/config.json` - Model configuration

## 📚 Documentation Files

- `README.md` - Main project documentation
- `PROJECT_SUMMARY.md` - Comprehensive overview
- `CONTRIBUTING.md` - How to contribute
- `CODE_OF_CONDUCT.md` - Community standards
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License
- `REFACTORING_SUMMARY.md` - Refactoring details

## 🚀 Entry Points

- `examples/basic_usage.py` - Basic usage demo
- `src/bedrock/run_extraction.py` - AWS Bedrock extraction
- `src/dataset/explore_data.py` - Dataset exploration
- `examples/index.html` - Interactive viewer

---

**Last Updated**: November 2, 2025  
**Version**: 1.0.0
