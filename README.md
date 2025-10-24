# Document Extraction Learning Group

A comprehensive repository for learning and experimenting with document extraction and OCR techniques using the Sparrow Invoice Dataset.

## 📋 Overview

This repository contains 501 annotated invoice documents with structured data extraction labels, ready for training and evaluating OCR and document understanding models. The dataset has been pre-processed and organized for easy use in machine learning workflows.

## 🗂️ Repository Structure

```
document-extraction-learning-group/
├── data/                           # Extracted invoice images and annotations
│   ├── test/
│   │   ├── invoice/               # 26 test invoice images (PNG)
│   │   └── label/                 # 26 test annotations (JSON)
│   ├── train/
│   │   ├── invoice/               # 425 training invoice images (PNG)
│   │   └── label/                 # 425 training annotations (JSON)
│   └── validation/
│       ├── invoice/               # 50 validation invoice images (PNG)
│       └── label/                 # 50 validation annotations (JSON)
│
└── data_extraction_scripts/       # Scripts for data processing and exploration
    ├── extract_all_data.py       # Extract data from parquet files
    ├── invoice_dataset.py        # Helper class for parquet data access
    ├── explore_data.py           # Dataset exploration utilities
    ├── use_extracted_data_example.py  # Usage examples
    ├── requirements.txt          # Python dependencies
    ├── sample-data/              # Sample invoice and annotation
    └── README.md                 # Detailed documentation for scripts
```

## 📦 Dataset Details

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
- **Annotation**: JSON file containing structured data:
  - **Header**: Invoice metadata (number, date, seller, client, tax IDs, IBAN)
  - **Items**: Line items (description, quantity, prices, VAT, totals)
  - **Summary**: Invoice totals (net worth, VAT, gross worth)

### Example Files

- Sample invoice image: `data_extraction_scripts/sample-data/sample_invoice.png`
- Sample annotation: `data_extraction_scripts/sample-data/sample_invoice_annotations.json`

## 🚀 Getting Started

### Prerequisites

```bash
# Navigate to the data_extraction_scripts folder
cd data_extraction_scripts

# Install required dependencies
pip install -r requirements.txt
```

Required packages:
- `pandas` - Data manipulation
- `pillow` - Image processing
- `pyarrow` - Parquet file support

### Quick Start: Using the Extracted Data

The dataset is already extracted and ready to use! Here's a simple example:

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
invoice_number = header['invoice_no']
invoice_date = header['invoice_date']

items = annotations['gt_parse']['items']
for item in items:
    print(f"Item: {item['item_desc']}")
    print(f"Quantity: {item['item_qty']}")
    print(f"Price: {item['item_net_price']}")

summary = annotations['gt_parse']['summary']
total = summary['total_gross_worth']
```

### Advanced Usage

For more detailed examples and utilities, see:
- `data_extraction_scripts/use_extracted_data_example.py` - Comprehensive usage examples
- `data_extraction_scripts/README.md` - Detailed documentation

## 💾 Raw Dataset Source

> **Note**: The raw Hugging Face dataset (parquet files) is **not included** in this repository due to file size constraints (~197 MB compressed).

### How to Obtain the Raw Dataset

If you need the original parquet files:

1. **Download from Hugging Face**:
   ```bash
   # Using Hugging Face datasets library
   from datasets import load_dataset
   dataset = load_dataset("katanaml-org/invoices-donut-data-v1")
   ```

2. **Or use the extraction scripts** (if you have the parquet files):
   ```bash
   cd data_extraction_scripts
   python extract_all_data.py
   ```
   See `data_extraction_scripts/README.md` for details.

The extraction scripts are included for transparency and reproducibility, allowing you to re-extract the data if needed.

## 📊 Annotation Structure

Each JSON annotation file follows this structure:

```json
{
  "gt_parse": {
    "header": {
      "invoice_no": "97159829",
      "invoice_date": "09/18/2015",
      "seller": "Bradley-Andrade 9879 Elizabeth Common Lake Jonathan, RI 12335",
      "client": "Castro PLC Unit 9678 Box 9664 DPO AP 69387",
      "seller_tax_id": "985-73-8194",
      "client_tax_id": "994-72-1270",
      "iban": "GB81LZWO32519172531418"
    },
    "items": [
      {
        "item_desc": "12\" Marble Lapis Inlay Chess Table Top...",
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

## 🎯 Use Cases

This dataset is suitable for:

- **Document Understanding**: Training models to extract structured data from invoices
- **OCR Training**: Fine-tuning OCR models for invoice recognition
- **Layout Analysis**: Learning document structure and layout patterns
- **Information Extraction**: Extracting key-value pairs from documents
- **Data Validation**: Building validation systems for invoice data
- **Model Benchmarking**: Evaluating document extraction model performance

## 🛠️ Suggested Models & Approaches

This dataset is compatible with:

- **Donut** (Document Understanding Transformer) - End-to-end document understanding
- **LayoutLM** family - Document layout understanding models
- **TrOCR** - Transformer-based OCR
- **Custom CNN+RNN** - Traditional OCR approaches
- **Vision Transformers** - Vision-based document analysis

## 📖 Dataset Source & License

- **Dataset Name**: Sparrow Invoice Dataset
- **Prepared by**: [Katana ML](https://www.katanaml.io)
- **Project**: [Sparrow](https://github.com/katanaml/sparrow) - Open-source data extraction solution
- **Original Data**: [Mendeley Data - Electronic Invoices](https://data.mendeley.com/datasets/tnj49gpmtz)
- **Citation**: Kozłowski, Marek; Weichbroth, Paweł (2021), "Samples of electronic invoices", Mendeley Data, V2, doi: 10.17632/tnj49gpmtz.2
- **License**: MIT
- **Language**: English

## 📚 Additional Resources

- **Hugging Face Dataset**: [katanaml-org/invoices-donut-data-v1](https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1)
- **Sparrow Project**: [github.com/katanaml/sparrow](https://github.com/katanaml/sparrow)
- **Data Extraction Scripts**: See `data_extraction_scripts/README.md` for detailed documentation

## 🤝 Contributing

This is a learning repository. Feel free to:
- Add new extraction scripts or utilities
- Improve documentation
- Share training notebooks or experiments
- Report issues with the data

## 📝 Notes

- All invoice images are stored as PNG format for quality preservation
- JSON files use UTF-8 encoding to support special characters
- File naming convention: `invoice_XXXX.{png|json}` (zero-padded 4-digit index)
- Images maintain original resolution for maximum quality

---

**Ready to start?** Check out `data_extraction_scripts/use_extracted_data_example.py` for practical examples, or dive directly into the `data/` folder to explore the invoice images and annotations!

