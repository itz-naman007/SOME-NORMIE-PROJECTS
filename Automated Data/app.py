import streamlit as st
import pandas as pd

from data_auditor import check_missing, count_duplicates, check_outliers, check_types
from data_cleaner import clean_data

st.set_page_config(page_title="Data Quality Auditor", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stMetric { background-color: #1e2530; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
    h1, h2, h3 { color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

st.title("Automated Data Quality Auditor")
st.markdown("Upload your dataset (CSV or Excel) to get an automated quality report, detecting missing values, duplicates, outliers, and schema inconsistencies.")

file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx'])

if file:
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.success("File uploaded successfully.")
        
        with st.expander("Preview Raw Data", expanded=False):
            st.dataframe(df.head())
            
        st.header("Data Quality Report")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Missing Values", df.isna().sum().sum())
        c4.metric("Duplicates", count_duplicates(df))

        st.divider()

        st.subheader("1. Missing Values")
        missing_df = check_missing(df)
        if not missing_df.empty:
            st.dataframe(missing_df, use_container_width=True)
            st.info("Recommendation: Impute missing values or drop excessive missing data.")
        else:
            st.success("No missing values found.")

        st.subheader("2. Duplicate Rows")
        duplicates = count_duplicates(df)
        if duplicates > 0:
            st.warning(f"Found {duplicates} duplicate rows ({(duplicates/len(df)*100).round(2)}%).")
            st.info("Recommendation: Review and remove duplicates if they aren't unique observations.")
        else:
            st.success("No duplicate rows found.")

        st.subheader("3. Outlier Detection (IQR)")
        outliers_df = check_outliers(df)
        if df.select_dtypes(include=['number']).empty:
            st.info("No numerical columns found for outlier detection.")
        elif not outliers_df.empty:
            st.dataframe(outliers_df, use_container_width=True)
            st.info("Recommendation: Investigate anomalies and consider capping or removing them.")
        else:
            st.success("No significant outliers detected.")

        st.subheader("4. Schema Inconsistencies")
        inconsistent_cols = check_types(df)
        if inconsistent_cols:
            st.warning(f"Mixed data types found in: {', '.join(inconsistent_cols)}")
            st.info("Recommendation: Standardize data types in these columns.")
        else:
            st.success("Data types are consistent.")

        st.divider()
        st.subheader("Quick Fixes")
        if st.button("Generate Cleaned Dataset"):
            with st.spinner("Applying fixes..."):
                cleaned_df = clean_data(df)
                st.success("Cleaning applied: Removed duplicates and imputed missing values.")
                st.download_button("Download CSV", cleaned_df.to_csv(index=False).encode('utf-8'), 'cleaned_data.csv', 'text/csv')

    except Exception as e:
        st.error(f"Error processing file: {e}")
