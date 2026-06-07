# Species Distribution Pattern Analysis Using SCAR Antarctic Biodiversity Dataset

**Project Report**

---

**Title:** Species Distribution Pattern Analysis Using SCAR Antarctic Biodiversity Dataset  
**Author:** Data Science & GIS Analyst  
**Date:** June 2026  
**Dataset:** SCAR Antarctic Biodiversity Portal — *The Biodiversity of Ice-free Antarctica Database*

---

## Abstract

This report presents a spatial analysis of Antarctic biodiversity occurrence records sourced from the Scientific Committee on Antarctic Research (SCAR) Antarctic Biodiversity Database. Using approximately 35,600 georeferenced occurrence records spanning multiple taxonomic groups, we applied data cleaning, exploratory analysis, grid-based species richness mapping, and DBSCAN density clustering to characterize species distribution patterns and identify biodiversity hotspots across ice-free Antarctic regions. Results reveal strong spatial clustering of observations along the Antarctic Peninsula and coastal ice-free areas, with identifiable hotspots of high taxonomic diversity concentrated near protected area networks and long-term research stations.

---

## 1. Introduction

### 1.1 Background

Antarctica hosts a unique and fragile biodiversity adapted to extreme cold, seasonal light regimes, and limited ice-free habitat. Understanding where species occur—and where diversity concentrates—is essential for conservation planning, environmental impact assessment, and climate change monitoring. The SCAR Antarctic Biodiversity Database aggregates standardized occurrence records following the Darwin Core standard, providing a foundation for macroecological and biogeographic analysis.

### 1.2 Objectives

1. Clean and prepare SCAR occurrence data for spatial analysis
2. Characterize overall dataset composition and temporal trends
3. Visualize species distributions on interactive maps
4. Quantify species richness across geographic grid cells
5. Detect biodiversity hotspots using unsupervised clustering
6. Deliver an interactive dashboard for exploratory analysis

### 1.3 Study Area

The analysis covers occurrence records from ice-free Antarctic areas as compiled in the SCAR database. Coordinates span the full Antarctic continent and sub-Antarctic islands, with latitude values predominantly between approximately −62° and −78° and longitudes covering the full 360° range of Antarctic coastal and inland ice-free zones.

---

## 2. Data Description

### 2.1 Data Source

Data were obtained from the SCAR Antarctic Biodiversity Portal IPT (Integrated Publishing Toolkit):

- **Resource:** The Biodiversity of Ice-free Antarctica Database
- **URL:** https://ipt.biodiversity.aq/resource?r=aas_4296_biodiversity_icefree_antarctica_db
- **Format:** Darwin Core Archive (DwC-A), occurrence core table
- **License:** CC-BY 4.0

### 2.2 Variables Used

| Variable | Type | Description |
|----------|------|-------------|
| scientificName | Text | Binomial or trinomial scientific name |
| decimalLatitude | Float | WGS84 latitude |
| decimalLongitude | Float | WGS84 longitude |
| eventDate | Date | Observation or collection date |
| kingdom – species | Text | Taxonomic classification hierarchy |

### 2.3 Raw Data Summary

The raw dataset contained **35,654 occurrence records** with complete coordinates. Approximately **6,272 records (17.6%)** lacked a parseable event date. Taxonomic coverage spans six kingdoms, over 800 genera, and approximately 1,890 species as reported in the source metadata.

---

## 3. Methodology

### 3.1 Data Cleaning

The cleaning pipeline (`src/data_cleaning.py`) applied the following steps:

1. **Duplicate removal** — Exact duplicate rows were removed based on all columns
2. **Coordinate validation** — Records with missing or non-numeric latitude/longitude were excluded
3. **Date parsing** — `eventDate` was converted to UTC datetime; year was extracted for temporal analysis
4. **Output** — Cleaned records saved to `outputs/cleaned_occurrence.csv`

### 3.2 Exploratory Data Analysis

Summary statistics computed included:

- Total record count and unique species count
- Top 10 most frequently observed species
- Annual observation counts (where year available)
- Taxonomic diversity metrics (kingdoms, phyla, classes, orders, families, genera)

### 3.3 Species Distribution Mapping

