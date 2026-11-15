# Data sources

## Integrated source vectors

| Dataset | Product | Use |
|---|---|---|
| Zenodo 10.5281/zenodo.17084058 | `PSR_Volatile_Estimates/PSR_volatile_abundance_final` shapefile | 141 PSR geometries and original attributes |
| Same record | `Landing_Sites/LandingSites` shapefile | candidate site context |
| Same record | `Landing_Sites/ExplorationArea_2km` shapefile | PNS02 exploration region |

Required shapefile sidecars are packaged under `data/demo/pns02/`; provenance, CC BY 4.0 attribution, authors, version and SHA-256 checksums are in that directory. No age workbook or ZIP archive is distributed.

## NASA LOLA Site07 (independent evidence module)

NASA GSFC PGDA Product 78, [High-Resolution LOLA Topography for Lunar South Pole Sites](https://pgda.gsfc.nasa.gov/products/78), supplies Site07 (“Peak near Shackleton”) surface height and slope products. The app contains full-tile summaries and native-grid visualizations derived from:

- `Site07_final_adj_5mpp_surf.tif` — float32 surface height, metres; source SHA-256 `38AAEE10BB4DA4D63E7427AA1CA25C79BDBC649D212079A04990E135462091F8`.
- `Site07_final_adj_5mpp_slp.tif` — float32 slope, degrees; source SHA-256 `FEBFE1BF19087F537BBA2F7854D40AC83ADADBA5003F2585B1685CBD90D02219`.

Both source GeoTIFFs are 3,200 × 3,200, 5 m, and have identical CRS metadata, affine transform, bounds, resolution, and finite-data masks. NASA product documentation identifies the data coordinates as MOON_ME/DE421 and says the surface layer fills empty pixels by interpolation; the embedded GeoTIFF datum is unnamed/unknown. NASA describes about 90% interpolated pixels for the polar 5 m DEMs at product level. The LDEC and uncertainty rasters were not downloaded, so Site07-specific observation support, interpolation fraction, and uncertainty are not calculated.

The application treats this as a separate NASA product. It does not transform or overlay these rasters with PNS02, compute PNS02 coverage, or describe the Site07 full-tile statistics as PNS02 measurements. Only precomputed JSON, CSV, and full-grid colorized PNG derivatives are packaged under `data/demo/nasa_site07/`; the raw rasters remain outside Git. The app requires no Rasterio/GDAL. Reprocessing is optional and uses `requirements-data.txt` plus `scripts/process_nasa_site07.py`.

NASA's page requests citation: Barker, M.K., et al. (2021), “Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions,” *Planetary and Space Science* 203, 105119, DOI [10.1016/j.pss.2020.105119](https://doi.org/10.1016/j.pss.2020.105119).

The offline calculations, checksums, summary definitions, and limitations are described in [`nasa_site07_independent_analysis.md`](nasa_site07_independent_analysis.md) and [`data/demo/nasa_site07/PROVENANCE.md`](../data/demo/nasa_site07/PROVENANCE.md). NASA data-use guidance notes that NASA material is generally not copyrighted while warning users to verify source-specific rights; Product 78’s accessed page gives a citation but no separate license statement. No NASA marks or endorsement claims are used.

NASA product: [PGDA Product 78](https://pgda.gsfc.nasa.gov/products/78).
