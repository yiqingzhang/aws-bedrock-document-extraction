"""
Example script showing how to use the extracted invoice data.

After running extract_all_data.py, this script demonstrates how to:
1. Load and display invoice images
2. Read and parse JSON annotations
3. Iterate through the dataset
"""

import json
from pathlib import Path
from PIL import Image
from typing import Dict, List


def load_invoice_pair(invoice_path: str, label_path: str) -> Dict:
    """
    Load an invoice image and its corresponding annotations.
    
    Args:
        invoice_path: Path to the invoice PNG image
        label_path: Path to the label JSON file
        
    Returns:
        Dictionary with 'image' and 'annotations'
    """
    # Load image
    image = Image.open(invoice_path)
    
    # Load annotations
    with open(label_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)
    
    return {
        'image': image,
        'annotations': annotations
    }


def iterate_dataset_split(split_name: str = 'test') -> List[Dict]:
    """
    Iterate through all invoices in a dataset split.
    
    Args:
        split_name: One of 'test', 'train', or 'validation'
        
    Returns:
        List of dictionaries containing invoice data
    """
    base_dir = Path('/Users/Michael.Zhang/Documents/myob/repos/ocr/data')
    invoice_dir = base_dir / split_name / 'invoice'
    label_dir = base_dir / split_name / 'label'
    
    # Get all invoice files
    invoice_files = sorted(invoice_dir.glob('invoice_*.png'))
    
    dataset = []
    for invoice_file in invoice_files:
        # Reason: Construct matching label filename
        label_file = label_dir / invoice_file.name.replace('.png', '.json')
        
        if label_file.exists():
            data = load_invoice_pair(str(invoice_file), str(label_file))
            data['filename'] = invoice_file.name
            dataset.append(data)
    
    return dataset


def print_invoice_summary(invoice_data: Dict, index: int):
    """
    Print a summary of an invoice.
    
    Args:
        invoice_data: Invoice data dictionary
        index: Invoice index for display
    """
    annotations = invoice_data['annotations']['gt_parse']
    header = annotations.get('header', {})
    items = annotations.get('items', [])
    summary = annotations.get('summary', {})
    
    print(f"\n{'='*60}")
    print(f"Invoice #{index}: {invoice_data['filename']}")
    print(f"{'='*60}")
    print(f"Invoice No: {header.get('invoice_no', 'N/A')}")
    print(f"Date: {header.get('invoice_date', 'N/A')}")
    print(f"Seller: {header.get('seller', 'N/A')[:50]}...")
    print(f"Client: {header.get('client', 'N/A')[:50]}...")
    print(f"Items: {len(items)}")
    print(f"Total: {summary.get('total_gross_worth', 'N/A')}")
    print(f"Image Size: {invoice_data['image'].size}")


def main():
    """Demonstrate usage of extracted data."""
    
    print("🎯 Invoice Data Usage Examples")
    print("="*60)
    
    # Example 1: Load a single invoice
    print("\n📄 Example 1: Loading a single invoice")
    invoice_data = load_invoice_pair(
        '/Users/Michael.Zhang/Documents/myob/repos/ocr/data/test/invoice/invoice_0000.png',
        '/Users/Michael.Zhang/Documents/myob/repos/ocr/data/test/label/invoice_0000.json'
    )
    print(f"  Loaded: {invoice_data['image'].size} image")
    print(f"  Invoice #: {invoice_data['annotations']['gt_parse']['header']['invoice_no']}")
    
    # Example 2: Iterate through test set
    print("\n📚 Example 2: Loading test set")
    test_data = iterate_dataset_split('test')
    print(f"  Loaded {len(test_data)} test invoices")
    
    # Show first 3 invoices
    print("\n📋 Sample Invoices from Test Set:")
    for idx, invoice_data in enumerate(test_data[:3]):
        print_invoice_summary(invoice_data, idx)
    
    # Example 3: Statistics
    print("\n" + "="*60)
    print("📊 Dataset Statistics")
    print("="*60)
    
    for split in ['test', 'train', 'validation']:
        data = iterate_dataset_split(split)
        total_items = sum(
            len(inv['annotations']['gt_parse'].get('items', []))
            for inv in data
        )
        print(f"\n{split.capitalize()}:")
        print(f"  Total invoices: {len(data)}")
        print(f"  Total line items: {total_items}")
        print(f"  Avg items per invoice: {total_items/len(data):.2f}")
    
    # Example 4: How to use in your code
    print("\n" + "="*60)
    print("💡 Usage Pattern for Your Code")
    print("="*60)
    print("""
# Load a specific split
train_data = iterate_dataset_split('train')

# Process each invoice
for invoice_data in train_data:
    image = invoice_data['image']  # PIL Image
    annotations = invoice_data['annotations']['gt_parse']
    
    # Access header information
    header = annotations['header']
    invoice_no = header['invoice_no']
    invoice_date = header['invoice_date']
    
    # Access line items
    for item in annotations['items']:
        description = item['item_desc']
        quantity = item['item_qty']
        price = item['item_net_price']
        # ... process item ...
    
    # Access summary
    summary = annotations['summary']
    total = summary['total_gross_worth']
    # ... process invoice ...
""")
    
    print("\n✅ All examples completed!")


if __name__ == "__main__":
    main()

