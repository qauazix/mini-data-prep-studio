# Mini Data Prep Studio

Mini Data Prep Studio is a Streamlit application for uploading, profiling, cleaning, validating, visualizing, and exporting tabular datasets.

The app is designed as a guided workflow rather than a dashboard gallery:

**upload → inspect → clean → visualize → export**

---

## Features

### 1. Upload & Overview
- Upload CSV, Excel, or JSON files
- View dataset shape
- View number of columns
- Inspect inferred data types
- Review missing values by column
- Check duplicate count
- Display summary statistics
- Reset session

### 2. Cleaning Studio
- Missing value handling
- Duplicate detection and removal
- Data type conversion
- Datetime parsing
- Categorical standardization
- Mapping / replacement
- Rare category grouping
- One-hot encoding
- Outlier detection
- Winsorization / outlier row removal
- Min-max scaling
- Z-score scaling
- Rename, drop, and create columns
- Numeric binning
- Data validation rules
- Transformation log
- Undo last step

### 3. Visualization Builder
- Histogram
- Box plot
- Scatter plot
- Line chart
- Bar chart
- Correlation heatmap
- Category and numeric filtering
- Top N category selection for bar charts

### 4. Export & Report
- Export cleaned dataset as CSV
- Export cleaned dataset as Excel
- Export transformation recipe as JSON
- Export transformation report as JSON
- Export validation violations table as CSV

---

## Supported File Types
- CSV
- Excel (.xlsx)
- JSON

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt