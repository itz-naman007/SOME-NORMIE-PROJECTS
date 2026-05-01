import pandas as pd
import numpy as np

def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        return pd.DataFrame()
    return pd.DataFrame({
        'Column': missing.index,
        'Count': missing.values,
        'Percentage': (missing.values / len(df) * 100).round(2)
    })

def count_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())

def check_outliers(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = df.select_dtypes(include=[np.number]).columns
    if num_cols.empty:
        return pd.DataFrame()
        
    summary = []
    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        
        if not outliers.empty:
            summary.append({
                'Column': col,
                'Count': len(outliers),
                'Percentage': round(len(outliers) / len(df) * 100, 2)
            })
    return pd.DataFrame(summary)

def check_types(df: pd.DataFrame) -> list:
    return [col for col in df.columns if df[col].dropna().apply(type).nunique() > 1]
