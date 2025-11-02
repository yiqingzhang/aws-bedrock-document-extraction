#!/usr/bin/env python3
"""
Basic Usage Example - Document Extraction Learning Group

This script demonstrates the basic usage of the invoice dataset:
- Loading invoice images
- Reading annotation files
- Accessing structured data
- Iterating through the dataset
"""

import json
from pathlib import Path
from PIL import Image


def load_single_invoice(invoice_id='invoice_0000', split='test'):
    """
    Load a single invoice and its annotations.
    
    Args:
        invoice_id: Invoice filename without extension (e.g., 'invoice_0000')
        split: Dataset split ('test', 'train', or 'validation')
    
    Returns:
        tuple: (image, annotations_dict)
    """
    # Get repository root (assuming script is in examples/)
    repo_root = Path(__file__).parent.parent
    
    # Construct paths
    image_path = repo_root / 'data' / split / 'invoice' / f'{invoice_id}.png'
    label_path = repo_root / 'data' / split / 'label' / f'{invoice_id}.json'
    
    # Load image
    image = Image.open(image_path)
    
    # Load annotations
    with open(label_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)
    
    return image, annotations


def print_invoice_details(annotations):
    """
    Print formatted invoice details from annotations.
    
    Args:
        annotations: Dictionary containing invoice annotations
    """
    gt_parse = annotations['gt_parse']
    header = gt_parse['header']
    items = gt_parse['items']
    summary = gt_parse['summary']
    
    print("\n" + "=" * 60)
    print("INVOICE DETAILS")
    print("=" * 60)
    
    # Header information
    print("\n📋 Header Information:")
    print(f"  Invoice Number: {header['invoice_no']}")
    print(f"  Invoice Date: {header['invoice_date']}")
    print(f"  Seller: {header['seller'][:50]}...")
    print(f"  Client: {header['client'][:50]}...")
    print(f"  Seller Tax ID: {header['seller_tax_id']}")
    print(f"  Client Tax ID: {header['client_tax_id']}")
    print(f"  IBAN: {header['iban']}")
    
    # Line items
    print(f"\n📦 Line Items ({len(items)} items):")
    for i, item in enumerate(items, 1):
        print(f"\n  Item {i}:")
        print(f"    Description: {item['item_desc'][:40]}...")
        print(f"    Quantity: {item['item_qty']}")
        print(f"    Net Price: {item['item_net_price']}")
        print(f"    Net Worth: {item['item_net_worth']}")
        print(f"    VAT: {item['item_vat']}")
        print(f"    Gross Worth: {item['item_gross_worth']}")
    
    # Summary
    print("\n💰 Summary:")
    print(f"  Total Net Worth: {summary['total_net_worth']}")
    print(f"  Total VAT: {summary['total_vat']}")
    print(f"  Total Gross Worth: {summary['total_gross_worth']}")
    
    print("\n" + "=" * 60 + "\n")


def iterate_dataset(split='test', max_items=5):
    """
    Iterate through multiple invoices in a dataset split.
    
    Args:
        split: Dataset split to iterate ('test', 'train', or 'validation')
        max_items: Maximum number of items to process
    """
    repo_root = Path(__file__).parent.parent
    invoice_dir = repo_root / 'data' / split / 'invoice'
    
    print(f"\n🔍 Iterating through {split} dataset (max {max_items} items):")
    print("=" * 60)
    
    # Get all invoice images
    invoice_files = sorted(invoice_dir.glob('*.png'))[:max_items]
    
    for invoice_path in invoice_files:
        invoice_id = invoice_path.stem
        label_path = repo_root / 'data' / split / 'label' / f'{invoice_id}.json'
        
        # Load data
        image = Image.open(invoice_path)
        with open(label_path, 'r', encoding='utf-8') as f:
            annotations = json.load(f)
        
        # Extract key information
        header = annotations['gt_parse']['header']
        items = annotations['gt_parse']['items']
        summary = annotations['gt_parse']['summary']
        
        print(f"\n📄 {invoice_id}")
        print(f"   Size: {image.size}")
        print(f"   Invoice #: {header['invoice_no']}")
        print(f"   Date: {header['invoice_date']}")
        print(f"   Items: {len(items)}")
        print(f"   Total: {summary['total_gross_worth']}")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """Main example execution."""
    print("\n" + "=" * 60)
    print(" " * 15 + "BASIC USAGE EXAMPLE")
    print("=" * 60)
    
    # Example 1: Load and display a single invoice
    print("\n📌 Example 1: Load a single invoice")
    image, annotations = load_single_invoice('invoice_0000', 'test')
    print(f"✅ Loaded invoice image: {image.size} pixels")
    print_invoice_details(annotations)
    
    # Example 2: Iterate through multiple invoices
    print("\n📌 Example 2: Iterate through test dataset")
    iterate_dataset('test', max_items=5)
    
    # Example 3: Dataset statistics
    print("\n📌 Example 3: Dataset statistics")
    repo_root = Path(__file__).parent.parent
    
    splits = ['test', 'train', 'validation']
    print("\n📊 Dataset Statistics:")
    print("=" * 60)
    
    for split in splits:
        invoice_dir = repo_root / 'data' / split / 'invoice'
        num_invoices = len(list(invoice_dir.glob('*.png')))
        print(f"  {split.capitalize()}: {num_invoices} invoices")
    
    print("\n" + "=" * 60)
    print("\n✅ Example complete! Check the code to see how it works.")
    print("\n💡 Next steps:")
    print("   - Explore src/dataset/use_extracted_data_example.py for more examples")
    print("   - Try AWS Bedrock extraction: cd src/bedrock && python run_extraction.py")
    print("   - Read the documentation in docs/")
    print()


if __name__ == "__main__":
    main()

