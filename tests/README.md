# Tests

This directory is reserved for unit tests and integration tests.

## 🧪 Testing Framework

We recommend using `pytest` for testing:

```bash
pip install pytest pytest-cov
```

## 📁 Test Structure

```
tests/
├── test_dataset.py          # Tests for dataset utilities
├── test_bedrock_client.py   # Tests for Bedrock client
├── test_extraction.py       # Tests for extraction logic
└── test_evaluation.py       # Tests for evaluation metrics
```

## 🚀 Running Tests

Run all tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_dataset.py
```

Run specific test:
```bash
pytest tests/test_dataset.py::test_load_invoice
```

## ✅ Writing Tests

Example test structure:

```python
import pytest
from pathlib import Path
from PIL import Image
import json


def test_load_invoice_image():
    """Test loading an invoice image."""
    image_path = Path('data/test/invoice/invoice_0000.png')
    assert image_path.exists(), "Test image not found"
    
    image = Image.open(image_path)
    assert image.size == (2481, 3508), "Unexpected image size"
    assert image.mode == 'RGB', "Image should be RGB"


def test_load_invoice_label():
    """Test loading an invoice label."""
    label_path = Path('data/test/label/invoice_0000.json')
    assert label_path.exists(), "Test label not found"
    
    with open(label_path, 'r') as f:
        label = json.load(f)
    
    assert 'gt_parse' in label, "Missing gt_parse key"
    assert 'header' in label['gt_parse'], "Missing header"
    assert 'items' in label['gt_parse'], "Missing items"
    assert 'summary' in label['gt_parse'], "Missing summary"


def test_invoice_header_fields():
    """Test that invoice header has required fields."""
    label_path = Path('data/test/label/invoice_0000.json')
    
    with open(label_path, 'r') as f:
        label = json.load(f)
    
    header = label['gt_parse']['header']
    required_fields = ['invoice_no', 'invoice_date', 'seller', 'client']
    
    for field in required_fields:
        assert field in header, f"Missing required field: {field}"
        assert header[field], f"Field {field} is empty"
```

## 🎯 Test Coverage Goals

- **Dataset utilities**: 80%+ coverage
- **Bedrock client**: 70%+ coverage (excluding AWS API calls)
- **Extraction logic**: 80%+ coverage
- **Evaluation metrics**: 90%+ coverage

## 🔧 Mocking AWS Services

For testing Bedrock integration without making actual API calls:

```python
import pytest
from unittest.mock import Mock, patch


@patch('boto3.client')
def test_bedrock_client_initialization(mock_boto_client):
    """Test Bedrock client initialization."""
    from src.bedrock.bedrock_vision_client import BedrockVisionClient
    
    mock_boto_client.return_value = Mock()
    
    client = BedrockVisionClient(
        model_id='test-model',
        region_name='us-east-1'
    )
    
    assert client.model_id == 'test-model'
    assert client.region_name == 'us-east-1'
    mock_boto_client.assert_called_once()
```

## 📊 Continuous Integration

Tests are automatically run via GitHub Actions on:
- Push to main/develop branches
- Pull requests

See `.github/workflows/ci.yml` for CI configuration.

## 🤝 Contributing Tests

When contributing code, please:
1. Write tests for new features
2. Ensure existing tests pass
3. Maintain or improve code coverage
4. Follow the existing test structure

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.

## 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Note**: Tests are a work in progress. Contributions welcome! 🎉

