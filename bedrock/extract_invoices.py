#!/usr/bin/env python3
"""
Invoice Extraction Script

This script processes all invoice images from the data/ directory using AWS Bedrock
Claude Vision API to extract key invoice fields. Results are saved for evaluation.

Key features:
- Processes invoices from test, train, and validation splits
- Extracts: invoice_no, invoice_date, total_gross_worth, seller, client
- Implements checkpoint/resume capability
- Saves extraction results with ground truth for evaluation
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from bedrock_vision_client import BedrockVisionClient


class InvoiceExtractor:
    """
    Manages the extraction of invoice data from images using Claude Vision.
    
    Handles:
    - Scanning invoice files from multiple data splits
    - Extracting data using Bedrock Vision API
    - Saving results with ground truth for evaluation
    - Progress tracking and resume capability
    """
    
    def __init__(self, data_dir, output_dir, logs_dir, model_id, region):
        """
        Initialize the invoice extractor.
        
        Args:
            data_dir (str): Path to the data directory containing splits
            output_dir (str): Path to save extraction results
            logs_dir (str): Path to save log files
            model_id (str): The Claude model ID to use for extraction
            region (str): AWS region name for Bedrock service
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.logs_dir = Path(logs_dir)
        
        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Bedrock client with configured model
        # Reason: Pass model_id and region to allow different model configurations
        self.client = BedrockVisionClient(model_id=model_id, region_name=region)
        
        # Statistics tracking
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None
        }
    
    def collect_all_invoices(self):
        """
        Collect all invoice file paths from test, train, and validation splits.
        
        Returns:
            list: List of tuples (image_path, label_path, output_filename)
        """
        invoices = []
        splits = ['test', 'train', 'validation']
        
        for split in splits:
            invoice_dir = self.data_dir / split / 'invoice'
            label_dir = self.data_dir / split / 'label'
            
            if not invoice_dir.exists():
                print(f"⚠️  Warning: {invoice_dir} does not exist, skipping...")
                continue
            
            # Get all invoice images
            # Reason: Sort to ensure consistent processing order
            invoice_files = sorted(invoice_dir.glob('invoice_*.png'))
            
            for invoice_path in invoice_files:
                # Construct corresponding label path
                label_filename = invoice_path.stem + '.json'
                label_path = label_dir / label_filename
                
                # Create unique output filename including split name
                # Reason: Avoid filename collisions between splits
                output_filename = f"{split}_{invoice_path.stem}_extracted.json"
                
                if label_path.exists():
                    invoices.append((invoice_path, label_path, output_filename))
                else:
                    print(f"⚠️  Warning: Label file not found for {invoice_path}, skipping...")
        
        return invoices
    
    def load_ground_truth(self, label_path):
        """
        Load ground truth data from label JSON file.
        
        NOTE: This data is only for evaluation - it is NOT sent to the model!
        
        Args:
            label_path (Path): Path to the label JSON file
            
        Returns:
            dict: Ground truth data with extracted fields
        """
        try:
            with open(label_path, 'r', encoding='utf-8') as f:
                label_data = json.load(f)
            
            # Extract the 5 fields we're interested in from gt_parse structure
            gt_parse = label_data.get('gt_parse', {})
            header = gt_parse.get('header', {})
            summary = gt_parse.get('summary', {})
            
            ground_truth = {
                'invoice_no': header.get('invoice_no', ''),
                'invoice_date': header.get('invoice_date', ''),
                'total_gross_worth': summary.get('total_gross_worth', ''),
                'seller': header.get('seller', ''),
                'client': header.get('client', '')
            }
            
            return ground_truth
            
        except Exception as error:
            print(f"❌ Error loading ground truth from {label_path}: {error}")
            return None
    
    def process_invoice(self, invoice_path, label_path, output_filename):
        """
        Process a single invoice: extract data and save results.
        
        Args:
            invoice_path (Path): Path to invoice image
            label_path (Path): Path to ground truth label
            output_filename (str): Filename for output JSON
            
        Returns:
            bool: True if successful, False otherwise
        """
        output_path = self.output_dir / output_filename
        
        # Check if already processed (checkpoint/resume capability)
        # Reason: Allow resuming from interruptions without reprocessing
        if output_path.exists():
            print(f"  ⏭️  Skipping {invoice_path.name} (already processed)")
            self.stats['skipped'] += 1
            return True
        
        try:
            # Load ground truth (for evaluation only - NOT sent to model)
            ground_truth = self.load_ground_truth(label_path)
            if ground_truth is None:
                return False
            
            # Extract invoice data using Claude Vision
            print(f"  🔍 Processing {invoice_path.name}...")
            start_time = time.time()
            
            extracted_data = self.client.extract_invoice_data(str(invoice_path))
            
            processing_time = time.time() - start_time
            
            # Prepare result object
            result = {
                'source_file': str(invoice_path),
                'ground_truth': ground_truth,
                'extracted': extracted_data,
                'processing_time': round(processing_time, 2),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save result
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Completed in {processing_time:.2f}s")
            self.stats['successful'] += 1
            return True
            
        except Exception as error:
            print(f"  ❌ Failed to process {invoice_path.name}: {error}")
            
            # Save failure record
            failure_result = {
                'source_file': str(invoice_path),
                'success': False,
                'error': str(error),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(failure_result, f, indent=2, ensure_ascii=False)
            
            # Log to failed invoices file
            with open(self.logs_dir / 'failed_invoices.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()} | {invoice_path} | {error}\n")
            
            self.stats['failed'] += 1
            return False
    
    def run_extraction(self):
        """
        Main extraction process: collect and process all invoices.
        
        Returns:
            dict: Statistics about the extraction process
        """
        print("🚀 Starting Invoice Extraction")
        print("=" * 60)
        
        # Test connection first
        print("\n🔍 Testing AWS Bedrock connection...")
        if not self.client.test_connection():
            raise Exception("Failed to connect to AWS Bedrock. Please check your credentials.")
        
        # Collect all invoices
        print("\n📊 Collecting invoice files...")
        invoices = self.collect_all_invoices()
        total_invoices = len(invoices)
        print(f"Found {total_invoices} invoices to process")
        
        if total_invoices == 0:
            print("❌ No invoices found to process!")
            return self.stats
        
        # Start processing
        self.stats['start_time'] = datetime.now().isoformat()
        print(f"\n⏰ Started at: {self.stats['start_time']}")
        print("=" * 60)
        
        start_timestamp = time.time()
        
        for idx, (invoice_path, label_path, output_filename) in enumerate(invoices, 1):
            print(f"\n[{idx}/{total_invoices}] Processing invoice...")
            
            self.process_invoice(invoice_path, label_path, output_filename)
            self.stats['total_processed'] = idx
            
            # Print progress summary every 10 invoices
            # Reason: Provide regular feedback without overwhelming the console
            if idx % 10 == 0:
                elapsed_time = time.time() - start_timestamp
                avg_time_per_invoice = elapsed_time / idx
                remaining_invoices = total_invoices - idx
                eta_seconds = avg_time_per_invoice * remaining_invoices
                
                print("\n" + "=" * 60)
                print(f"📈 Progress: {idx}/{total_invoices} ({idx/total_invoices*100:.1f}%)")
                print(f"✅ Successful: {self.stats['successful']}")
                print(f"❌ Failed: {self.stats['failed']}")
                print(f"⏭️  Skipped: {self.stats['skipped']}")
                print(f"⏱️  Avg time/invoice: {avg_time_per_invoice:.2f}s")
                print(f"⏰ ETA: {eta_seconds/60:.1f} minutes")
                print("=" * 60)
        
        # Final summary
        self.stats['end_time'] = datetime.now().isoformat()
        total_time = time.time() - start_timestamp
        
        print("\n" + "=" * 60)
        print("🎉 EXTRACTION COMPLETE!")
        print("=" * 60)
        print(f"📊 Final Statistics:")
        print(f"  Total processed: {self.stats['total_processed']}")
        print(f"  ✅ Successful: {self.stats['successful']}")
        print(f"  ❌ Failed: {self.stats['failed']}")
        print(f"  ⏭️  Skipped: {self.stats['skipped']}")
        print(f"  ⏱️  Total time: {total_time/60:.1f} minutes")
        print(f"  ⏱️  Avg time per invoice: {total_time/total_invoices:.2f}s")
        print("=" * 60)
        
        # Save statistics
        stats_file = self.logs_dir / 'extraction_stats.json'
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"\n📝 Statistics saved to: {stats_file}")
        
        return self.stats


def main():
    """Main entry point for invoice extraction."""
    # Reason: Use absolute paths to ensure correct file access
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'bedrock' / 'output'
    logs_dir = base_dir / 'bedrock' / 'logs'
    
    # Reason: Use default Claude 4.5 model for standalone execution
    default_model_id = 'au.anthropic.claude-sonnet-4-5-20250929-v1:0'
    default_region = 'ap-southeast-2'
    
    try:
        extractor = InvoiceExtractor(
            data_dir=str(data_dir),
            output_dir=str(output_dir),
            logs_dir=str(logs_dir),
            model_id=default_model_id,
            region=default_region
        )
        
        extractor.run_extraction()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user. Progress has been saved.")
        print("You can resume by running this script again.")
    except Exception as error:
        print(f"\n❌ Fatal error: {error}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


