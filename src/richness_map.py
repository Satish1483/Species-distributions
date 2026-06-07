"""Folium-based species richness heatmap."""

import branca.colormap as cm
import folium

from src.mapping import ANTARCTIC_CENTER, DEFAULT_ZOOM
from src.richness import calculate_species_richness, richness_to_geojson_features


def create_richness_map(
    df,
    lat_step: float = 1.0,
    lon_step: float = 2.0,
    richness_df=None,
) -> folium.Map:
    """Generate an interactive species richness heatmap on a Folium map."""
    richness = richness_df if richness_df is not None else calculate_species_richness(
        df, lat_step=lat_step, lon_step=lon_step
    )
    m = folium.Map(location=ANTARCTIC_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")

    if richness.empty:
        return m

    min_count = int(richness["species_count"].min())
    max_count = int(richness["species_count"].max())
    colormap = cm.LinearColormap(
        colors=["#FFFFCC", "#FED976", "#FD8D3C", "#E31A1C", "#800026"],
        vmin=min_count,
        vmax=max_count,
        caption="Species Richness (unique species per grid cell)",
    )
    colormap.add_to(m)

    geojson = {
        "type": "FeatureCollection",
        "features": richness_to_geojson_features(richness, lat_step, lon_step),
    }

    def style_fn(feature):
        count = feature["properties"]["species_count"]
        color = colormap(count)
        return {"fillColor": color, "color": color, "weight": 0.5, "fillOpacity": 0.65}

    folium.GeoJson(
        geojson,
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(fields=["species_count"], aliases=["Species:"]),
    ).add_to(m)

    return m
