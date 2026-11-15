# Limitations

- This is a lunar spatial evidence viewer, not a validated Earth analog discovery or ranking system.
- No NASA mission raster/altimetry observations are currently integrated.
- Source PSR and exploration layers use different lunar projected CRSs; the app transforms PSRs into the exploration-area CRS using their supplied WKT. The CRS names/datum conventions originate in the source data and have not been independently re-derived from mission control networks.
- Five PSR polygons have positive-area overlap with the 2 km exploration zone. Intersection does not by itself establish that a crater-center record and PSR polygon identify the same geological object.
- ID 335 has an approximately 59.8 km workbook-coordinate versus PSR polygon mismatch. No coordinate or identifier was altered.
- Workbook and shapefile attributes both contain `meanAge`, but values differ for all five target IDs; names alone do not prove matching definitions.
- DBF fields remain displayed under original names (`Volatiles_`, `Volatiles1`). The app does not label a field `Volatiles_max` or sum volatile estimates. Published cumulative value and source aggregation rule remain unresolved.
- The cited paper's estimates are models, not direct evidence of accessible ice. Supporting Information S1 method review is incomplete.
- Shapefile attributes may omit field aliases, units, uncertainty, and model provenance; consult the Zenodo layer file, paper, and SI before quantitative interpretation.
