#!/usr/bin/env python3
"""
Unit tests for dataset utilities

Run with: pytest tests/test_dataset.py
"""

import pytest
from pathlib import Path
from PIL import Image
import json


class TestDatasetStructure:
    """Tests for dataset structure and integrity."""
    
    def test_data_directory_exists(self):
        """Test that data directory exists."""
        data_dir = Path('data')
        assert data_dir.exists(), "Data directory not found"
        assert data_dir.is_dir(), "Data path is not a directory"
    
    def test_required_splits_exist(self):
        """Test that all required data splits exist."""
        data_dir = Path('data')
        required_splits = ['test', 'train', 'validation']
        
        for split in required_splits:
            split_dir = data_dir / split
            assert split_dir.exists(), f"Split directory not found: {split}"
            
            invoice_dir = split_dir / 'invoice'
            label_dir = split_dir / 'label'
            
            assert invoice_dir.exists(), f"Invoice directory not found: {split}/invoice"
            assert label_dir.exists(), f"Label directory not found: {split}/label"
    
    def test_matching_invoice_label_counts(self):
        """Test that invoice and label counts match for each split."""
        data_dir = Path('data')
        splits = ['test', 'train', 'validation']
        
        for split in splits:
            invoice_dir = data_dir / split / 'invoice'
            label_dir = data_dir / split / 'label'
            
            invoices = list(invoice_dir.glob('*.png'))
            labels = list(label_dir.glob('*.json'))
            
            assert len(invoices) == len(labels), \
                f"Mismatch in {split}: {len(invoices)} invoices vs {len(labels)} labels"


class TestInvoiceImages:
    """Tests for invoice image files."""
    
    def test_load_sample_invoice(self):
        """Test loading a sample invoice image."""
        image_path = Path('data/test/invoice/invoice_0000.png')
        
        if not image_path.exists():
            pytest.skip("Sample image not found")
        
        image = Image.open(image_path)
        
        # Check image properties
        assert image.mode == 'RGB', "Image should be RGB"
        assert image.size[0] > 0 and image.size[1] > 0, "Image has invalid dimensions"
    
    def test_all_invoices_are_readable(self):
        """Test that all invoice images can be opened."""
        data_dir = Path('data')
        test_invoices = list((data_dir / 'test' / 'invoice').glob('*.png'))[:5]  # Test first 5
        
        for invoice_path in test_invoices:
            try:
                image = Image.open(invoice_path)
                assert image is not None, f"Failed to load image: {invoice_path}"
            except Exception as e:
                pytest.fail(f"Error loading {invoice_path}: {e}")


class TestInvoiceLabels:
    """Tests for invoice label files."""
    
    def test_load_sample_label(self):
        """Test loading a sample invoice label."""
        label_path = Path('data/test/label/invoice_0000.json')
        
        if not label_path.exists():
            pytest.skip("Sample label not found")
        
        with open(label_path, 'r', encoding='utf-8') as f:
            label = json.load(f)
        
        # Check required structure
        assert 'gt_parse' in label, "Missing gt_parse key"
        assert 'header' in label['gt_parse'], "Missing header"
        assert 'items' in label['gt_parse'], "Missing items"
        assert 'summary' in label['gt_parse'], "Missing summary"
    
    def test_header_required_fields(self):
        """Test that invoice header has required fields."""
        label_path = Path('data/test/label/invoice_0000.json')
        
        if not label_path.exists():
            pytest.skip("Sample label not found")
        
        with open(label_path, 'r', encoding='utf-8') as f:
            label = json.load(f)
        
        header = label['gt_parse']['header']
        required_fields = ['invoice_no', 'invoice_date', 'seller', 'client']
        
        for field in required_fields:
            assert field in header, f"Missing required field: {field}"
    
    def test_items_structure(self):
        """Test that invoice items have correct structure."""
        label_path = Path('data/test/label/invoice_0000.json')
        
        if not label_path.exists():
            pytest.skip("Sample label not found")
        
        with open(label_path, 'r', encoding='utf-8') as f:
            label = json.load(f)
        
        items = label['gt_parse']['items']
        assert isinstance(items, list), "Items should be a list"
        
        if len(items) > 0:
            item = items[0]
            expected_fields = ['item_desc', 'item_qty', 'item_net_price']
            
            for field in expected_fields:
                assert field in item, f"Missing item field: {field}"
    
    def test_summary_structure(self):
        """Test that invoice summary has correct structure."""
        label_path = Path('data/test/label/invoice_0000.json')
        
        if not label_path.exists():
            pytest.skip("Sample label not found")
        
        with open(label_path, 'r', encoding='utf-8') as f:
            label = json.load(f)
        
        summary = label['gt_parse']['summary']
        required_fields = ['total_net_worth', 'total_vat', 'total_gross_worth']
        
        for field in required_fields:
            assert field in summary, f"Missing summary field: {field}"


class TestDatasetStatistics:
    """Tests for dataset statistics."""
    
    def test_expected_split_sizes(self):
        """Test that splits have expected number of samples."""
        data_dir = Path('data')
        
        expected_counts = {
            'test': 26,
            'train': 425,
            'validation': 50
        }
        
        for split, expected_count in expected_counts.items():
            invoice_dir = data_dir / split / 'invoice'
            actual_count = len(list(invoice_dir.glob('*.png')))
            
            assert actual_count == expected_count, \
                f"{split} split: expected {expected_count}, got {actual_count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

