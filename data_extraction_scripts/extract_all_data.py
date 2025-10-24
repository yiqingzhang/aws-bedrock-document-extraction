"""
Extract all invoice images and annotations from parquet files.

This script processes all parquet files (train, test, validation) and extracts:
- Invoice images -> data/{split}/invoice/
- JSON annotations -> data/{split}/label/

Each file is named with the format: invoice_{index:04d}.{extension}
"""

import pandas as pd
from PIL import Image
import json
import io
from pathlib import Path
from typing import Dict


def load_image_from_parquet(image_data) -> Image.Image:
    """
    Load image from various formats stored in parquet.
    
    Args:
        image_data: Image data from parquet (can be dict, PIL Image, or numpy array)
        
    Returns:
        PIL Image object
    """
    if isinstance(image_data, dict):
        # Reason: Parquet stores images as dict with 'bytes' key
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


def extract_parquet_to_folders(
    parquet_path: str,
    output_image_dir: str,
    output_label_dir: str,
    split_name: str
):
    """
    Extract images and annotations from a parquet file to organized folders.
    
    Args:
        parquet_path: Path to the parquet file
        output_image_dir: Directory to save images
        output_label_dir: Directory to save JSON annotations
        split_name: Name of the split (train/test/validation) for logging
    """
    # Create output directories if they don't exist
    image_path = Path(output_image_dir)
    label_path = Path(output_label_dir)
    image_path.mkdir(parents=True, exist_ok=True)
    label_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"📦 Processing {split_name.upper()} split")
    print(f"{'='*60}")
    print(f"Source: {parquet_path}")
    print(f"Output images: {output_image_dir}")
    print(f"Output labels: {output_label_dir}")
    
    # Load parquet file
    df = pd.read_parquet(parquet_path)
    total_samples = len(df)
    print(f"\nFound {total_samples} samples to extract...")
    
    # Extract each sample
    for idx, row in df.iterrows():
        # Extract and save image
        image = load_image_from_parquet(row['image'])
        image_filename = f"invoice_{idx:04d}.png"
        image_filepath = image_path / image_filename
        image.save(image_filepath)
        
        # Extract and save annotations
        annotations = json.loads(row['ground_truth'])
        label_filename = f"invoice_{idx:04d}.json"
        label_filepath = label_path / label_filename
        
        # Reason: Save with readable formatting and UTF-8 encoding for special characters
        with open(label_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(annotations, json_file, indent=2, ensure_ascii=False)
        
        # Print progress every 50 samples
        if (idx + 1) % 50 == 0 or (idx + 1) == total_samples:
            print(f"  Processed {idx + 1}/{total_samples} samples...")
    
    print(f"✅ Completed {split_name} split: {total_samples} images and labels extracted")
    return total_samples


def main():
    """Main extraction process for all data splits."""
    
    print("🚀 Starting Invoice Data Extraction")
    print("="*60)
    
    # Define paths for all splits
    base_parquet_dir = "/Users/Michael.Zhang/Documents/myob/repos/ocr/invoices-donut-data-v1/data"
    base_output_dir = "/Users/Michael.Zhang/Documents/myob/repos/ocr/data"
    
    splits_config = {
        'test': {
            'parquet': f"{base_parquet_dir}/test-00000-of-00001-56af6bd5ff7eb34d.parquet",
            'image_dir': f"{base_output_dir}/test/invoice",
            'label_dir': f"{base_output_dir}/test/label"
        },
        'train': {
            'parquet': f"{base_parquet_dir}/train-00000-of-00001-a5c51039eab2980a.parquet",
            'image_dir': f"{base_output_dir}/train/invoice",
            'label_dir': f"{base_output_dir}/train/label"
        },
        'validation': {
            'parquet': f"{base_parquet_dir}/validation-00000-of-00001-b8a5c4a6237baf25.parquet",
            'image_dir': f"{base_output_dir}/validation/invoice",
            'label_dir': f"{base_output_dir}/validation/label"
        }
    }
    
    # Track statistics
    total_extracted = 0
    stats = {}
    
    # Process each split
    for split_name, config in splits_config.items():
        try:
            num_samples = extract_parquet_to_folders(
                parquet_path=config['parquet'],
                output_image_dir=config['image_dir'],
                output_label_dir=config['label_dir'],
                split_name=split_name
            )
            stats[split_name] = num_samples
            total_extracted += num_samples
        except Exception as e:
            print(f"❌ Error processing {split_name}: {e}")
            stats[split_name] = 0
    
    # Print summary
    print("\n" + "="*60)
    print("🎉 EXTRACTION COMPLETE!")
    print("="*60)
    print("\n📊 Summary Statistics:")
    for split_name, count in stats.items():
        print(f"  {split_name.capitalize():12s}: {count:3d} samples")
    print(f"  {'Total':12s}: {total_extracted:3d} samples")
    
    print("\n📁 Output Structure:")
    print(f"""
data/
├── test/
│   ├── invoice/     ({stats.get('test', 0)} images)
│   └── label/       ({stats.get('test', 0)} JSON files)
├── train/
│   ├── invoice/     ({stats.get('train', 0)} images)
│   └── label/       ({stats.get('train', 0)} JSON files)
└── validation/
    ├── invoice/     ({stats.get('validation', 0)} images)
    └── label/       ({stats.get('validation', 0)} JSON files)
""")
    
    print("✅ All invoice images and annotations have been extracted successfully!")


if __name__ == "__main__":
    main()

