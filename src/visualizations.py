"""Static visualizations for species distribution analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.richness import calculate_species_richness

sns.set_theme(style="whitegrid", palette="muted")
OUTPUT_DIR = Path("outputs/figures")


def _save_fig(fig, filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_top_species(df: pd.DataFrame, n: int = 10) -> Path:
    """Bar chart of the top N most observed species."""
    counts = df["scientificName"].value_counts().head(n)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index, legend=False, ax=ax, palette="viridis")
    ax.set_xlabel("Number of Observations")
    ax.set_ylabel("Scientific Name")
    ax.set_title(f"Top {n} Most Observed Species in Antarctica")
    return _save_fig(fig, "top_species_bar_chart.png")


def plot_yearly_trend(df: pd.DataFrame) -> Path:
    """Line chart of species observations by year."""
    yearly = df.dropna(subset=["year"]).copy()
    yearly["year"] = yearly["year"].astype(int)
    counts = yearly.groupby("year").size()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(counts.index, counts.values, marker="o", linewidth=2, color="#2E86AB")
    ax.fill_between(counts.index, counts.values, alpha=0.2, color="#2E86AB")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Observations")
    ax.set_title("Species Observations by Year")
    ax.tick_params(axis="x", rotation=45)
    return _save_fig(fig, "yearly_trend_chart.png")


def plot_richness_heatmap(
    df: pd.DataFrame,
    lat_step: float = 1.0,
    lon_step: float = 2.0,
) -> Path:
    """Heatmap of species richness across geographic grid cells."""
    richness = calculate_species_richness(df, lat_step=lat_step, lon_step=lon_step)

    pivot = richness.pivot_table(
        index="lat_bin",
        columns="lon_bin",
        values="species_count",
        aggfunc="first",
    ).sort_index(ascending=False)

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        linewidths=0.1,
        linecolor="white",
        cbar_kws={"label": "Unique Species"},
        ax=ax,
    )
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Species Richness Heatmap (Grid Cells)")
    return _save_fig(fig, "richness_heatmap.png")


def plot_occurrence_scatter(df: pd.DataFrame, sample_size: int = 8000) -> Path:
    """Scatter map of occurrence points (static)."""
    plot_df = df if len(df) <= sample_size else df.sample(sample_size, random_state=42)

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.scatter(
        plot_df["decimalLongitude"],
        plot_df["decimalLatitude"],
        s=4,
        alpha=0.4,
        c="#2E86AB",
        edgecolors="none",
    )
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Antarctic Species Occurrence Map")
    ax.set_facecolor("#E8F4F8")
    ax.grid(True, alpha=0.3)
    return _save_fig(fig, "occurrence_scatter_map.png")


def generate_all_visualizations(df: pd.DataFrame) -> list[Path]:
    """Generate all static charts and return output paths."""
    return [
        plot_top_species(df),
        plot_yearly_trend(df),
        plot_richness_heatmap(df),
        plot_occurrence_scatter(df),
    ]