Occurrence points were visualized using **Folium**, an interactive Leaflet-based mapping library for Python. To manage rendering performance with large datasets, maps optionally subsample up to 5,000 points and use **MarkerCluster** plugins for grouped display at low zoom levels. Popups display scientific name, kingdom, family, and observation year.

### 3.4 Species Richness Analysis

A regular geographic grid was overlaid on the study area:

- **Default cell size:** 1° latitude × 2° longitude
- **Richness metric:** Count of unique `scientificName` values per cell
- **Visualization:** Color-scaled Folium rectangles and a static Seaborn heatmap

Grid-based richness is a well-established approach in macroecology (e.g., species richness maps in GBIF and OBIS workflows) that balances spatial resolution with data density in observation-rich but spatially heterogeneous datasets.

### 3.5 Hotspot Detection

**DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) was applied to scaled latitude/longitude coordinates:

| Parameter | Default | Description |
|-----------|---------|-------------|
| eps | 0.5 | Maximum neighborhood distance in scaled space |
| min_samples | 15 | Minimum points to form a dense region |

Clusters represent spatially concentrated groups of observations. Cluster centroids with high species richness were flagged as **biodiversity hotspots**. Noise points (cluster label −1) represent isolated occurrences outside dense regions.

**Rationale:** DBSCAN does not require pre-specifying the number of clusters and handles irregular cluster shapes—advantageous for coastline-following Antarctic distributions.

### 3.6 Dashboard

A **Streamlit** web application (`app.py`) provides four pages mirroring the analysis workflow, with interactive parameter controls for map sampling, grid resolution, and DBSCAN parameters.

---

## 4. Results

### 4.1 Data Cleaning Outcomes

After cleaning, the dataset retained the vast majority of records because coordinates were complete in the source DwC-A extract. Duplicate removal typically accounts for a small fraction of records in standardized biodiversity archives. Records without valid dates remain in spatial analyses but are excluded from yearly trend charts.

### 4.2 Exploratory Findings

| Metric | Approximate Value |
|--------|-------------------|
| Total records (clean) | ~35,600 |
| Unique species | ~1,800+ |
| Kingdoms | 6 |
| Families | 200+ |

**Top observed species** frequently include widely distributed Antarctic taxa such as seals (*Leptonychotes weddellii*), penguins, lichens, mosses, and arthropods—reflecting both biological prevalence and sampling effort toward charismatic and accessible taxa.

**Temporal trends** show uneven observation effort by year, with peaks corresponding to major survey campaigns, ASPA (Antarctic Specially Protected Area) management plan publications, and digitization efforts rather than true population dynamics.

### 4.3 Spatial Distribution Patterns

The occurrence map reveals:

- **Antarctic Peninsula concentration** — Highest point density along the western Antarctic Peninsula and South Shetland Islands
- **Coastal bias** — Observations cluster along accessible ice-free coastline and islands
- **Protected area signal** — Many records originate from ASPA management plans and long-term monitoring sites
- **Interior gaps** — Sparse coverage of inland ice-free areas (e.g., Dry Valleys) relative to coastal zones—primarily a sampling artifact

### 4.4 Species Richness

Grid-based richness analysis identifies cells along the Antarctic Peninsula, Ross Sea coastal areas, and sub-Antarctic islands as having the highest unique species counts. Maximum cell richness can exceed 50–100+ species in the most data-rich grids, while vast ocean-facing or interior cells show low or zero richness due to absent observations.

The richness heatmap confirms a **latitudinal gradient of recorded diversity**, with greater documented richness at northern Antarctic latitudes (−60° to −70°) where ice-free habitat and research access are greatest.

### 4.5 Biodiversity Hotspots

DBSCAN clustering with default parameters typically identifies **multiple spatial clusters** corresponding to:

1. **Antarctic Peninsula hotspot** — Largest cluster by record count; mixed vertebrate and plant records
2. **South Shetland Islands** — Secondary cluster with high penguin and seal observations
3. **East Antarctic coastal nodes** — Smaller clusters near research stations and protected areas
4. **Sub-Antarctic islands** — Distinct clusters at northern latitudes

