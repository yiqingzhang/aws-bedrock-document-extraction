"""
Invoice Dataset Helper Class

Provides easy access to invoice images and annotations from parquet files.
This dataset contains invoice documents with OCR ground truth annotations.
"""

import pandas as pd
from PIL import Image
import json
import io
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class InvoiceDataset:
    """
    Helper class to load and access invoice dataset from parquet files.
    
    Each sample contains:
    - image: Invoice image (PIL Image)
    - ground_truth: Structured annotations with header, items, and summary
    """
    
    def __init__(self, parquet_path: str):
        """
        Initialize the dataset.
        
        Args:
            parquet_path: Path to the parquet file
        """
        self.parquet_path = parquet_path
        self.df = pd.read_parquet(parquet_path)
        print(f"✅ Loaded {len(self.df)} invoice samples from {Path(parquet_path).name}")
    
    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return len(self.df)
    
    def __getitem__(self, idx: int) -> Dict:
        """
        Get a single sample by index.
        
        Args:
            idx: Sample index
            
        Returns:
            Dictionary with 'image' (PIL Image) and 'annotations' (dict)
        """
        row = self.df.iloc[idx]
        return {
            'image': self._load_image(row['image']),
            'annotations': json.loads(row['ground_truth'])
        }
    
    def _load_image(self, image_data) -> Image.Image:
        """
        Load image from various formats stored in parquet.
        
        Reason: Parquet can store images in different formats (dict with bytes, numpy array, etc.)
        """
        if isinstance(image_data, dict):
            if 'bytes' in image_data:
                return Image.open(io.BytesIO(image_data['bytes']))
            else:
                return Image.fromarray(image_data)
        elif hasattr(image_data, 'size'):
            # Reason: Already a PIL Image
            return image_data
        else:
            # Reason: Likely a numpy array
            return Image.fromarray(image_data)
    
    def get_sample(self, idx: int) -> Dict:
        """
        Get a detailed sample with all information.
        
        Args:
            idx: Sample index
            
        Returns:
            Dictionary containing:
            - image: PIL Image object
            - header: Invoice header information
            - items: List of line items
            - summary: Invoice summary totals
        """
        sample = self[idx]
        annotations = sample['annotations']['gt_parse']
        
        return {
            'image': sample['image'],
            'header': annotations.get('header', {}),
            'items': annotations.get('items', []),
            'summary': annotations.get('summary', {})
        }
    
    def save_image(self, idx: int, output_path: str):
        """
        Save a specific invoice image to disk.
        
        Args:
            idx: Sample index
            output_path: Path to save the image
        """
        sample = self[idx]
        sample['image'].save(output_path)
        print(f"💾 Saved image {idx} to {output_path}")
    
    def export_all_images(self, output_dir: str):
        """
        Export all images to a directory.
        
        Args:
            output_dir: Directory to save images
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for idx in range(len(self)):
            image_file = output_path / f"invoice_{idx:04d}.png"
            self.save_image(idx, str(image_file))
        
        print(f"✅ Exported all {len(self)} images to {output_dir}")
    
    def get_statistics(self) -> Dict:
        """
        Get dataset statistics.
        
        Returns:
            Dictionary with dataset statistics
        """
        total_items = 0
        invoice_numbers = []
        
        for idx in range(len(self)):
            sample = self.get_sample(idx)
            total_items += len(sample['items'])
            invoice_numbers.append(sample['header'].get('invoice_no', 'N/A'))
        
        return {
            'total_invoices': len(self),
            'total_line_items': total_items,
            'avg_items_per_invoice': total_items / len(self) if len(self) > 0 else 0,
            'sample_invoice_numbers': invoice_numbers[:5]
        }
    
    def print_sample_details(self, idx: int):
        """
        Print detailed information about a specific sample.
        
        Args:
            idx: Sample index
        """
        sample = self.get_sample(idx)
        
        print(f"\n{'='*60}")
        print(f"📄 Invoice Sample #{idx}")
        print(f"{'='*60}")
        
        print("\n📋 HEADER:")
        for key, value in sample['header'].items():
            print(f"  {key}: {value}")
        
        print(f"\n📦 ITEMS ({len(sample['items'])} total):")
        for i, item in enumerate(sample['items'], 1):
            print(f"\n  Item {i}:")
            for key, value in item.items():
                print(f"    {key}: {value}")
        
        print("\n💰 SUMMARY:")
        for key, value in sample['summary'].items():
            print(f"  {key}: {value}")
        
        print(f"\n🖼️  IMAGE:")
        print(f"  Size: {sample['image'].size}")
        print(f"  Mode: {sample['image'].mode}")


# Example usage demonstration
if __name__ == "__main__":
    # Load the test dataset
    test_data_path = "/Users/Michael.Zhang/Documents/myob/repos/ocr/invoices-donut-data-v1/data/test-00000-of-00001-56af6bd5ff7eb34d.parquet"
    
    dataset = InvoiceDataset(test_data_path)
    
    print(f"\n📊 Dataset has {len(dataset)} samples")
    
    # Show statistics
    stats = dataset.get_statistics()
    print("\n📈 Dataset Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show first sample details
    dataset.print_sample_details(0)
    
    # Access data programmatically
    print("\n" + "="*60)
    print("💡 How to Use This Class:")
    print("="*60)
    print("""
from invoice_dataset import InvoiceDataset

# Load dataset
dataset = InvoiceDataset('path/to/data.parquet')

# Get total number of samples
print(f"Total samples: {len(dataset)}")

# Access a specific sample
sample = dataset[0]
image = sample['image']  # PIL Image
annotations = sample['annotations']  # Dict with all annotations

# Or get structured data
sample = dataset.get_sample(0)
header = sample['header']  # Invoice header info
items = sample['items']    # List of line items
summary = sample['summary'] # Invoice totals

# Save an image
dataset.save_image(0, 'output.png')

# Export all images
dataset.export_all_images('output_directory/')

# Iterate through all samples
for idx in range(len(dataset)):
    sample = dataset.get_sample(idx)
    # Process each invoice...
""")

