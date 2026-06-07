"""Biodiversity hotspot detection using DBSCAN clustering."""

import pandas as pd
from sklearn.cluster import DBSCAN

import folium
from folium.plugins import FastMarkerCluster

from src.mapping import ANTARCTIC_CENTER, DEFAULT_ZOOM


def detect_hotspots(
    df: pd.DataFrame,
    eps: float = 0.8,
    min_samples: int = 12,
) -> pd.DataFrame:
    """
    Apply DBSCAN on geographic coordinates (degrees).

    eps ≈ 0.8° (~50–90 km depending on latitude) groups regional occurrence
    clusters. Returns DataFrame with cluster labels (-1 = noise).
    """
    coords = df[["decimalLatitude", "decimalLongitude"]].values
    labels = DBSCAN(
        eps=eps, min_samples=min_samples, metric="euclidean", n_jobs=-1
    ).fit_predict(coords)

    result = df.copy()
    result["cluster"] = labels
    return result


def summarize_hotspots(clustered_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize each cluster: size, centroid, and species richness."""
    clusters = clustered_df[clustered_df["cluster"] >= 0].copy()
    if clusters.empty:
        return pd.DataFrame(columns=["cluster", "n_records", "centroid_lat", "centroid_lon", "n_species"])

    summary = (
        clusters.groupby("cluster")
        .agg(
            n_records=("scientificName", "size"),
            centroid_lat=("decimalLatitude", "mean"),
            centroid_lon=("decimalLongitude", "mean"),
            n_species=("scientificName", "nunique"),
        )
        .reset_index()
        .sort_values("n_species", ascending=False)
    )
    return summary


def create_hotspot_map(
    clustered_df: pd.DataFrame,
    hotspot_summary: pd.DataFrame,
    sample_size: int = 2000,
    max_clusters: int = 8,
) -> folium.Map:
    """Visualize DBSCAN clusters and hotspot centroids on a map."""
    m = folium.Map(location=ANTARCTIC_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")

    if hotspot_summary.empty:
        return m

    top_clusters = hotspot_summary.head(max_clusters)["cluster"].tolist()
    plot_df = clustered_df[
        (clustered_df["cluster"] >= 0) & (clustered_df["cluster"].isin(top_clusters))
    ]
    if len(plot_df) > sample_size:
        plot_df = plot_df.sample(sample_size, random_state=42)

    for cluster_id, group in plot_df.groupby("cluster"):
        coords = group[["decimalLatitude", "decimalLongitude"]].values.tolist()
        fg = folium.FeatureGroup(name=f"Cluster {int(cluster_id)}", show=True)
        FastMarkerCluster(coords).add_to(fg)
        fg.add_to(m)

    for _, row in hotspot_summary.head(10).iterrows():
        folium.Marker(
            location=[row["centroid_lat"], row["centroid_lon"]],
            popup=(
                f"<b>Hotspot Cluster {int(row['cluster'])}</b><br>"
                f"Records: {int(row['n_records'])}<br>"
                f"Species: {int(row['n_species'])}"
            ),
            icon=folium.Icon(color="red", icon="star"),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m
