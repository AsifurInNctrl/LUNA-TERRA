# PNS02 validation record

## Data and method
Inputs are the user-supplied official Zenodo v1 extraction under `%USERPROFILE%\Downloads\LUNA-TERRA_PNS02_inspection`. Zenodo DOI: [10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058). The archive MD5 hashes for `PSR_Volatile_Estimates.zip` and `Landing_Sites.zip` were verified against the Zenodo file table; the workbook hash was also verified. See `pns02_official_source_reconciliation.md`.

`src/pns02_data.py` reads shapefile geometries and `.prj` WKT with PyShp/PyProj. It verifies the site and exploration CRSs are equivalent, then transforms PSR polygons from `Moon_2000_South_Pole_Stereographic` into the exploration-area lunar CRS using `always_xy=True`. It refuses invalid geometry and does not repair or discard features. Spatial intersections/areas use projected metres.

## Reproduced checks

- 141 PSR source polygons; 0 invalid in inspected source.
- `Name=PNS02` resolves uniquely to exploration feature `ORIG_FID=39`; `BUFF_DIST=2000`.
- Area: 12,565,537.34 m².
- Five positive-area overlaps: 324, 325, 330, 335, 338.
- ID 335 workbook coordinate `(-88.737914, -109.246494)` is ~59.8 km from polygon `Id_1=335`.
- The five workbook and polygon `meanAge` pairs differ.
- Volatile aggregation is unresolved; app displays raw source fields only.

## Status definitions

PASS means local file identity or calculation was reproduced. FAIL means a stated source association/check does not hold (not that either record is necessarily wrong). INCONCLUSIVE means evidence does not establish the scientifically correct interpretation. Archive checksums are documented in the detailed reconciliation report.

## Citations and acknowledgment

Wueller et al. (2026), JGR: Planets, [10.1029/2025JE009434](https://doi.org/10.1029/2025JE009434). Official data: [Zenodo 10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058). Supporting Information S1 assisted in identifying the detailed-method source; full method verification remains incomplete.
