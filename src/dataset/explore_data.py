"""
Script to explore the invoice dataset in parquet format.

This dataset contains invoice images with ground truth annotations for OCR/document understanding.
Each row has:
- image: The actual invoice image
- ground_truth: JSON string with annotations
"""

import pandas as pd
from PIL import Image
import json
import io

# Reason: Using absolute path to ensure correct file access
parquet_file = "/Users/Michael.Zhang/Documents/myob/repos/ocr/invoices-donut-data-v1/data/test-00000-of-00001-56af6bd5ff7eb34d.parquet"

# Load the parquet file
print("Loading parquet file...")
df = pd.read_parquet(parquet_file)

print(f"\n📊 Dataset Overview:")
print(f"  - Number of samples: {len(df)}")
print(f"  - Columns: {df.columns.tolist()}")
print(f"  - Data types:\n{df.dtypes}\n")

# Examine the first sample
print("=" * 60)
print("🔍 Exploring First Sample:")
print("=" * 60)

first_sample = df.iloc[0]

# Display ground truth
print("\n📝 Ground Truth (annotations):")
ground_truth = json.loads(first_sample['ground_truth'])
print(json.dumps(ground_truth, indent=2))

# Access the image
print("\n🖼️  Image Information:")
image = first_sample['image']
if isinstance(image, dict):
    # Reason: Parquet can store images as dict with 'bytes' key
    if 'bytes' in image:
        img = Image.open(io.BytesIO(image['bytes']))
    else:
        # Try to convert dict to image
        img = Image.fromarray(image)
else:
    # It might already be a PIL Image or numpy array
    if hasattr(image, 'size'):
        img = image
    else:
        img = Image.fromarray(image)

print(f"  - Size: {img.size} (width x height)")
print(f"  - Mode: {img.mode}")
print(f"  - Format: {img.format if hasattr(img, 'format') else 'N/A'}")

# Save first image as example
output_image_path = "/Users/Michael.Zhang/Documents/myob/repos/ocr/sample_invoice.png"
img.save(output_image_path)
print(f"\n✅ Saved first invoice image to: {output_image_path}")

# Save the corresponding annotations as JSON
output_json_path = "/Users/Michael.Zhang/Documents/myob/repos/ocr/sample_invoice_annotations.json"
# Reason: Save ground truth in readable format for inspection
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(ground_truth, json_file, indent=2, ensure_ascii=False)
print(f"✅ Saved first invoice annotations to: {output_json_path}")

# Show how to iterate through all samples
print("\n" + "=" * 60)
print("📚 All Samples Summary:")
print("=" * 60)
for idx, row in df.iterrows():
    gt = json.loads(row['ground_truth'])
    print(f"\nSample {idx}:")
    print(f"  - Ground truth keys: {list(gt.keys())}")
    if 'gt_parse' in gt:
        print(f"  - Parsed fields: {list(gt['gt_parse'].keys())}")
    
    # Reason: Only show first 3 to avoid overwhelming output
    if idx >= 2:
        print(f"\n... and {len(df) - 3} more samples")
        break

print("\n" + "=" * 60)
print("💡 Usage Example:")
print("=" * 60)
print("""
# Access a specific sample:
sample = df.iloc[0]
image = sample['image']
annotations = json.loads(sample['ground_truth'])

# Iterate through all samples:
for idx, row in df.iterrows():
    image = row['image']
    ground_truth = json.loads(row['ground_truth'])
    # Process your data here...
""")

