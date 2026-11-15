# LUNA-TERRA — PNS02 Evidence Explorer

A Streamlit evidence explorer for candidate landing site PNS02 and nearby permanently shadowed regions near the lunar south pole. It inspects supplied source vector data, exposes unresolved source relationships, and organizes literature-supported Earth analog research candidates. It does not quantitatively compare or rank Earth analogs.

## Current functionality

- Loads 141 PSR polygons, landing-site points and the PNS02 2 km exploration area from repository-relative `data/demo/pns02/`.
- Transforms PSRs from the supplied lunar south-pole stereographic CRS into the verified lunar exploration-area CRS.
- Displays real polygon geometries in projected lunar X/Y metres, interactive feature selection, source attributes, positive-area overlaps, and PASS/FAIL/INCONCLUSIVE evidence notes.
- Presents an independent, precomputed NASA LOLA Site07 full-tile elevation/slope summary with native-grid images and distributions. It is not spatially registered to PNS02.
- Provides a literature-grounded Earth Analog Evidence Matrix for five distinct research candidates, with sources, process-specific purposes, limitations and future measurement needs. It reports no computational analog validation or ranking.

## Install and run

Python 3.12 is the deployment target. In a clean Python 3.12 environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Current workspace launch (existing venv):

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Data provenance and attribution

Demo shapefiles are a small set of required components from Wueller et al., *Complementary Data for Wueller et al. (2026)*, Zenodo record v1, DOI [10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058), licensed CC BY 4.0. Citation: Wueller, L., Berger, L. M., Christopher, H., Sugimoto, K., Thaker, A. D., Carton, L., Jo, W., Lee, S., Pedrelli, R., Sanchez, P., & Kring, D. A. (2026). *Assessing Potential Landing Sites With Favorable Illumination and Accessible, Potentially Volatile-Rich Permanently Shadowed Regions Within Artemis Candidate Landing Regions*. JGR: Planets, 131(3), e2025JE009434. DOI [10.1029/2025JE009434](https://doi.org/10.1029/2025JE009434).

File-level SHA-256 checksums and attribution are in `data/demo/pns02/`. Original archive hashes were verified during research preparation; the deployed app does not recompute package hashes or contact Zenodo at runtime. The original source workspace remains outside this repository; workbooks, archives, layerfiles and unrelated datasets are not packaged.

## Streamlit Community Cloud

1. Push the reviewed `main` branch to `AsifurInNctrl/LUNA-TERRA` after your team approves the diff.
2. In Streamlit Community Cloud, create an app from that repository, branch `main`, entry point `app.py`.
3. Select Python 3.12 in Advanced settings; dependencies are read from `requirements.txt`.
4. No secrets or custom configuration are required.

## Scientific limitations and open questions

- ID 335's workbook coordinate is about 59.8 km from PSR polygon `Id_1=335`; no join is corrected.
- Workbook and polygon `meanAge` fields differ for all five investigated IDs; same field names do not prove equivalent methods.
- Five-feature volatile aggregation does not reproduce the paper's approximate PNS02 total. The app does not label DBF fields as `Volatiles_max`, aggregate them, or assert accessible water.
- NASA LOLA Site07 is included as a separate product-level evidence module. Raw GeoTIFFs are not packaged; the app reads precomputed derivatives and makes no PNS02 raster coverage or terrain claim. See `docs/nasa_site07_independent_analysis.md`.
- Cross-planet analog measurements, uncertainty models, and candidate rankings are not implemented.

See `docs/pns02_validation.md`, `docs/pns02_official_source_reconciliation.md`, and `docs/limitations.md` for validation details.

See `docs/earth_analog_evidence_matrix.md` for the evidence hierarchy, candidate rationale, comparison dimensions, citations and data requirements. The matrix is a literature-led research framework; its cited evidence is not a direct LUNA-TERRA measurement.

### Optional NASA raster preprocessing

The deployed app does not require Rasterio/GDAL or the original NASA GeoTIFFs. To reproduce the packaged Site07 summaries locally, install the optional processor dependency and run `scripts/process_nasa_site07.py`; instructions and source checksums are in `data/demo/nasa_site07/PROVENANCE.md`.
