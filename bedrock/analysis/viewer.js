/**
 * Invoice Extraction Analysis Viewer
 * 
 * This script manages the interactive viewer for analyzing invoice extraction results,
 * comparing ground truth with model predictions, and navigating between invoices.
 */

// Global state
let currentModel = 'claude_4_5';
let currentInvoiceIndex = 0;
let evaluationData = null;
let invoiceList = [];

/**
 * Load evaluation report for a specific model
 * 
 * @param {string} modelName - Name of the model (e.g., 'claude_3_5', 'claude_4_5')
 * @returns {Promise<Object>} Evaluation report data
 */
async function loadEvaluationData(modelName) {
    try {
        // Reason: Server is now at document-extraction-learning-group/ root
        // So paths are relative to that: /bedrock/model_*/logs/evaluation_report.json
        const response = await fetch(`/bedrock/model_${modelName}/logs/evaluation_report.json`);
        if (!response.ok) {
            throw new Error(`Failed to load evaluation data: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading evaluation data:', error);
        alert(`Error loading data for ${modelName}. Make sure the evaluation has been run.\n\nError: ${error.message}`);
        return null;
    }
}

/**
 * Initialize the viewer when page loads
 */
async function initialize() {
    console.log('Initializing viewer...');
    
    // Load initial model data
    await switchModel(currentModel);
    
    // Set up event listeners
    setupEventListeners();
    
    console.log('Viewer initialized successfully');
}

/**
 * Set up event listeners for navigation and model selection
 */
function setupEventListeners() {
    // Model selector
    document.getElementById('modelSelect').addEventListener('change', (e) => {
        switchModel(e.target.value);
    });
    
    // Navigation buttons
    document.getElementById('prevBtn').addEventListener('click', goToPreviousInvoice);
    document.getElementById('nextBtn').addEventListener('click', goToNextInvoice);
    
    // Invoice dropdown
    document.getElementById('invoiceSelect').addEventListener('change', (e) => {
        goToInvoice(parseInt(e.target.value));
    });
    
    // Keyboard shortcuts
    // Reason: Enable arrow key navigation for better user experience
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            goToPreviousInvoice();
        } else if (e.key === 'ArrowRight') {
            goToNextInvoice();
        }
    });
}

/**
 * Switch to a different model and reload data
 * 
 * @param {string} modelName - Name of the model to switch to
 */
async function switchModel(modelName) {
    console.log(`Switching to model: ${modelName}`);
    currentModel = modelName;
    
    // Update model selector
    document.getElementById('modelSelect').value = modelName;
    
    // Load evaluation data
    const data = await loadEvaluationData(modelName);
    if (!data) return;
    
    evaluationData = data;
    invoiceList = data.detailed_results || [];
    
    console.log(`Loaded ${invoiceList.length} invoices`);
    
    // Update overall accuracy display
    const overallAccuracy = (data.metrics?.overall_accuracy?.accuracy || 0) * 100;
    document.getElementById('overallAccuracy').textContent = `${overallAccuracy.toFixed(1)}%`;
    
    // Populate invoice dropdown
    populateInvoiceDropdown();
    
    // Display first invoice
    if (invoiceList.length > 0) {
        goToInvoice(0);
    }
}

/**
 * Populate the invoice selection dropdown
 */
function populateInvoiceDropdown() {
    const dropdown = document.getElementById('invoiceSelect');
    dropdown.innerHTML = '';
    
    invoiceList.forEach((invoice, index) => {
        const option = document.createElement('option');
        option.value = index;
        
        // Extract invoice filename from source path
        const filename = invoice.source_file ? invoice.source_file.split('/').pop() : `Invoice ${index + 1}`;
        option.textContent = `${index + 1}. ${filename}`;
        
        dropdown.appendChild(option);
    });
}

/**
 * Display invoice at the specified index
 * 
 * @param {number} index - Index of the invoice to display
 */
function goToInvoice(index) {
    if (index < 0 || index >= invoiceList.length) {
        console.warn(`Invalid invoice index: ${index}`);
        return;
    }
    
    currentInvoiceIndex = index;
    displayCurrentInvoice();
    updateNavigationState();
}

/**
 * Go to the previous invoice
 */
function goToPreviousInvoice() {
    if (currentInvoiceIndex > 0) {
        goToInvoice(currentInvoiceIndex - 1);
    }
}

/**
 * Go to the next invoice
 */
function goToNextInvoice() {
    if (currentInvoiceIndex < invoiceList.length - 1) {
        goToInvoice(currentInvoiceIndex + 1);
    }
}

/**
 * Update navigation button states (enable/disable)
 */
function updateNavigationState() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dropdown = document.getElementById('invoiceSelect');
    
    // Update button states
    prevBtn.disabled = currentInvoiceIndex === 0;
    nextBtn.disabled = currentInvoiceIndex === invoiceList.length - 1;
    
    // Update dropdown selection
    dropdown.value = currentInvoiceIndex;
    
    // Update counter
    document.getElementById('invoiceCounter').textContent = 
        `${currentInvoiceIndex + 1} / ${invoiceList.length}`;
}

/**
 * Display the current invoice data and image
 */
function displayCurrentInvoice() {
    if (!invoiceList || invoiceList.length === 0) {
        console.warn('No invoices to display');
        return;
    }
    
    const invoice = invoiceList[currentInvoiceIndex];
    console.log('Displaying invoice:', invoice.source_file);
    
    // Display invoice image
    displayInvoiceImage(invoice.source_file);
    
    // Display field comparison table
    displayFieldComparison(invoice);
    
    // Update match status
    updateMatchStatus(invoice);
}

/**
 * Display the invoice image
 * 
 * @param {string} sourcePath - Path to the invoice image file
 */
function displayInvoiceImage(sourcePath) {
    const imageElement = document.getElementById('invoiceImage');
    const imageLoader = document.getElementById('imageLoader');
    const imageSource = document.getElementById('imageSource');
    
    // Show loader
    imageLoader.style.display = 'block';
    imageElement.classList.remove('loaded');
    
    // Reason: Convert absolute filesystem path to HTTP path relative to server root
    // Server is running from document-extraction-learning-group/
    // Path format: /Users/.../document-extraction-learning-group/data/test/invoice/invoice_0000.png
    // HTTP path: /data/test/invoice/invoice_0000.png (relative to server root)
    let httpPath = sourcePath;
    
    if (sourcePath.includes('/data/')) {
        // Extract everything from /data/ onwards
        const dataIndex = sourcePath.indexOf('/data/');
        httpPath = sourcePath.substring(dataIndex);
    }
    
    console.log('Loading image via HTTP:', httpPath);
    console.log('Original path:', sourcePath);
    
    // Load image
    imageElement.onload = () => {
        imageLoader.style.display = 'none';
        imageElement.classList.add('loaded');
    };
    
    imageElement.onerror = () => {
        imageLoader.textContent = `Failed to load image: ${httpPath}`;
        console.error('Failed to load image:', httpPath);
        console.error('Make sure HTTP server is running from document-extraction-learning-group/ directory');
    };
    
    imageElement.src = httpPath;
    imageSource.textContent = `Source: ${sourcePath.split('/').slice(-3).join('/')}`;
}

/**
 * Display field comparison table
 * 
 * @param {Object} invoice - Invoice data with field details
 */
function displayFieldComparison(invoice) {
    const tableBody = document.querySelector('#resultsTable tbody');
    tableBody.innerHTML = '';
    
    const fieldDetails = invoice.field_details || {};
    const fields = ['invoice_no', 'invoice_date', 'total_gross_worth', 'seller', 'client'];
    
    // Reason: Display fields in a user-friendly order
    const fieldLabels = {
        'invoice_no': 'Invoice Number',
        'invoice_date': 'Invoice Date',
        'total_gross_worth': 'Total Gross Worth',
        'seller': 'Seller',
        'client': 'Client'
    };
    
    fields.forEach(field => {
        const details = fieldDetails[field] || {};
        const row = document.createElement('tr');
        
        // Field name
        const fieldCell = document.createElement('td');
        fieldCell.textContent = fieldLabels[field] || field;
        row.appendChild(fieldCell);
        
        // Ground truth
        const gtCell = document.createElement('td');
        const gtValue = createFieldValueElement(details.ground_truth, details.match);
        gtCell.appendChild(gtValue);
        row.appendChild(gtCell);
        
        // Extracted value
        const extractedCell = document.createElement('td');
        const extractedValue = createFieldValueElement(details.extracted, details.match);
        extractedCell.appendChild(extractedValue);
        row.appendChild(extractedCell);
        
        // Match status
        const matchCell = document.createElement('td');
        const matchStatus = document.createElement('span');
        matchStatus.className = `match-status ${details.match ? 'match' : 'mismatch'}`;
        matchStatus.textContent = details.match ? '✅ Match' : '❌ Mismatch';
        matchCell.appendChild(matchStatus);
        row.appendChild(matchCell);
        
        tableBody.appendChild(row);
    });
}

/**
 * Create a formatted field value element with highlighting
 * 
 * @param {string} value - The field value
 * @param {boolean} isMatch - Whether this field matches
 * @returns {HTMLElement} Formatted value element
 */
function createFieldValueElement(value, isMatch) {
    const element = document.createElement('div');
    element.className = `field-value ${isMatch ? 'match-bg' : 'mismatch-bg'}`;
    
    if (!value || value === '') {
        element.textContent = '(empty)';
        element.classList.add('empty');
    } else {
        element.textContent = value;
    }
    
    return element;
}

/**
 * Update the current invoice match status display
 * 
 * @param {Object} invoice - Invoice data
 */
function updateMatchStatus(invoice) {
    const matchElement = document.getElementById('currentMatch');
    const allCorrect = invoice.all_correct;
    
    if (allCorrect) {
        matchElement.textContent = '✅ All Fields Match';
        matchElement.style.color = '#28a745';
    } else {
        // Count mismatches
        const fieldDetails = invoice.field_details || {};
        const mismatches = Object.values(fieldDetails).filter(f => !f.match).length;
        matchElement.textContent = `❌ ${mismatches} Mismatch${mismatches !== 1 ? 'es' : ''}`;
        matchElement.style.color = '#dc3545';
    }
}

// Initialize the viewer when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

