# Independent NASA LOLA Site07 analysis

## Scope and scientific separation

This module presents full-tile evidence from NASA GSFC PGDA Product 78, Site07 (“Peak near Shackleton”). It is an independent NASA product display. It is **not spatially registered to the LUNA-TERRA PNS02 exploration polygon**. No PNS02 transformation, raster overlay, coverage calculation, geometry sampling, source-attribute join, or combined score is performed. Every statistic below applies to the complete 3,200 × 3,200 Site07 product grid.

NASA Product 78 identifies its 5 m/pixel product coordinates as south-polar stereographic X/Y metres in MOON_ME/DE421. The actual raster CRS WKT labels its datum unknown. PNS02 vectors use `D_Moon_2000`; an authoritative tie between that datum and MOON_ME/DE421 has not been established. This independent summary avoids depending on such a tie.

## Inputs and integrity

| Product | Local research source | Size | SHA-256 | Units |
|---|---|---:|---|---|
| Site07 surface | `LUNA-TERRA_LOLA_Site07_validation/verified_source_products/Site07_final_adj_5mpp_surf.tif` | 40,980,808 bytes | `38AAEE10BB4DA4D63E7427AA1CA25C79BDBC649D212079A04990E135462091F8` | surface height, m |
| Site07 slope | `LUNA-TERRA_LOLA_Site07_validation/verified_source_products/Site07_final_adj_5mpp_slp.tif` | 40,980,774 bytes | `FEBFE1BF19087F537BBA2F7854D40AC83ADADBA5003F2585B1685CBD90D02219` | degrees |

