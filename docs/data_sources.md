# Data sources

## Integrated source vectors

| Dataset | Product | Use |
|---|---|---|
| Zenodo 10.5281/zenodo.17084058 | `PSR_Volatile_Estimates/PSR_volatile_abundance_final` shapefile | 141 PSR geometries and original attributes |
| Same record | `Landing_Sites/LandingSites` shapefile | candidate site context |
| Same record | `Landing_Sites/ExplorationArea_2km` shapefile | PNS02 exploration region |

Required shapefile sidecars are packaged under `data/demo/pns02/`; provenance, CC BY 4.0 attribution, authors, version and SHA-256 checksums are in that directory. No age workbook or ZIP archive is distributed.

## NASA LOLA investigation (not integrated)

NASA GSFC PGDA Product 78, *High-Resolution LOLA Topography for Lunar South Pole Sites*, lists Site07 under the high-resolution site data. It publishes `Site07_final_adj_5mpp_surf.tif` (surface elevation) and `Site07_final_adj_5mpp_slp.tif` (slope), plus LDEC, uncertainty and XYZI products. HTTP HEAD checks on 2026-11-15 returned image/tiff and sizes of 40,980,808 bytes (surface) and 40,980,774 bytes (slope). They are not huge, but TIFF metadata/CRS/coverage have not been independently inspected because no rasterio/GDAL is present. Site07's named region is Peak Near Shackleton, but the actual footprint versus PNS02 and the product lunar reference frame must be confirmed before reprojection/sampling. Both rasters are ~5 m/pixel gridded LOLA-derived products; resolution does not mean uniform 5 m independent measurements, and interpolation/track coverage and uncertainty matter.

NASA's page requests citation: Barker, M.K., et al. (2021), “Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions,” *Planetary and Space Science* 203, 105119, DOI [10.1016/j.pss.2020.105119](https://doi.org/10.1016/j.pss.2020.105119).

Conclusion: no NASA mission product is currently loaded by the app. LOLA Site07 is the smallest reasonable next product, but do not integrate until raster CRS, lunar frame, footprint, no-data values, vertical units/datum, and uncertainty metadata are verified. Avoid assuming that the Site07 raster shares the shapefile's CRS or datum merely because both concern the Moon.

NASA product: [PGDA Product 78](https://pgda.gsfc.nasa.gov/products/78).
