"""Species richness analysis using geographic grid cells."""

import numpy as np
import pandas as pd


def assign_grid_cells(
    df: pd.DataFrame,
    lat_step: float = 1.0,
    lon_step: float = 2.0,
) -> pd.DataFrame:
    """Assign each occurrence to a lat/lon grid cell."""
    gridded = df.copy()
    gridded["lat_bin"] = (np.floor(gridded["decimalLatitude"] / lat_step) * lat_step).round(4)
    gridded["lon_bin"] = (np.floor(gridded["decimalLongitude"] / lon_step) * lon_step).round(4)
    gridded["grid_id"] = (
        gridded["lat_bin"].astype(str) + "_" + gridded["lon_bin"].astype(str)
    )
    return gridded


def calculate_species_richness(
    df: pd.DataFrame,
    lat_step: float = 1.0,
    lon_step: float = 2.0,
) -> pd.DataFrame:
    """Calculate unique species count per grid cell."""
    gridded = assign_grid_cells(df, lat_step=lat_step, lon_step=lon_step)
    richness = (
        gridded.groupby(["lat_bin", "lon_bin", "grid_id"])["scientificName"]
        .nunique()
        .reset_index(name="species_count")
    )
    richness["center_lat"] = richness["lat_bin"] + lat_step / 2
    richness["center_lon"] = richness["lon_bin"] + lon_step / 2
    return richness.sort_values("species_count", ascending=False).reset_index(drop=True)


def richness_to_geojson_features(richness_df: pd.DataFrame, lat_step: float, lon_step: float) -> list:
    """Convert richness grid to GeoJSON-like features for mapping."""
    features = []
    for _, row in richness_df.iterrows():
        lat, lon = row["lat_bin"], row["lon_bin"]
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [lon, lat],
                        [lon + lon_step, lat],
                        [lon + lon_step, lat + lat_step],
                        [lon, lat + lat_step],
                        [lon, lat],
                    ]],
                },
                "properties": {
                    "species_count": int(row["species_count"]),
                    "grid_id": row["grid_id"],
                },
            }
        )
    return features
