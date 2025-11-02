#!/usr/bin/env python3
"""
Main Entry Point for Invoice Extraction and Evaluation

This script runs the complete pipeline:
1. Extract invoice data from all images using AWS Bedrock Claude Vision
2. Evaluate extraction accuracy against ground truth
3. Generate comprehensive performance report

Usage:
    python run_extraction.py --model claude_3_5
    python run_extraction.py --model claude_4_5
"""

import sys
import json
import argparse
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

from extract_invoices import InvoiceExtractor
from evaluate_extraction import ExtractionEvaluator


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
        description='Run invoice extraction and evaluation pipeline with configurable model.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Model configuration to use (e.g., claude_3_5, claude_4_5)',
        required=False
    )
    
    return parser.parse_args()


def print_banner():
    """Print a welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 15 + "🤖 INVOICE EXTRACTION PIPELINE 🤖")
    print("=" * 70)
    print("\nThis pipeline will:")
    print("  1️⃣  Extract invoice data from all images using Claude Vision")
    print("  2️⃣  Evaluate extraction accuracy against ground truth")
    print("  3️⃣  Generate comprehensive performance metrics")
    print("\n" + "=" * 70 + "\n")


def main():
    """
    Main pipeline execution.
    
    Runs extraction followed by evaluation, with proper error handling
    and user feedback.
    """
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
            print(f"      Model ID: {model_config['model_id']}")
            print(f"      Region: {model_config['region']}")
            print(f"      Output directory: src/bedrock/{model_config['output_subdir']}/")
        print("\nUsage examples:")
        for model_name in config.keys():
            print(f"  python run_extraction.py --model {model_name}")
        print("\n" + "=" * 70 + "\n")
        sys.exit(0)
    
    # Validate model configuration
    if args.model not in config:
        print(f"\n❌ Error: Unknown model configuration '{args.model}'")
        print(f"\nAvailable models: {', '.join(config.keys())}")
        sys.exit(1)
    
    # Get model configuration
    model_config = config[args.model]
    model_id = model_config['model_id']
    region = model_config['region']
    output_subdir = model_config['output_subdir']
    
    print_banner()
    print(f"📦 Using model configuration: {args.model}")
    print(f"   Model ID: {model_id}")
    print(f"   Region: {region}")
    print()
    
    # Setup paths using configured output subdirectory
    # Reason: Use absolute paths relative to script location for reliability
    base_dir = Path(__file__).parent.parent.parent  # Go up to repository root
    data_dir = base_dir / 'data'
    output_dir = Path(__file__).parent / output_subdir / 'output'
    logs_dir = Path(__file__).parent / output_subdir / 'logs'
    
    try:
        # ============================================================
        # STEP 1: EXTRACTION
        # ============================================================
        print("🚀 STEP 1: INVOICE EXTRACTION")
        print("=" * 70)
        print(f"📂 Data directory: {data_dir}")
        print(f"📂 Output directory: {output_dir}")
        print(f"📂 Logs directory: {logs_dir}")
        print()
        
        # Confirm with user (optional)
        print("⚠️  Note: This will process 501 invoices using AWS Bedrock.")
        print("⚠️  Estimated cost: ~$0.50-1.00 USD (depends on image sizes)")
        print("⚠️  Estimated time: ~15-30 minutes")
        print()
        
        response = input("Continue? [y/N]: ").strip().lower()
        if response != 'y':
            print("\n❌ Extraction cancelled by user.")
            return
        
        print("\n" + "-" * 70 + "\n")
        
        # Initialize and run extractor with configured model
        extractor = InvoiceExtractor(
            data_dir=str(data_dir),
            output_dir=str(output_dir),
            logs_dir=str(logs_dir),
            model_id=model_id,
            region=region
        )
        
        extraction_stats = extractor.run_extraction()
        
        # Check if extraction was successful
        if extraction_stats['failed'] > 0:
            print(f"\n⚠️  Warning: {extraction_stats['failed']} invoices failed to extract.")
            print(f"Check {logs_dir / 'failed_invoices.log'} for details.")
        
        # ============================================================
        # STEP 2: EVALUATION
        # ============================================================
        print("\n\n🚀 STEP 2: EVALUATION")
        print("=" * 70 + "\n")
        
        # Initialize and run evaluator
        evaluator = ExtractionEvaluator(
            output_dir=str(output_dir),
            logs_dir=str(logs_dir)
        )
        
        evaluation_metrics = evaluator.run_evaluation()
        
        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("\n\n" + "=" * 70)
        print(" " * 20 + "🎉 PIPELINE COMPLETE! 🎉")
        print("=" * 70)
        
        print("\n📊 Quick Summary:")
        print(f"  Total invoices: {evaluation_metrics['total_invoices']}")
        print(f"  Successful: {evaluation_metrics['successful_extractions']}")
        print(f"  Failed: {evaluation_metrics['failed_extractions']}")
        print(f"  Overall accuracy: {evaluation_metrics['overall_accuracy']['accuracy']:.2%}")
        
        print("\n📁 Output Files:")
        print(f"  Extraction results: {output_dir}/")
        print(f"  Evaluation report: {logs_dir / 'evaluation_report.json'}")
        print(f"  Evaluation summary: {logs_dir / 'evaluation_summary.json'}")
        print(f"  Extraction stats: {logs_dir / 'extraction_stats.json'}")
        
        if extraction_stats['failed'] > 0:
            print(f"  Failed invoices log: {logs_dir / 'failed_invoices.log'}")
        
        print("\n" + "=" * 70 + "\n")
        
        print("✅ All done! Check the files above for detailed results.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user.")
        print("Progress has been saved. You can resume by running this script again.")
        print("Already processed invoices will be skipped automatically.")
        sys.exit(1)
        
    except Exception as error:
        print(f"\n\n❌ Fatal error in pipeline: {error}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


