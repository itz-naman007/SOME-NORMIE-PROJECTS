# Automated Data Quality Auditor

Automated Data Quality Auditor is a Streamlit-based project for quickly checking and improving dataset quality.  
It helps identify common data issues such as missing values, duplicate rows, outliers, and inconsistent data types, then offers a one-click cleaning option.

## Features

- Upload CSV or Excel datasets
- Get a quick data overview (rows, columns, missing values, duplicates)
- Detect missing values with count and percentage
- Detect duplicate rows
- Detect outliers in numeric columns using the IQR method
- Detect schema inconsistencies (mixed data types in columns)
- Generate and download a cleaned CSV file

## Project Structure

```text
Automated Data/
├── app.py              # Streamlit app UI and workflow
├── data_auditor.py     # Data quality checks
├── data_cleaner.py     # Duplicate removal and missing value imputation
├── requirements.txt    # Python dependencies
└── readme.md           # Project documentation
```

## Requirements

- Python 3.9 or newer
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

From the `Automated Data` directory, run:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## How It Works

1. Upload a CSV or Excel file.
2. Review the generated data quality report.
3. Inspect recommendations for each issue type.
4. Click **Generate Cleaned Dataset** to apply quick fixes.
5. Download the cleaned dataset as CSV.

## Data Cleaning Logic

- Removes duplicate rows
- Fills missing numeric values with the column median (or `0` if median is not available)
- Fills missing non-numeric values with the mode (or `"Unknown"` if mode is not available)

## Notes

- Outlier detection uses the Interquartile Range (IQR) rule.
- The cleaning step is intended for quick preprocessing and may need customization for production use.
