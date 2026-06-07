"""Interactive Folium maps for species occurrence visualization."""

from pathlib import Path

import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
import pandas as pd


ANTARCTIC_CENTER = [-75.0, 0.0]
DEFAULT_ZOOM = 3


def create_occurrence_map(
    df: pd.DataFrame,
    sample_size: int | None = 3000,
    use_cluster: bool = True,
    with_popups: bool = False,
) -> folium.Map:
    """Plot occurrence points on an interactive Folium map."""
    m = folium.Map(location=ANTARCTIC_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")

    if sample_size is not None and len(df) > sample_size:
        plot_df = df.sample(sample_size, random_state=42)
    else:
        plot_df = df

    coords = plot_df[["decimalLatitude", "decimalLongitude"]].values.tolist()

    if with_popups and len(plot_df) <= 800:
        target = MarkerCluster(name="Occurrences").add_to(m) if use_cluster else m
        names = plot_df["scientificName"].astype(str)
        kingdoms = plot_df["kingdom"].fillna("N/A").astype(str)
        families = plot_df["family"].fillna("N/A").astype(str)
        years = plot_df["year"].apply(lambda y: int(y) if pd.notna(y) else "N/A")
        for (lat, lon), name, kingdom, family, year in zip(
            coords, names, kingdoms, families, years, strict=True
        ):
            popup = f"<b>{name}</b><br>Kingdom: {kingdom}<br>Family: {family}<br>Year: {year}"
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                color="#2E86AB",
                fill=True,
                fill_color="#2E86AB",
                fill_opacity=0.6,
                popup=folium.Popup(popup, max_width=250),
            ).add_to(target)
    else:
        layer = FastMarkerCluster(coords, name="Occurrences") if use_cluster else None
        if layer:
            layer.add_to(m)
        else:
            folium.GeoJson(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {"type": "Point", "coordinates": [lon, lat]},
                            "properties": {},
                        }
                        for lat, lon in coords
                    ],
                },
                marker={"radius": 3, "color": "#2E86AB", "fillOpacity": 0.6},
            ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


def save_map(m: folium.Map, filepath: str | Path) -> Path:
    """Save a Folium map to HTML."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(path))
    return path
