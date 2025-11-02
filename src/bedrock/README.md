# Bedrock Invoice Extraction System

Automated invoice data extraction using AWS Bedrock Claude Vision API with comprehensive evaluation metrics.

## Overview

This system processes invoice images using Claude Sonnet 4.5 Vision to extract key fields and evaluates extraction accuracy against ground truth labels.

### Extracted Fields

1. **invoice_no** - Invoice number
2. **invoice_date** - Invoice date
3. **total_gross_worth** - Total gross amount (with currency)
4. **seller** - Seller name and address
5. **client** - Client name and address

## Directory Structure

```
src/bedrock/
├── bedrock_vision_client.py    # AWS Bedrock client with vision support
├── extract_invoices.py         # Main extraction script
├── evaluate_extraction.py      # Evaluation and metrics calculation
├── run_extraction.py           # Main pipeline entry point
├── compare_models.py           # Compare different Claude models
├── config.json                 # Model configuration
├── requirements.txt            # Python dependencies
├── output/                     # Extraction results (JSON files, gitignored)
├── logs/                       # Logs and evaluation reports (gitignored)
└── README.md                   # This file
```

## Setup

### Prerequisites

1. **AWS Account** with Bedrock access
2. **AWS CLI** configured with credentials
3. **Python 3.8+**

### Installation

1. Install dependencies:
```bash
cd src/bedrock
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (use `ap-southeast-2`)

3. Verify Bedrock access:
```bash
python bedrock_vision_client.py
```

You should see "Connection test successful" if everything is configured correctly.

## Usage

### Quick Start (Recommended)

Run the complete pipeline (extraction + evaluation):

```bash
python run_extraction.py
```

This will:
1. Process all 501 invoices from test/train/validation splits
2. Extract the 5 key fields from each invoice
3. Save results to `output/` directory
4. Evaluate accuracy against ground truth
5. Generate comprehensive metrics report

### Advanced Usage

#### Extract Only

To run just the extraction step:

```bash
python extract_invoices.py
```

#### Evaluate Only

If you already have extraction results:

```bash
python evaluate_extraction.py
```

#### Resume Interrupted Process

The system automatically skips already-processed invoices. If extraction is interrupted, simply run the script again:

```bash
python run_extraction.py
```

## Output Files

### Extraction Results

Location: `output/`

Each invoice produces a JSON file named `{split}_{invoice_name}_extracted.json`:

```json
{
  "source_file": "path/to/invoice.png",
  "ground_truth": {
    "invoice_no": "97159829",
    "invoice_date": "09/18/2015",
    "total_gross_worth": "$ 978,12",
    "seller": "Bradley-Andrade 9879 Elizabeth Common...",
    "client": "Castro PLC Unit 9678 Box 9664..."
  },
  "extracted": {
    "invoice_no": "97159829",
    "invoice_date": "09/18/2015",
    "total_gross_worth": "$ 978,12",
    "seller": "Bradley-Andrade 9879 Elizabeth Common...",
    "client": "Castro PLC Unit 9678 Box 9664..."
  },
  "processing_time": 2.34,
  "success": true,
  "timestamp": "2025-01-15T10:30:45.123456"
}
```

### Evaluation Reports

Location: `logs/`

- **evaluation_report.json** - Detailed results with per-invoice analysis
- **evaluation_summary.json** - Metrics summary only
- **extraction_stats.json** - Processing statistics
- **failed_invoices.log** - List of failed extractions (if any)

Example metrics:

```json
{
  "total_invoices": 501,
  "successful_extractions": 498,
  "failed_extractions": 3,
  "field_accuracy": {
    "invoice_no": 0.95,
    "invoice_date": 0.92,
    "total_gross_worth": 0.88,
    "seller": 0.85,
    "client": 0.87
  },
  "overall_accuracy": 0.75
}
```

## Cost Estimation

### AWS Bedrock Pricing

Claude Sonnet 4.5 pricing (as of Jan 2025):
- Input: ~$0.003 per 1K tokens
- Output: ~$0.015 per 1K tokens

### Estimated Costs

Processing 501 invoices:
- Average image size: ~500KB
- Average tokens per image: ~2000 input + 200 output
- **Estimated total: $0.50 - $1.00 USD**

Note: Actual costs may vary based on image sizes and response lengths.

## Performance

### Processing Time

- Average time per invoice: ~2-3 seconds
- Total time for 501 invoices: ~15-30 minutes
- Includes API calls, retry logic, and file I/O

### Accuracy Expectations

Claude Sonnet 4.5 Vision typically achieves:
- **Invoice numbers**: 90-95% accuracy
- **Dates**: 85-92% accuracy
- **Amounts**: 85-90% accuracy
- **Text fields (seller/client)**: 80-85% accuracy
- **Overall (all 5 fields)**: 70-80% accuracy

## Troubleshooting

### Connection Errors

**Problem**: "AWS credentials not found"

**Solution**:
```bash
aws configure
# Enter your credentials
```

### Permission Errors

**Problem**: "Access denied to Bedrock"

**Solution**: Ensure your IAM user/role has `bedrock:InvokeModel` permission for the Claude model.

### Rate Limiting

**Problem**: "ThrottlingException"

**Solution**: The script includes automatic retry with exponential backoff. If persistent, consider:
- Adding delay between requests
- Requesting rate limit increase from AWS

### JSON Parsing Errors

**Problem**: "Failed to parse response"

**Solution**: The model occasionally returns invalid JSON. The retry logic handles this automatically (3 attempts).

### Out of Memory

**Problem**: Script crashes with memory error

**Solution**:
- Process images in smaller batches
- Reduce image resolution before processing
- Increase available system memory

## Advanced Configuration

### Modify Model Settings

Edit `bedrock_vision_client.py`:

```python
# Change temperature (0.0 = deterministic, 1.0 = creative)
temperature=0.0

