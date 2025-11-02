# Examples

This directory contains examples and demos for the Document Extraction Learning Group project.

## 📊 Interactive Extraction Viewer

An interactive web-based tool to visualize and compare invoice extraction results.

### Features

- **Side-by-side comparison**: View original invoice images alongside extracted data
- **Ground truth comparison**: Compare extracted fields with ground truth labels
- **Accuracy metrics**: See field-level accuracy for each invoice
- **Navigation**: Browse through all processed invoices
- **Responsive design**: Works on desktop and mobile browsers

### Usage

1. **Run the extraction** (if you haven't already):
   ```bash
   cd src/bedrock
   python run_extraction.py
   ```

2. **Open the viewer**:
   - Open `examples/index.html` in your web browser
   - Or use a local server:
     ```bash
     cd examples
     python -m http.server 8000
     # Open http://localhost:8000 in your browser
     ```

3. **Load extraction results**:
   - The viewer will automatically load results from `src/bedrock/output/`
   - Use the navigation buttons to browse through invoices
   - Click on fields to see detailed comparison

### Files

- `index.html` - Main HTML structure
- `viewer.js` - JavaScript logic for loading and displaying results
- `styles.css` - Styling for the viewer interface
- `ANALYSIS_VIEWER.md` - Additional documentation

## 🔮 Future Examples

We plan to add more examples:

- [ ] Jupyter notebook tutorials
- [ ] Fine-tuning scripts for open-source models
- [ ] Data augmentation examples
- [ ] Custom model integration examples
- [ ] Batch processing scripts
- [ ] API integration examples

## 🤝 Contributing Examples

Have a useful example or tutorial? We'd love to include it! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Example Submission Guidelines

1. **Clear documentation**: Include a README explaining what the example does
2. **Working code**: Ensure the example runs without errors
3. **Dependencies**: List any additional dependencies required
4. **Comments**: Add inline comments explaining key concepts
5. **Sample output**: Include expected output or screenshots

## 📝 Example Ideas

Looking for inspiration? Here are some example ideas:

- **Basic Usage**: Simple scripts showing common use cases
- **Model Comparison**: Compare different extraction models
- **Custom Fields**: Extract additional fields from invoices
- **Data Visualization**: Create charts and graphs from extraction results
- **Error Analysis**: Analyze and visualize extraction errors
- **Performance Optimization**: Techniques for faster processing

---

**Need help?** Open an [issue](../../issues) or start a [discussion](../../discussions)!