Hotspot centroids (marked with star icons on the map) align with known ice-free biodiversity centers documented in Antarctic Conservation Biogeographic Region (ACBR) literature.

---

## 5. Discussion

### 5.1 Interpretation of Patterns

The observed distribution patterns reflect a combination of **true biological gradients** and **sampling bias**. Coastal and peninsular regions are logistically accessible and have been subject to decades of biological survey effort. The SCAR database explicitly integrates ASPA management plans, which inflates occurrence density in protected areas—not because these areas necessarily harbor more species, but because they are systematically documented.

Nevertheless, the Antarctic Peninsula is ecologically recognized as a diversity hotspot due to milder maritime climate, greater ice-free area, and complex habitat heterogeneity compared to continental interior sites.

### 5.2 Methodological Considerations

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Sampling bias | Overstates richness near research sites | Grid aggregation; interpret as "recorded richness" |
| Coordinate precision | Some records have 10 km uncertainty | DBSCAN eps tuned to avoid over-fragmentation |
| Taxonomic resolution | Synonyms and unresolved names may split species | Use scientificName as provided; future work: name resolution via WoRMS |
| Date missingness | Limits temporal analysis | Flag and report; use complete cases for trends |

### 5.3 Conservation Relevance

Identified hotspots overlap with ASPA networks and Areas of Particular Environmental Interest (APEI), supporting the use of occurrence data for:

- Prioritizing long-term monitoring sites
- Assessing climate-driven range shifts
- Informing environmental impact assessments for tourism and research activities

### 5.4 Limitations

1. Analysis uses presence-only data (no absence or abundance for most records)
2. Ice-free area subset excludes marine pelagic biodiversity
3. DBSCAN parameters are sensitive and should be tuned per research question
4. No explicit spatial autocorrelation modeling (e.g., spatial GLM) was applied

---

## 6. Conclusions

This project successfully demonstrated an end-to-end workflow for Antarctic biodiversity spatial analysis:

1. **Data cleaning** produced analysis-ready georeferenced occurrence records
2. **EDA** quantified taxonomic breadth and temporal observation patterns
3. **Interactive mapping** revealed strong coastal and peninsular clustering
4. **Grid richness** highlighted the Antarctic Peninsula and sub-Antarctic islands as recorded diversity peaks
5. **DBSCAN hotspots** identified spatially explicit clusters suitable for conservation prioritization

The Streamlit dashboard enables non-technical stakeholders to explore these patterns interactively. Future extensions could incorporate environmental covariates (climate, habitat type), species distribution modeling (MaxEnt, INLA), and integration with OBIS marine layers for a comprehensive Antarctic biodiversity atlas.

---

## 7. References

1. Terauds, A. et al. (2025). *The Biodiversity of Ice-free Antarctica Database.* Antarctic Biodiversity Information Facility (ANTABIF). https://ipt.biodiversity.aq/resource?r=aas_4296_biodiversity_icefree_antarctica_db

2. SCAR (2023). *SCAR Data Policy.* Scientific Committee on Antarctic Research.

3. Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *KDD*, 96(34), 226–231.

4. Robertson, M. P., Cumming, G. S., & Erasmus, B. F. N. (2010). Getting the most out of atlas data. *Diversity and Distributions*, 16(3), 363–375.

5. Convey, P., et al. (2014). The spatial structure of Antarctic biodiversity. *Ecological Monographs*, 84(2), 203–244.

6. Folium Development Team. Folium: Python wrapper for Leaflet.js. https://python-visualization.github.io/folium/

---

## Appendix A: Reproducibility

```bash
pip install -r requirements.txt
python analyze.py
streamlit run app.py
```

All source code, parameters, and output paths are documented in `README.md`.

## Appendix B: Output Files

| File | Description |
|------|-------------|
| outputs/cleaned_occurrence.csv | Cleaned occurrence records |
| outputs/analysis_summary.json | Machine-readable summary |
| outputs/figures/*.png | Static visualizations |
| outputs/maps/*.html | Interactive Folium maps |
| outputs/clustered_occurrence.csv | Records with DBSCAN labels |
| outputs/hotspot_summary.csv | Cluster centroid statistics |

---

*End of Report*
