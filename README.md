# 📄 Document Extraction Learning Group

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive repository for learning and experimenting with document extraction and OCR techniques using the Sparrow Invoice Dataset and AWS Bedrock Claude Vision API.

![Invoice Extraction Demo](https://img.shields.io/badge/Dataset-501_Invoices-blue) ![Accuracy](https://img.shields.io/badge/Extraction_Accuracy-70--80%25-green)

---

## 🌟 Features

- **📊 Complete Dataset**: 501 annotated invoice images with structured labels (train/test/validation splits)
- **🤖 AWS Bedrock Integration**: Extract invoice data using Claude Sonnet 3.5 and 4.5 Vision models
- **📈 Evaluation Framework**: Comprehensive accuracy metrics and field-level analysis
- **🔍 Interactive Viewer**: Web-based tool to visualize extraction results
- **🛠️ Dataset Utilities**: Helper scripts for data exploration and processing
- **📚 Extensive Documentation**: Detailed guides and examples for all components

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Repository Structure](#-repository-structure)
- [Dataset Details](#-dataset-details)
- [Usage Examples](#-usage-examples)
- [AWS Bedrock Extraction](#-aws-bedrock-extraction)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

> 📄 For a comprehensive overview, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access (for extraction features)
- pip or conda for package management

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/document-extraction-learning-group.git
   cd document-extraction-learning-group
   ```

2. **Install dataset utilities**
   ```bash
   pip install -r src/dataset/requirements.txt
   ```

3. **Install Bedrock extraction tools** (optional)
   ```bash
   pip install -r src/bedrock/requirements.txt
   ```

### Basic Usage

**Load and explore the dataset:**

```python
import json
from PIL import Image

# Load an invoice image
image = Image.open('data/test/invoice/invoice_0000.png')

# Load corresponding annotations
with open('data/test/label/invoice_0000.json', 'r') as f:
    annotations = json.load(f)

# Access structured data
header = annotations['gt_parse']['header']
print(f"Invoice #: {header['invoice_no']}")
print(f"Date: {header['invoice_date']}")
print(f"Total: {annotations['gt_parse']['summary']['total_gross_worth']}")
```

**Run AWS Bedrock extraction:**

```bash
cd src/bedrock
python run_extraction.py
```

See [Quick Start Guide](docs/QUICKSTART.md) for detailed instructions.

---

## 📁 Repository Structure

```
document-extraction-learning-group/
├── data/                          # Invoice dataset (501 images + labels)
│   ├── train/                    # 425 training samples
│   ├── test/                     # 26 test samples
│   └── validation/               # 50 validation samples
│
├── src/                          # Source code
│   ├── bedrock/                  # AWS Bedrock extraction system
│   │   ├── bedrock_vision_client.py
│   │   ├── extract_invoices.py
│   │   ├── evaluate_extraction.py
│   │   ├── run_extraction.py
│   │   └── config.json
│   │
│   └── dataset/                  # Dataset utilities
│       ├── invoice_dataset.py    # Helper class for data access
│       ├── explore_data.py       # Dataset exploration
│       ├── extract_all_data.py   # Extract from parquet files
│       └── sample-data/          # Sample invoice and annotations
│
├── docs/                         # Documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── CONFIG_GUIDE.md          # Configuration guide
│   ├── EVALUATION_IMPROVEMENTS.md
│   └── IMPLEMENTATION_SUMMARY.md
│
├── examples/                     # Examples and demos
│   ├── index.html               # Interactive extraction viewer
│   ├── viewer.js                # Viewer JavaScript
│   └── styles.css               # Viewer styles
│
├── tests/                        # Test files (to be added)
│
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
└── README.md                    # This file
```

---

## 📊 Dataset Details

### Statistics

| Split      | Invoices | Line Items | Avg Items/Invoice |
|------------|----------|------------|-------------------|
| Train      | 425      | 1,626      | 3.83              |
| Test       | 26       | 106        | 4.08              |
| Validation | 50       | 196        | 3.92              |
| **Total**  | **501**  | **1,928**  | **3.85**          |

### Data Format

Each invoice consists of:
- **Image**: High-resolution PNG (typically 2481×3508 pixels, RGB)
- **Annotation**: JSON file containing:
  - **Header**: Invoice metadata (number, date, seller, client, tax IDs, IBAN)
  - **Items**: Line items (description, quantity, prices, VAT, totals)
  - **Summary**: Invoice totals (net worth, VAT, gross worth)

### Annotation Structure

```json
{
  "gt_parse": {
    "header": {
      "invoice_no": "97159829",
      "invoice_date": "09/18/2015",
      "seller": "Bradley-Andrade 9879 Elizabeth Common...",
      "client": "Castro PLC Unit 9678 Box 9664...",
      "seller_tax_id": "985-73-8194",
      "client_tax_id": "994-72-1270",
      "iban": "GB81LZWO32519172531418"
    },
    "items": [
      {
        "item_desc": "12\" Marble Lapis Inlay Chess Table...",
        "item_qty": "2,00",
        "item_net_price": "444,60",
        "item_net_worth": "889,20",
        "item_vat": "10%",
        "item_gross_worth": "978,12"
      }
    ],
    "summary": {
      "total_net_worth": "$ 889,20",
      "total_vat": "$ 88,92",
      "total_gross_worth": "$ 978,12"
    }
  }
}
```

---

## 💡 Usage Examples

### 1. Dataset Exploration

```python
from src.dataset.invoice_dataset import InvoiceDataset

# Load dataset (if you have parquet files)
dataset = InvoiceDataset('path/to/parquet/file.parquet')

# Get a sample
sample = dataset.get_sample(0)
print(f"Invoice #: {sample['header']['invoice_no']}")
print(f"Items: {len(sample['items'])}")

# View sample details
dataset.print_sample_details(0)
```

### 2. Batch Processing

```python
from pathlib import Path
import json
from PIL import Image

# Process all test invoices
test_dir = Path('data/test')
for img_path in test_dir.glob('invoice/*.png'):
    # Load image
    image = Image.open(img_path)
    
    # Load label
    label_path = test_dir / 'label' / f"{img_path.stem}.json"
    with open(label_path) as f:
        label = json.load(f)
    
    # Your processing logic here
    print(f"Processing {img_path.name}...")
```

### 3. AWS Bedrock Extraction

```python
from src.bedrock.bedrock_vision_client import BedrockVisionClient

# Initialize client
client = BedrockVisionClient(
    model_id='au.anthropic.claude-sonnet-4-5-20250929-v1:0',
    region_name='ap-southeast-2'
)

# Extract invoice data
result = client.extract_invoice_data('data/test/invoice/invoice_0000.png')

print(f"Invoice #: {result['invoice_no']}")
print(f"Date: {result['invoice_date']}")
print(f"Total: {result['total_gross_worth']}")
```

See [src/dataset/use_extracted_data_example.py](src/dataset/use_extracted_data_example.py) for more examples.

---

## 🤖 AWS Bedrock Extraction

This repository includes a complete system for extracting invoice data using AWS Bedrock Claude Vision API.

### Features

- **Multi-model support**: Claude Sonnet 3.5 and 4.5
- **Automatic retry logic**: Handles API failures gracefully
- **Resume capability**: Skip already-processed invoices
- **Comprehensive evaluation**: Field-level accuracy metrics
- **Interactive viewer**: Visualize extraction results

### Quick Start

1. **Configure AWS credentials**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Key, and region (ap-southeast-2)
   ```

2. **Run extraction**
   ```bash
   cd src/bedrock
   python run_extraction.py
   ```

3. **View results**
   - Extraction results: `src/bedrock/output/`
   - Evaluation metrics: `src/bedrock/logs/`
   - Interactive viewer: Open `examples/index.html` in a browser

### Performance

- **Processing time**: ~15-30 minutes for 501 invoices
- **Cost**: ~$0.50-1.00 USD (AWS Bedrock charges)
- **Accuracy**: 70-80% overall (all 5 fields correct)

See [Bedrock README](src/bedrock/README.md) for detailed documentation.

---

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)**: Get started in 3 steps
- **[Configuration Guide](docs/CONFIG_GUIDE.md)**: Model and system configuration
- **[Bedrock System](src/bedrock/README.md)**: AWS Bedrock extraction documentation
- **[Dataset Utilities](src/dataset/README.md)**: Dataset processing and exploration
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to this project

---

## 🎯 Use Cases

This dataset and toolkit are suitable for:

- **Document Understanding**: Training models to extract structured data from invoices
- **OCR Training**: Fine-tuning OCR models for invoice recognition
- **Layout Analysis**: Learning document structure and layout patterns
- **Information Extraction**: Extracting key-value pairs from documents
- **Model Benchmarking**: Evaluating document extraction model performance
- **Research**: Experimenting with new extraction techniques

---

## 🛠️ Suggested Models & Approaches

This dataset is compatible with:

- **AWS Bedrock Claude Vision** - Cloud-based vision API (included)
- **Donut** - Document Understanding Transformer
- **LayoutLM** family - Document layout understanding models
- **TrOCR** - Transformer-based OCR
- **Custom CNN+RNN** - Traditional OCR approaches
- **Vision Transformers** - Vision-based document analysis

---

## 🔮 Future Improvements

- [ ] Add support for more LLM providers (OpenAI GPT-4V, Google Gemini)
- [ ] Implement fine-tuning scripts for open-source models
- [ ] Add Jupyter notebook tutorials
- [ ] Create Docker container for easy deployment
- [ ] Add unit tests and integration tests
- [ ] Implement data augmentation utilities
- [ ] Add support for other document types (receipts, forms)
- [ ] Create web API for extraction service

See [issues](../../issues) for planned features and known bugs.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star this repository if you find it useful!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Dataset Attribution

- **Dataset Name**: Sparrow Invoice Dataset
- **Prepared by**: [Katana ML](https://www.katanaml.io)
- **Project**: [Sparrow](https://github.com/katanaml/sparrow) - Open-source data extraction solution
- **Original Data**: [Mendeley Data - Electronic Invoices](https://data.mendeley.com/datasets/tnj49gpmtz)
- **Citation**: Kozłowski, Marek; Weichbroth, Paweł (2021), "Samples of electronic invoices", Mendeley Data, V2, doi: 10.17632/tnj49gpmtz.2

---

## 🙏 Acknowledgments

- **Katana ML** for preparing and sharing the Sparrow Invoice Dataset
- **AWS Bedrock** for providing Claude Vision API access
- **Anthropic** for developing Claude models
- The open-source community for tools and libraries

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Documentation**: [docs/](docs/)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Ready to start?** Check out the [Quick Start Guide](docs/QUICKSTART.md) or dive into the [examples](examples/)!
