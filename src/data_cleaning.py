"""Data cleaning utilities for Antarctic occurrence records."""

import pandas as pd


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load occurrence CSV into a DataFrame."""
    return pd.read_csv(filepath, low_memory=False)


def clean_occurrence_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Antarctic biodiversity occurrence records.

    Steps:
    - Remove duplicate records
    - Drop rows with missing coordinates
    - Convert eventDate to datetime and extract year
    """
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates()

    cleaned = cleaned.dropna(subset=["decimalLatitude", "decimalLongitude"])

    cleaned["decimalLatitude"] = pd.to_numeric(cleaned["decimalLatitude"], errors="coerce")
    cleaned["decimalLongitude"] = pd.to_numeric(cleaned["decimalLongitude"], errors="coerce")
    cleaned = cleaned.dropna(subset=["decimalLatitude", "decimalLongitude"])

    cleaned["eventDate"] = pd.to_datetime(cleaned["eventDate"], errors="coerce", utc=True)
    cleaned["year"] = cleaned["eventDate"].dt.year

    return cleaned.reset_index(drop=True)


def get_cleaning_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> dict:
    """Return summary statistics from the cleaning pipeline."""
    return {
        "raw_records": len(raw_df),
        "clean_records": len(clean_df),
        "duplicates_removed": len(raw_df) - len(raw_df.drop_duplicates()),
        "missing_coords_removed": len(raw_df.drop_duplicates())
        - len(raw_df.drop_duplicates().dropna(subset=["decimalLatitude", "decimalLongitude"])),
        "records_with_year": int(clean_df["year"].notna().sum()),
    }
