# Dataset Utilities

This directory contains utilities for working with the Sparrow Invoice Dataset - 501 annotated invoice documents ready for OCR and document understanding tasks.

## 📦 Dataset Structure

The data is stored in **Parquet format** with the following structure:

- **Images**: High-resolution invoice images (RGB JPEG, typically 2481x3508 pixels)
- **Ground Truth**: JSON annotations containing:
  - **Header**: Invoice number, date, seller/client info, tax IDs, IBAN
  - **Items**: Line items with descriptions, quantities, prices, VAT, totals
  - **Summary**: Total net worth, VAT, and gross totals

### Dataset Splits

- **Train**: 425 samples
- **Test**: 26 samples  
- **Validation**: 50 samples

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Extract All Data from Parquet Files

If you have the original parquet files from Hugging Face, run this script to extract all images and JSON annotations:

```bash
cd src/dataset
python extract_all_data.py
```

This will create the following structure in the `data/` directory:
```
data/
├── test/
│   ├── invoice/     (26 PNG images)
│   └── label/       (26 JSON files)
├── train/
│   ├── invoice/     (425 PNG images)
│   └── label/       (425 JSON files)
└── validation/
    ├── invoice/     (50 PNG images)
    └── label/       (50 JSON files)
```

**Note**: The extracted data is already included in this repository, so you only need to run this if you want to re-extract from parquet files.

### Using Extracted Data

The dataset is already extracted and ready to use! Here's how to work with it:

```python
# See use_extracted_data_example.py for full examples

from pathlib import Path
import json
from PIL import Image

# Load a single invoice (from repository root)
image = Image.open('data/test/invoice/invoice_0000.png')
with open('data/test/label/invoice_0000.json', 'r') as f:
    annotations = json.load(f)

# Access invoice data
header = annotations['gt_parse']['header']
items = annotations['gt_parse']['items']
summary = annotations['gt_parse']['summary']
```

### Working with Parquet Files Directly

```python
from invoice_dataset import InvoiceDataset

# Load the test dataset
dataset = InvoiceDataset('invoices-donut-data-v1/data/test-00000-of-00001-56af6bd5ff7eb34d.parquet')

# Get a sample
sample = dataset.get_sample(0)
image = sample['image']      # PIL Image
header = sample['header']    # Invoice header info
items = sample['items']      # Line items
summary = sample['summary']  # Totals

# View details
dataset.print_sample_details(0)

# Save an image
dataset.save_image(0, 'invoice.png')
```

## 📁 Files

- `invoice_dataset.py` - Helper class for easy data access (works with parquet files)
- `explore_data.py` - Script to explore the dataset structure
- `extract_all_data.py` - Script to extract all images and annotations from parquet files
- `use_extracted_data_example.py` - Example showing how to use the extracted data
- `requirements.txt` - Python dependencies
- `sample_invoice.png` - Example invoice image
- `sample_invoice_annotations.json` - Example invoice annotations

## 📊 Example Data Structure

```json
{
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
```

## 📖 Dataset Info

- **Source**: Sparrow Invoice Dataset by [Katana ML](https://www.katanaml.io)
- **Original Dataset**: [Mendeley Data](https://data.mendeley.com/datasets/tnj49gpmtz)
- **License**: MIT
- **Task**: Feature extraction / Document understanding
- **Language**: English

## 📚 Additional Resources

- **Main README**: See [../../README.md](../../README.md) for project overview
- **Bedrock Extraction**: See [../bedrock/README.md](../bedrock/README.md) for AWS Bedrock extraction
- **Contributing**: See [../../CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines

