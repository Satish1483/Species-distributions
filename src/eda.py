"""Exploratory data analysis for Antarctic species occurrences."""

import pandas as pd


def total_records(df: pd.DataFrame) -> int:
    return len(df)


def total_unique_species(df: pd.DataFrame) -> int:
    return df["scientificName"].nunique()


def top_species(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df["scientificName"].value_counts().head(n)


def observations_by_year(df: pd.DataFrame) -> pd.Series:
    yearly = df.dropna(subset=["year"]).copy()
    yearly["year"] = yearly["year"].astype(int)
    return yearly.groupby("year").size().sort_index()


def taxonomic_summary(df: pd.DataFrame) -> dict:
    return {
        "kingdoms": df["kingdom"].nunique(),
        "phyla": df["phylum"].nunique(),
        "classes": df["class"].nunique(),
        "orders": df["order"].nunique(),
        "families": df["family"].nunique(),
        "genera": df["genus"].nunique(),
    }


def eda_summary(df: pd.DataFrame) -> dict:
    """Compile all EDA metrics into a single dictionary."""
    return {
        "total_records": total_records(df),
        "total_unique_species": total_unique_species(df),
        "top_10_species": top_species(df, 10).to_dict(),
        "observations_by_year": observations_by_year(df).to_dict(),
        "taxonomic_summary": taxonomic_summary(df),
    }
