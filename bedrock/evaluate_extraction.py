#!/usr/bin/env python3
"""
Invoice Extraction Evaluation Script

This script evaluates the performance of invoice extraction by comparing
extracted fields against ground truth labels. It calculates per-field
accuracy and overall accuracy metrics.

Evaluation metrics:
- Per-field exact match accuracy
- Overall accuracy (all 5 fields correct)
- Success rate (extraction completed without errors)

Usage:
    python evaluate_extraction.py --model claude_3_5
    python evaluate_extraction.py --model claude_4_5
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime


def load_config():
    """
    Load model configuration from config.json.
    
    Returns:
        dict: Configuration dictionary with model settings
    
    Raises:
        Exception: If config file cannot be loaded
    """
    config_path = Path(__file__).parent / 'config.json'
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise Exception(f"❌ Configuration file not found: {config_path}")
    except json.JSONDecodeError as error:
        raise Exception(f"❌ Invalid JSON in configuration file: {error}")


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Evaluate invoice extraction results with configurable model output directory.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Model configuration to use (e.g., claude_3_5, claude_4_5)',
        required=False
    )
    
    return parser.parse_args()


class ExtractionEvaluator:
    """
    Evaluates invoice extraction results against ground truth.
    
    Calculates:
    - Exact match accuracy for each field
    - Overall accuracy (all fields correct)
    - Processing statistics
    """
    
    def __init__(self, output_dir, logs_dir):
        """
        Initialize the evaluator.
        
        Args:
            output_dir (str): Path to directory containing extraction results
            logs_dir (str): Path to directory for saving evaluation report
        """
        self.output_dir = Path(output_dir)
        self.logs_dir = Path(logs_dir)
        
        # Evaluation metrics
        self.metrics = {
            'total_invoices': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'field_accuracy': {
                'invoice_no': {'correct': 0, 'total': 0, 'accuracy': 0.0},
                'invoice_date': {'correct': 0, 'total': 0, 'accuracy': 0.0},
                'total_gross_worth': {'correct': 0, 'total': 0, 'accuracy': 0.0},
                'seller': {'correct': 0, 'total': 0, 'accuracy': 0.0},
                'client': {'correct': 0, 'total': 0, 'accuracy': 0.0}
            },
            'overall_accuracy': {'correct': 0, 'total': 0, 'accuracy': 0.0},
            'evaluation_timestamp': None
        }
        
        # Store detailed results for analysis
        self.detailed_results = []
    
    def normalize_string(self, text):
        """
        Normalize a string for comparison with aggressive whitespace handling.
        
        Handles:
        - Removes ALL whitespace (spaces, tabs, newlines)
        - Case normalization (lowercase)
        - Empty string handling
        
        This treats values that differ only in whitespace as matches.
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Normalized text with all whitespace removed
        """
        if text is None:
            return ""
        # Reason: Aggressive normalization treats whitespace-only differences as matches
        return re.sub(r'\s+', '', str(text).strip()).lower()
    
    def exact_match(self, extracted, ground_truth):
        """
        Check if extracted value exactly matches ground truth.
        
        Uses normalized comparison (whitespace and case-insensitive).
        
        Args:
            extracted (str): Extracted value
            ground_truth (str): Ground truth value
            
        Returns:
            bool: True if values match, False otherwise
        """
        return self.normalize_string(extracted) == self.normalize_string(ground_truth)
    
    def evaluate_invoice(self, result_data):
        """
        Evaluate a single invoice extraction result.
        
        Args:
            result_data (dict): Extraction result containing extracted and ground_truth
            
        Returns:
            dict: Evaluation details for this invoice including field-by-field comparison
        """
        invoice_eval = {
            'source_file': result_data.get('source_file', 'unknown'),
            'success': result_data.get('success', False),
            'field_matches': {},
            'field_details': {},
            'all_correct': False
        }
        
        # Check if extraction was successful
        if not result_data.get('success', False):
            return invoice_eval
        
        extracted = result_data.get('extracted', {})
        ground_truth = result_data.get('ground_truth', {})
        
        # Evaluate each field
        fields = ['invoice_no', 'invoice_date', 'total_gross_worth', 'seller', 'client']
        all_correct = True
        
        for field in fields:
            extracted_value = extracted.get(field, '')
            ground_truth_value = ground_truth.get(field, '')
            
            is_match = self.exact_match(extracted_value, ground_truth_value)
            invoice_eval['field_matches'][field] = is_match
            
            # Reason: Store detailed comparison data for debugging and analysis
            invoice_eval['field_details'][field] = {
                'ground_truth': ground_truth_value,
                'extracted': extracted_value,
                'match': is_match
            }
            
            # Update field accuracy metrics
            self.metrics['field_accuracy'][field]['total'] += 1
            if is_match:
                self.metrics['field_accuracy'][field]['correct'] += 1
            else:
                all_correct = False
        
        # Update overall accuracy
        invoice_eval['all_correct'] = all_correct
        self.metrics['overall_accuracy']['total'] += 1
        if all_correct:
            self.metrics['overall_accuracy']['correct'] += 1
        
        return invoice_eval
    
    def load_extraction_results(self):
        """
        Load all extraction result files from output directory.
        
        Returns:
            list: List of extraction result dictionaries
        """
        results = []
        
        # Reason: Sort files for consistent ordering
        result_files = sorted(self.output_dir.glob('*_extracted.json'))
        
        if not result_files:
            print("⚠️  No extraction result files found!")
            return results
        
        print(f"📂 Found {len(result_files)} result files")
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    results.append(result_data)
            except Exception as error:
                print(f"⚠️  Error loading {result_file}: {error}")
        
        return results
    
    def calculate_final_metrics(self):
        """
        Calculate final accuracy percentages for all metrics.
        """
        # Calculate per-field accuracies
        for field in self.metrics['field_accuracy']:
            total = self.metrics['field_accuracy'][field]['total']
            correct = self.metrics['field_accuracy'][field]['correct']
            
            if total > 0:
                accuracy = correct / total
                self.metrics['field_accuracy'][field]['accuracy'] = round(accuracy, 4)
        
        # Calculate overall accuracy
        total = self.metrics['overall_accuracy']['total']
        correct = self.metrics['overall_accuracy']['correct']
        
        if total > 0:
            accuracy = correct / total
            self.metrics['overall_accuracy']['accuracy'] = round(accuracy, 4)
    
    def run_evaluation(self):
        """
        Main evaluation process: load results and calculate metrics.
        
        Returns:
            dict: Evaluation metrics
        """
        print("📊 Starting Extraction Evaluation")
        print("=" * 60)
        
        # Load all extraction results
        print("\n📂 Loading extraction results...")
        results = self.load_extraction_results()
        
        if not results:
            print("❌ No results to evaluate!")
            return self.metrics
        
        self.metrics['total_invoices'] = len(results)
        print(f"Loaded {len(results)} extraction results")
        
        # Evaluate each result
        print("\n🔍 Evaluating extractions...")
        for idx, result_data in enumerate(results, 1):
            invoice_eval = self.evaluate_invoice(result_data)
            self.detailed_results.append(invoice_eval)
            
            # Track success/failure
            if result_data.get('success', False):
                self.metrics['successful_extractions'] += 1
            else:
                self.metrics['failed_extractions'] += 1
            
            # Progress indicator
            if idx % 50 == 0:
                print(f"  Evaluated {idx}/{len(results)} results...")
        
        # Calculate final metrics
        self.calculate_final_metrics()
        self.metrics['evaluation_timestamp'] = datetime.now().isoformat()
        
        # Print evaluation report
        self.print_report()
        
        # Save detailed report
        self.save_report()
        
        return self.metrics
    
    def print_report(self):
        """
        Print a formatted evaluation report to console.
        """
        print("\n" + "=" * 60)
        print("📋 EVALUATION REPORT")
        print("=" * 60)
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total invoices: {self.metrics['total_invoices']}")
        print(f"  ✅ Successful extractions: {self.metrics['successful_extractions']}")
        print(f"  ❌ Failed extractions: {self.metrics['failed_extractions']}")
        
        success_rate = 0.0
        if self.metrics['total_invoices'] > 0:
            success_rate = self.metrics['successful_extractions'] / self.metrics['total_invoices']
        print(f"  📈 Success rate: {success_rate:.2%}")
        
        print(f"\n🎯 Per-Field Accuracy (Exact Match):")
        for field, data in self.metrics['field_accuracy'].items():
            correct = data['correct']
            total = data['total']
            accuracy = data['accuracy']
            print(f"  {field:20s}: {correct:3d}/{total:3d} = {accuracy:.2%}")
        
        overall = self.metrics['overall_accuracy']
        print(f"\n🏆 Overall Accuracy (All 5 Fields Correct):")
        print(f"  {overall['correct']}/{overall['total']} = {overall['accuracy']:.2%}")
        
        print("\n" + "=" * 60)
    
    def save_report(self):
        """
        Save detailed evaluation report to JSON file.
        """
        report_file = self.logs_dir / 'evaluation_report.json'
        
        report = {
            'metrics': self.metrics,
            'detailed_results': self.detailed_results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
        
        # Also save a summary report (metrics only)
        summary_file = self.logs_dir / 'evaluation_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Summary report saved to: {summary_file}")


def main():
    """Main entry point for evaluation."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    try:
        config = load_config()
    except Exception as error:
        print(f"\n{error}")
        sys.exit(1)
    
    # Check if model is specified, otherwise show available models
    if not args.model:
        print("\n" + "=" * 70)
        print(" " * 15 + "⚙️  MODEL CONFIGURATION REQUIRED ⚙️")
        print("=" * 70)
        print("\nPlease specify a model configuration using the --model flag.")
        print("\nAvailable models:")
        for model_name, model_config in config.items():
            print(f"\n  📦 {model_name}")
            print(f"      Output directory: bedrock/{model_config['output_subdir']}/")
        print("\nUsage examples:")
        for model_name in config.keys():
            print(f"  python evaluate_extraction.py --model {model_name}")
        print("\n" + "=" * 70 + "\n")
        sys.exit(0)
    
    # Validate model configuration
    if args.model not in config:
        print(f"\n❌ Error: Unknown model configuration '{args.model}'")
        print(f"\nAvailable models: {', '.join(config.keys())}")
        sys.exit(1)
    
    # Get model configuration
    model_config = config[args.model]
    output_subdir = model_config['output_subdir']
    
    # Reason: Use absolute paths to ensure correct file access
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'bedrock' / output_subdir / 'output'
    logs_dir = base_dir / 'bedrock' / output_subdir / 'logs'
    
    print(f"\n📦 Evaluating results for model: {args.model}")
    print(f"   Output directory: {output_dir}")
    print(f"   Logs directory: {logs_dir}\n")
    
    try:
        evaluator = ExtractionEvaluator(
            output_dir=str(output_dir),
            logs_dir=str(logs_dir)
        )
        
        evaluator.run_evaluation()
        
    except Exception as error:
        print(f"\n❌ Fatal error: {error}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