Source URLs: [surface](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_surf.tif), [slope](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_slp.tif), [NASA Product 78](https://pgda.gsfc.nasa.gov/products/78), [product README](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/README). Both GeoTIFFs were downloaded and validated on 2026-11-15. NASA does not provide comparison SHA-256 hashes in the accessed product listing; these are computed file hashes.

The Phase 3A validation workspace also contains the 1,312-byte `Site07_ROIs.tgz` (SHA-256 `694D85297C40133E91570F020E46F7FD0B25C14E94F0A7C5B6D001E8728BDDBE`), a two-feature ROI shapefile archive inspected in its own NASA product coordinate context but not used by this module, and the 1,829-byte NASA README (SHA-256 `E985A2337C9DE1CD665B0DDAD8B7F1FAC88D65C96D1E47D1B975A91C8E53E7BD`). LDEC, total elevation uncertainty, and slope uncertainty files were not downloaded.

## Grid and data-quality verification

| Property | Surface | Slope | Result |
|---|---|---|---|
| Dimensions / bands | 3,200 × 3,200 / 1 | 3,200 × 3,200 / 1 | Match |
| Stored type | float32 | float32 | Match |
| Pixel spacing | 5 m × 5 m | 5 m × 5 m | Match |
| Affine transform | `(5, 0, 22000; 0, -5, -12000)` | Same | Exact match |
| Product bounds | X 22,000–38,000 m; Y −28,000 to −12,000 m | Same | Exact match |
| CRS metadata | Polar stereographic; unknown datum; sphere radius 1,737,400 m | Same | Exact match |
| NoData marker | NaN | NaN | Same |
| Finite cells | 10,240,000 (100%) | 10,240,000 (100%) | Same validity mask |
| Masked/nonfinite cells | 0 | 0 | Same validity mask |

The grid checks use rasterio dataset CRS equality, exact affine transform equality, shape, bounds, and resolution. Pairwise cell position is therefore consistent within the two NASA products. No pixel values were paired for a joint model or spatial statistic. A NaN NoData marker is present, but there are no NoData/nonfinite cells in either downloaded raster.

“100% finite” means every tile cell stores a finite float value. It does not mean every cell is directly observed. The NASA product page says about 90% of the 5 m polar DEM cells are interpolated in general, and the surface README describes interpolation filling empty pixels. The Site07-specific LDEC count raster was not downloaded, so this analysis does not estimate the Site07 observed/interpolated share. Neither total-elevation-error nor slope-error raster was downloaded.

## Full-tile surface height statistics

All values use finite, unmasked float32 cells; displayed results below are rounded for reading. Percentiles use NumPy linear interpolation; standard deviation is population standard deviation.

| Statistic | Site07 full tile |
|---|---:|
| Valid cells | 10,240,000 |
| NoData/nonfinite cells | 0 |
| Minimum | −418.9165 m |
| 5th percentile | −47.6088 m |
| 25th percentile | 479.2797 m |
| Median | 903.3766 m |
| Mean | 800.0183 m |
| 75th percentile | 1,134.1875 m |
| 95th percentile | 1,437.1169 m |
| Maximum | 1,648.6798 m |
| Population standard deviation | 453.2991 m |

NASA labels the raster values as surface height Z in metres. The displayed descriptive statistics do not estimate elevation/height at PNS02.

## Full-tile slope statistics

| Statistic | Site07 full tile |
|---|---:|
| Valid cells | 10,240,000 |
| NoData/nonfinite cells | 0 |
| Minimum | 0.0000° |
| 5th percentile | 3.2329° |
| 25th percentile | 7.3032° |
| Median | 10.6005° |
| Mean | 10.7347° |
| 75th percentile | 13.9713° |
| 95th percentile | 18.6051° |
| Maximum | 60.4841° |
| Population standard deviation | 4.7001° |

Slope intervals use lower-inclusive, upper-exclusive boundaries and count source pixels:

| Slope interval | Cells | Share of valid slope cells |
|---|---:|---:|
| 0° to <5° | 1,203,779 | 11.7557% |
| 5° to <10° | 3,429,976 | 33.4959% |
| 10° to <15° | 3,692,381 | 36.0584% |
| 15° to <20° | 1,629,665 | 15.9147% |
| 20° to <30° | 280,999 | 2.7441% |
| 30° to <61° | 3,200 | 0.0313% |

The last interval contains all finite values above 30°; the observed maximum is 60.4842°. These are descriptive full-tile bins, not a landing safety threshold or PNS02 measurement.

## Visualization and packaged outputs

The app shows one image pixel per source raster cell in original row/column order. Images are not map overlays and have no PNS02 geometry. Each uses a linear min-to-max palette stretch for display; the colorization is not the original float raster. Exact numerical summaries and histograms were calculated from original float32 values.

Packaged outputs under `data/demo/nasa_site07/`:

- `summary.json` — metadata, source hashes, all summary statistics, histogram bins, software versions, and processing-method caveats.
- `elevation_histogram.csv`, `slope_histogram.csv`, `slope_intervals.csv` — reproducible count tables.
- `site07_surface_native_grid.png`, `site07_slope_native_grid.png` — full-size 3,200 × 3,200 visualizations.
- `PROVENANCE.md`, `checksums.csv` — source details, rerun command, and packaged-output checksums.

Raw NASA GeoTIFFs remain outside Git. The deployed app reads these precomputed JSON/CSV/PNG derivatives; it does not import Rasterio or GDAL. The current full image pair is roughly 7.3 MB, substantially smaller than packaging both ~41 MB source rasters. See [`data/demo/nasa_site07/PROVENANCE.md`](../data/demo/nasa_site07/PROVENANCE.md) for the processor command and dependency versions. Rasterio 1.5.2 publishes Python 3.12+ wheels, including Linux binary builds, but no Community Cloud build was executed; app runtime does not depend on Rasterio.

## Reproducibility and sources

The reproducible implementation is `src/nasa_site07.py`; command-line wrapper is `scripts/process_nasa_site07.py`; optional offline dependency is pinned in `requirements-data.txt`. The command-line workflow checks source hashes against the validated source versions before processing. The run records Python, Rasterio, GDAL, and NumPy versions plus SHA-256 values of both source rasters and processing code. Unit tests cover packaged outputs, full-resolution image dimensions, finite/NoData handling, and rejection of misaligned test grids.

NASA Product 78 says the surface layer is interpolated to fill empty pixels and reports product-level interpolation and uncertainty information; it provides Site07 surface/slope, LDEC and error products. This project downloaded only surface, slope and the ROI archive in the earlier validation. It did not download or calculate LDEC or per-pixel uncertainty. NASA asks users to cite Barker et al. (2021), *Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions*, *Planetary and Space Science* 203, 105119, DOI [10.1016/j.pss.2020.105119](https://doi.org/10.1016/j.pss.2020.105119). NASA’s guidance says NASA-originated material is generally not copyrighted but source-specific rights should be checked; no separate product license was found on Product 78. No NASA insignia or endorsement is used.

## Decision

**GO** for the independent NASA Site07 product module. It is a source-backed full-product summary with verified within-product grid consistency and explicit attribution. It provides no evidence about PNS02 terrain, overlap, or coverage. The unresolved PNS02-to-MOON_ME/DE421 frame tie still blocks any joint spatial analysis.
