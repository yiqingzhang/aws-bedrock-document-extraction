# Model Configuration Guide

## Overview

The invoice extraction pipeline now supports multiple Claude models with separate output directories. Configuration is managed through `config.json` and command-line arguments.

## Configuration File

The `config.json` file defines available model configurations:

```json
{
  "claude_3_5": {
    "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "region": "ap-southeast-2",
    "output_subdir": "model_claude_3_5"
  },
  "claude_4_5": {
    "model_id": "au.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "region": "ap-southeast-2",
    "output_subdir": "model_claude_4_5"
  }
}
```

### Configuration Fields

- **model_id**: The AWS Bedrock model identifier
- **region**: AWS region where the model is available
- **output_subdir**: Directory name for storing outputs (under `bedrock/`)

## Usage

### Running Extraction

Run extraction with Claude 3.5:
```bash
python run_extraction.py --model claude_3_5
```

Run extraction with Claude 4.5:
```bash
python run_extraction.py --model claude_4_5
```

### Running Evaluation

Evaluate Claude 3.5 results:
```bash
python evaluate_extraction.py --model claude_3_5
```

Evaluate Claude 4.5 results:
```bash
python evaluate_extraction.py --model claude_4_5
```

### Viewing Available Models

To see all available model configurations:
```bash
python run_extraction.py
# or
python evaluate_extraction.py
```

## Output Directory Structure

Each model configuration has its own output directory:

```
bedrock/
├── config.json
├── model_claude_3_5/
│   ├── output/        # Extraction results for Claude 3.5
│   └── logs/          # Logs and evaluation reports for Claude 3.5
└── model_claude_4_5/
    ├── output/        # Extraction results for Claude 4.5
    └── logs/          # Logs and evaluation reports for Claude 4.5
```

This structure allows you to:
- Compare results between different models
- Run extractions in parallel with different models
- Keep historical results organized by model

## Adding New Models

To add a new model configuration:

1. Edit `config.json`
2. Add a new entry with a unique name:
```json
{
  "claude_3_opus": {
    "model_id": "anthropic.claude-3-opus-20240229-v1:0",
    "region": "us-east-1",
    "output_subdir": "model_claude_3_opus"
  }
}
```
3. Use the new configuration:
```bash
python run_extraction.py --model claude_3_opus
```

## Important Notes

- **Model Availability**: Ensure the model ID is available in your AWS region
- **Credentials**: AWS credentials should be configured via environment variables or AWS CLI
- **Resume Capability**: Each model's output directory maintains its own checkpoint state
- **Cost Tracking**: Separate directories make it easier to track costs per model

## Cursor Rules Used

The implementation follows these cursor rules:
- **Comment non-obvious code**: Added `# Reason:` comments explaining configuration logic
- **Longer names for clarity**: Used descriptive variable names like `output_subdir`, `model_config`
- **Always look at available code**: Reused existing path construction patterns
- **Never assume missing context**: Asked for specific model IDs and region before implementation

