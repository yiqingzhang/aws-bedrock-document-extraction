# Invoice Extraction Analysis Viewer

Interactive web-based tool for analyzing and comparing invoice extraction results across different Claude models.

## Features

- 📊 **Side-by-side comparison** of ground truth vs extracted values
- 🖼️ **Invoice image display** alongside extraction results
- ✅ **Visual highlighting** of matches and mismatches
- 🔄 **Easy navigation** with dropdown, buttons, and keyboard shortcuts
- 📈 **Real-time statistics** showing accuracy metrics
- 🎨 **Color-coded fields** for quick identification of errors
- 📱 **Responsive design** works on desktop and mobile

## Quick Start

### Starting the Server

**IMPORTANT**: The HTTP server must run from the parent directory to access both `bedrock/` and `data/` folders.

```bash
# 1. Navigate to the parent directory
cd /Users/Michael.Zhang/Documents/myob/repos/ocr/document-extraction-learning-group

# 2. Start the HTTP server
python -m http.server 8001

# You should see:
# Serving HTTP on :: port 8001 (http://[::]:8001/) ...
```

**Note**: Keep this terminal window open while using the viewer.

### Opening the Viewer

Once the server is running, open your browser and navigate to:

```
http://localhost:8001/bedrock/analysis/
```

Or run this command in a new terminal:

```bash
open http://localhost:8001/bedrock/analysis/
```

### Stopping the Server

When you're done using the viewer, stop the server:

**Method 1: If server is running in foreground (terminal shows logs)**
- Press `Ctrl + C` in the terminal window

**Method 2: If server is running in background**
```bash
# Find the server process
lsof -ti:8001

# Kill the process (replace PID with the number from above)
kill <PID>

# Or kill all Python HTTP servers on port 8001
kill $(lsof -ti:8001)
```

**Quick one-liner to start fresh:**
```bash
# Stop any existing server and start new one
kill $(lsof -ti:8001) 2>/dev/null; cd /Users/Michael.Zhang/Documents/myob/repos/ocr/document-extraction-learning-group && python -m http.server 8001
```

### Troubleshooting Server Issues

**Problem**: Port already in use
```
OSError: [Errno 48] Address already in use
```

**Solution**: Kill existing process on port 8001
```bash
kill $(lsof -ti:8001)
```

**Problem**: Can't find the command `lsof`

**Solution**: Use alternative method
```bash
# List all Python processes
ps aux | grep python

# Find the PID and kill it
kill <PID>
```

## Usage

### Navigation

- **Next/Previous Buttons**: Click to move between invoices
- **Dropdown Menu**: Select any invoice directly by name
- **Keyboard Shortcuts**:
  - `←` (Left Arrow): Go to previous invoice
  - `→` (Right Arrow): Go to next invoice

### Model Comparison

1. Use the **Model Selector** dropdown in the header to switch between:
   - Claude 3.5 Sonnet
   - Claude 4.5 Sonnet

2. The viewer will reload data and show results for the selected model

### Understanding the Display

#### Stats Bar
- **Current Invoice**: Shows position (e.g., "25 / 501")
- **Overall Accuracy**: Model's overall accuracy across all invoices
- **Current Match**: Match status for the current invoice

#### Image Panel (Left)
- Displays the original invoice image
- Shows source file path

#### Data Panel (Right)
- **Field-by-field comparison** table with:
  - **Field Name**: The invoice field being extracted
  - **Ground Truth**: The correct value from labels
  - **Extracted**: The value extracted by the model
  - **Match Status**: ✅ for matches, ❌ for mismatches

#### Color Coding
- 🟢 **Green background**: Fields that match
- 🔴 **Red background**: Fields that don't match
- ⚪ **Gray text**: Empty or missing values

## File Structure

```
analysis/
├── index.html          # Main viewer interface
├── viewer.js           # JavaScript application logic
├── styles.css          # Styling and layout
└── README.md           # This file
```

## Data Requirements

The viewer expects the following directory structure:

```
bedrock/
├── analysis/           # Viewer files (this directory)
├── model_claude_3_5/
│   └── logs/
│       └── evaluation_report.json
├── model_claude_4_5/
│   └── logs/
│       └── evaluation_report.json
└── data/
    ├── test/invoice/
    ├── train/invoice/
    └── validation/invoice/
```

### Running Evaluations

If evaluation reports don't exist, run:

```bash
cd /Users/Michael.Zhang/Documents/myob/repos/ocr/document-extraction-learning-group/bedrock

# Evaluate Claude 3.5
python evaluate_extraction.py --model claude_3_5

# Evaluate Claude 4.5
python evaluate_extraction.py --model claude_4_5
```

## Troubleshooting

### Images Not Loading

**Problem**: Images show "Failed to load image" or don't appear.

**Solution**: 
1. Make sure you're using a local web server (Option 1 above)
2. Check that invoice images exist in the `data/` directory
3. Verify file paths in evaluation reports are correct

### Evaluation Data Not Loading

**Problem**: "Failed to load evaluation data" error.

**Solution**:
1. Ensure evaluations have been run for both models
2. Check that JSON files exist in:
   - `model_claude_3_5/logs/evaluation_report.json`
   - `model_claude_4_5/logs/evaluation_report.json`
3. Open browser console (F12) for detailed error messages

### CORS Errors

**Problem**: "CORS policy" errors in browser console.

**Solution**: Use Python HTTP server (Option 1) instead of opening files directly.

## Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer (not supported)

## Tips for Analysis

1. **Find Problem Cases**: 
   - Use Next/Previous to browse through invoices
   - Look for ❌ mismatch indicators
   - Compare what the model extracted vs ground truth

2. **Compare Models**:
   - Switch between Claude 3.5 and Claude 4.5
   - Keep the same invoice selected to see differences
   - Note which model performs better on specific fields

3. **Identify Patterns**:
   - Are certain fields consistently wrong?
   - Do errors occur on specific invoice layouts?
   - Is there a pattern in seller/client extraction errors?

## Advanced Usage

### Filtering by Match Status

To see only mismatches, you can modify the JavaScript:

```javascript
// In viewer.js, add after loading data:
invoiceList = invoiceList.filter(invoice => !invoice.all_correct);
```

### Exporting Results

Use browser's Print to PDF function to save analysis:
1. Navigate to an interesting invoice
2. File → Print → Save as PDF

## Support

For issues or questions:
1. Check console errors (F12 → Console)
2. Verify evaluation reports exist
3. Ensure web server is running
4. Check file paths in evaluation reports

## Version

Version 1.0 - Initial release

Built with ❤️ for invoice extraction analysis

