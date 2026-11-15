# NASA LOLA Site07 derived demonstration data

This folder contains reproducible, **derived** summaries and visualization assets from NASA GSFC Planetary Geology, Geophysics and Geochemistry Laboratory (PGDA) Product 78, *High-Resolution LOLA Topography for Lunar South Pole Sites*, Site07 (“Peak near Shackleton”). It does not contain the source GeoTIFFs.

## Source files

| Source product | URL | Downloaded bytes | SHA-256 | Values |
|---|---|---:|---|---|
| `Site07_final_adj_5mpp_surf.tif` | [NASA PGDA Site07 surface](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_surf.tif) | 40,980,808 | `38AAEE10BB4DA4D63E7427AA1CA25C79BDBC649D212079A04990E135462091F8` | Surface height, metres |
| `Site07_final_adj_5mpp_slp.tif` | [NASA PGDA Site07 slope](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_slp.tif) | 40,980,774 | `FEBFE1BF19087F537BBA2F7854D40AC83ADADBA5003F2585B1685CBD90D02219` | Slope, degrees |

Both were downloaded and independently validated on 2026-11-15. The source SHA-256 hashes are local integrity identifiers; NASA did not publish these SHA-256 values on the product page. The source products are 3,200 × 3,200 single-band float32 GeoTIFFs with 5 m cells. Both have identical CRS metadata, affine transform, bounds, resolution, and finite-data masks. CRS WKT records an unnamed/unknown datum; NASA Product 78 and its [README](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/README) state the product frame is MOON_ME/DE421 and that pixels are GMT pixel-registered centers.

Also downloaded and inspected in the separate Phase 3A validation workspace, but **not used to generate this package**: `Site07_ROIs.tgz` (1,312 bytes; SHA-256 `694D85297C40133E91570F020E46F7FD0B25C14E94F0A7C5B6D001E8728BDDBE`), whose archive contains a two-feature ROI shapefile, and NASA's 1,829-byte README (`NASA_LOLA_README.txt`; SHA-256 `E985A2337C9DE1CD665B0DDAD8B7F1FAC88D65C96D1E47D1B975A91C8E53E7BD`). The ROI shapefile CRS also labels its datum unknown. The LDEC, total elevation error, and slope error rasters were not downloaded.

## Processing and reproduction

Processing script: [`scripts/process_nasa_site07.py`](../../../scripts/process_nasa_site07.py). Processing module: [`src/nasa_site07.py`](../../../src/nasa_site07.py). Both source raster paths are required as command-line arguments; no Downloads path is hard-coded:

```powershell
python -m pip install -r requirements-data.txt
python scripts/process_nasa_site07.py `
  --surface C:\path\to\Site07_final_adj_5mpp_surf.tif `
  --slope C:\path\to\Site07_final_adj_5mpp_slp.tif `
  --output data\demo\nasa_site07 `
  --download-date 2026-11-15
```

The command-line processor first verifies both inputs against the recorded source SHA-256 hashes. It then verifies that product CRS, shape, affine transform, bounds and resolution match before any row/column correspondence is accepted. It reads masked bands, excludes masked and nonfinite cells, confirms histogram bins account for all valid pixels, computes complete-tile statistics and histograms, and writes one PNG pixel per source pixel. There is no resampling, reprojection, PNS geometry, spatial overlay, or PNS sampling. The images use a fixed linear min/max display stretch; numeric summaries and histograms are calculated from original float32 cells.

Processing environment used: Python 3.15.2, Rasterio 1.5.2, GDAL 3.12.2, NumPy 2.5.4. Offline preprocessing only. The Streamlit app reads JSON/CSV/PNG package outputs and has no Rasterio/GDAL runtime dependency. The exact source and processor-code hashes are recorded in `summary.json`; derived-file SHA-256 hashes are listed in `checksums.csv`.

## Interpretation limits

- All statistics describe the entire Site07 raster tile, not PNS02 or its exploration polygon.
- NASA reports that the polar 5 m LOLA DEMs have an interpolated fraction of about 90% at product level. The Site07 LDEC raster was not downloaded, so the Site07-specific observed/interpolated fraction is unknown.
- LDEC, total elevation uncertainty, and slope uncertainty rasters are not included or summarized.
- NASA’s product description names MOON_ME/DE421, but the GeoTIFF WKT datum is unknown, and PNS02 `D_Moon_2000` has no established tie to that frame. The sources are not spatially registered together.
- The map palette is a visual encoding; it does not preserve exact per-pixel float values. Full-tile statistics and histogram counts use the original raster values.
- NASA Product 78 requests citation to Barker et al. (2021), DOI [10.1016/j.pss.2020.105119](https://doi.org/10.1016/j.pss.2020.105119). The product page did not state a separate license. NASA’s [media-use guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/) says NASA material is generally not copyrighted and asks users to verify third-party/source-specific rights. This project provides attribution and does not imply NASA endorsement or use NASA marks.
