import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.drop_duplicates()
    for col in cleaned.columns:
        if cleaned[col].dtype in [np.float64, np.int64]:
            val = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(val if pd.notna(val) else 0)
        else:
            mode = cleaned[col].mode()
            cleaned[col] = cleaned[col].fillna(mode[0] if not mode.empty else "Unknown")
    return cleaned
