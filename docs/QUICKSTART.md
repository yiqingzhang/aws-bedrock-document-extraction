# Quick Start Guide

Get started with invoice extraction in 3 simple steps!

## Step 1: Install Dependencies

```bash
cd bedrock
pip install -r requirements.txt
```

## Step 2: Configure AWS

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region: `ap-southeast-2`

## Step 3: Run Extraction

```bash
python run_extraction.py
```

That's it! The system will:
- ✅ Extract data from 501 invoices
- ✅ Evaluate accuracy against ground truth
- ✅ Generate comprehensive metrics report

## What You'll Get

### Extraction Results
- `output/` - JSON files with extracted data for each invoice

### Evaluation Metrics
- `logs/evaluation_report.json` - Detailed accuracy metrics
- `logs/evaluation_summary.json` - Quick metrics summary

### Expected Results
- Processing time: ~15-30 minutes
- Cost: ~$0.50-1.00 USD
- Overall accuracy: 70-80% (all 5 fields correct)

## Troubleshooting

**Problem**: AWS credentials error  
**Solution**: Run `aws configure` and enter your credentials

**Problem**: Bedrock access denied  
**Solution**: Ensure your IAM user has `bedrock:InvokeModel` permission

**Problem**: Script interrupted  
**Solution**: Just run it again! Already-processed invoices are automatically skipped

## Need More Details?

See [README.md](README.md) for complete documentation.