# Change max tokens for longer responses
max_tokens=2000

# Change model (if using different region/model)
self.model_id = 'au.anthropic.claude-sonnet-4-5-20250929-v1:0'
```

### Customize Extraction Prompt

Edit `bedrock_vision_client.py` in the `extract_invoice_data` method to modify the extraction prompt.

### Add More Fields

1. Update the extraction prompt in `bedrock_vision_client.py`
2. Update field lists in `extract_invoices.py` and `evaluate_extraction.py`
3. Update ground truth extraction in `extract_invoices.py` `load_ground_truth` method

## Architecture

### Component Overview

1. **BedrockVisionClient** (`bedrock_vision_client.py`)
   - Handles AWS Bedrock API communication
   - Encodes images to base64
   - Implements retry logic
   - Parses JSON responses

2. **InvoiceExtractor** (`extract_invoices.py`)
   - Scans invoice files from data directory
   - Coordinates extraction process
   - Implements checkpoint/resume
   - Saves results and logs

3. **ExtractionEvaluator** (`evaluate_extraction.py`)
   - Loads extraction results
   - Compares with ground truth
   - Calculates accuracy metrics
   - Generates reports

4. **Pipeline Runner** (`run_extraction.py`)
   - Orchestrates full pipeline
   - Provides user interface
   - Handles interruptions gracefully

### Error Handling

- **Retry Logic**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Checkpoint/Resume**: Already-processed files are automatically skipped
- **Graceful Failures**: Failed extractions are logged but don't stop the process
- **Keyboard Interrupts**: Progress is saved, can resume later

## Development

### Testing Individual Components

Test the Bedrock client:
```bash
python bedrock_vision_client.py
```

Test extraction (single invoice):
```python
from bedrock_vision_client import BedrockVisionClient

client = BedrockVisionClient()
result = client.extract_invoice_data('path/to/invoice.png')
print(result)
```

### Adding Custom Metrics

Edit `evaluate_extraction.py` and add custom evaluation logic in the `evaluate_invoice` method.

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Sparrow Invoice Dataset](https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1)

## Support

For issues related to:
- **AWS/Bedrock**: Check AWS documentation or AWS Support
- **Dataset**: See `../dataset/README.md`
- **Code**: Check error logs in `logs/` directory
- **General**: Open an issue in the [main repository](../../issues)

---

**Ready to start?** Run `python run_extraction.py` and follow the prompts!

