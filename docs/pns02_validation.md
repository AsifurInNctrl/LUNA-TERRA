# PNS02 validation record

## Data locations and provenance

The original research and inspection workspace was maintained separately at `%USERPROFILE%\Downloads\LUNA-TERRA_PNS02_inspection`. It contains the source extraction and inspection materials; it is not required by the deployed application.

The application loads its demonstration shapefiles from the repository-relative `data/demo/pns02/` directory. The included PSR, landing-site, and exploration-area shapefile components are a selected subset of the official Zenodo v1 dataset. Source authors, DOI, version, CC BY 4.0 attribution, and copying notes are recorded in [`data/demo/pns02/PROVENANCE.md`](../data/demo/pns02/PROVENANCE.md). SHA-256 values for the packaged files are listed in [`data/demo/pns02/checksums.csv`](../data/demo/pns02/checksums.csv).

During research preparation, the original downloaded `PSR_Volatile_Estimates.zip`, `Landing_Sites.zip`, and age workbook were checksum-compared with the official Zenodo file checksums. This was a preparation-time verification. The Streamlit app does not recompute packaged-file SHA-256 hashes at startup, contact Zenodo, or automatically compare files to the checksum manifest. A manifest entry documents a checksum; it is not a runtime integrity check.

## Data and method

`src/pns02_data.py` loads the packaged shapefiles and their `.prj` WKT using PyShp and PyProj. It verifies the site and exploration CRSs are equivalent, then transforms PSR polygons from `Moon_2000_South_Pole_Stereographic` into the exploration-area lunar CRS using `always_xy=True`. It refuses invalid geometry and does not repair or discard features. Spatial intersections and areas use projected metres.

## Reproduced checks

- 141 PSR source polygons; 0 invalid in the inspected source.
- `Name=PNS02` resolves uniquely to exploration feature `ORIG_FID=39`; `BUFF_DIST=2000`.
- Area: 12,565,537.34 m².
- Five positive-area overlaps: 324, 325, 330, 335, 338.
- ID 335 workbook coordinate `(-88.737914, -109.246494)` is ~59.8 km from polygon `Id_1=335`.
- The five workbook and polygon `meanAge` pairs differ.
- Volatile aggregation is unresolved; app displays raw source fields only.

The intersection count and areas are project-derived spatial calculations over source geometries. They do not establish scientific identity between crater and PSR records or validate source-model interpretations.

## Status definitions

PASS means the stated file identity or calculation was reproduced. FAIL means a stated source association or equality check does not hold (not that either source record is necessarily wrong). INCONCLUSIVE means evidence does not establish the scientifically correct interpretation. Preparation-time archive checksums and packaged-file manifest entries are provenance evidence, not checks run by the deployed app at runtime.

## Citations and acknowledgment

Wueller et al. (2026), JGR: Planets, [10.1029/2025JE009434](https://doi.org/10.1029/2025JE009434). Official data: [Zenodo 10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058). Zenodo v1 data are attributed under CC BY 4.0; see the repository provenance record. Supporting Information S1 assisted in identifying the detailed-method source; full method verification remains incomplete.

The app also contains a separate standalone NASA LOLA Site07 full-tile evidence module. No NASA raster is registered to or sampled over PNS02; see [`data_sources.md`](data_sources.md) and [`nasa_site07_independent_analysis.md`](nasa_site07_independent_analysis.md).
