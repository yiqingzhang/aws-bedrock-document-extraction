#!/usr/bin/env python3
"""
Model Performance Comparison Script

This script compares the performance of different Claude models on invoice extraction
by generating side-by-side bar charts showing field accuracy and overall accuracy.

Usage:
    python compare_models.py
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_evaluation_summary(model_name):
    """
    Load evaluation summary for a specific model.
    
    Args:
        model_name (str): Name of the model (e.g., 'claude_3_5', 'claude_4_5')
        
    Returns:
        dict: Evaluation summary data
        
    Raises:
        FileNotFoundError: If the evaluation summary file doesn't exist
    """
    base_dir = Path(__file__).parent
    summary_path = base_dir / f'model_{model_name}' / 'logs' / 'evaluation_summary.json'
    
    if not summary_path.exists():
        raise FileNotFoundError(f"Evaluation summary not found: {summary_path}")
    
    with open(summary_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_metrics(summary_data):
    """
    Extract field accuracies and overall accuracy from evaluation summary.
    
    Args:
        summary_data (dict): Evaluation summary data
        
    Returns:
        dict: Dictionary with field names as keys and accuracy percentages as values
    """
    metrics = {}
    
    # Reason: Extract individual field accuracies and convert to percentages
    field_accuracy = summary_data.get('field_accuracy', {})
    for field_name, field_data in field_accuracy.items():
        accuracy = field_data.get('accuracy', 0.0)
        metrics[field_name] = accuracy * 100  # Convert to percentage
    
    # Add overall accuracy
    overall_accuracy = summary_data.get('overall_accuracy', {}).get('accuracy', 0.0)
    metrics['overall'] = overall_accuracy * 100  # Convert to percentage
    
    return metrics


def create_comparison_chart(claude_35_metrics, claude_45_metrics, output_path):
    """
    Create side-by-side bar chart comparing model performance.
    
    Args:
        claude_35_metrics (dict): Metrics for Claude 3.5 model
        claude_45_metrics (dict): Metrics for Claude 4.5 model
        output_path (Path): Path to save the chart
    """
    # Prepare data for plotting
    # Reason: Use consistent field order for clear comparison
    field_labels = [
        'Invoice No',
        'Invoice Date', 
        'Total Gross\nWorth',
        'Seller',
        'Client',
        'Overall'
    ]
    
    field_keys = [
        'invoice_no',
        'invoice_date',
        'total_gross_worth',
        'seller',
        'client',
        'overall'
    ]
    
    claude_35_values = [claude_35_metrics.get(key, 0) for key in field_keys]
    claude_45_values = [claude_45_metrics.get(key, 0) for key in field_keys]
    
    # Set up the bar chart
    # Reason: Use large figure size for readability with multiple bars
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(field_labels))  # Label locations
    bar_width = 0.35  # Width of bars
    
    # Create bars with specified colors
    bars1 = ax.bar(x - bar_width/2, claude_35_values, bar_width, 
                   label='Claude 3.5', color='#2E86AB', alpha=0.8)
    bars2 = ax.bar(x + bar_width/2, claude_45_values, bar_width,
                   label='Claude 4.5', color='#06A77D', alpha=0.8)
    
    # Customize the chart
    ax.set_xlabel('Fields', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Model Performance Comparison: Claude 3.5 vs Claude 4.5', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(field_labels, fontsize=11)
    ax.set_ylim(0, 105)  # Slightly above 100 to fit labels
    ax.legend(fontsize=11, loc='lower left')
    
    # Reason: Add horizontal grid lines for easier reading of accuracy values
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add value labels on top of bars
    # Reason: Display exact percentage values for precise comparison
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Model Comparison Chart saved to: {output_path}")
    
    # Optionally display the chart
    # plt.show()


def main():
    """
    Main function to generate model comparison visualization.
    """
    print("📊 Generating Model Performance Comparison Chart")
    print("=" * 60)
    
    try:
        # Load evaluation summaries for both models
        print("\n📂 Loading evaluation summaries...")
        claude_35_summary = load_evaluation_summary('claude_3_5')
        claude_45_summary = load_evaluation_summary('claude_4_5')
        print("✅ Summaries loaded successfully")
        
        # Extract metrics
        print("\n📈 Extracting metrics...")
        claude_35_metrics = extract_metrics(claude_35_summary)
        claude_45_metrics = extract_metrics(claude_45_summary)
        
        # Print summary statistics
        print("\n📋 Performance Summary:")
        print(f"  Claude 3.5 Overall Accuracy: {claude_35_metrics['overall']:.2f}%")
        print(f"  Claude 4.5 Overall Accuracy: {claude_45_metrics['overall']:.2f}%")
        improvement = claude_45_metrics['overall'] - claude_35_metrics['overall']
        print(f"  Improvement: {improvement:+.2f}%")
        
        # Create comparison chart
        print("\n🎨 Creating comparison chart...")
        output_path = Path(__file__).parent / 'model_comparison.png'
        create_comparison_chart(claude_35_metrics, claude_45_metrics, output_path)
        
        print("\n" + "=" * 60)
        print("✅ Comparison chart generated successfully!")
        
    except FileNotFoundError as error:
        print(f"\n❌ Error: {error}")
        print("Please ensure both models have been evaluated first.")
        print("Run: python evaluate_extraction.py --model claude_3_5")
        print("     python evaluate_extraction.py --model claude_4_5")
        
    except Exception as error:
        print(f"\n❌ Unexpected error: {error}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

