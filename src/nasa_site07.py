"""Offline processing and packaged summaries for NASA LOLA Site07.

This module deliberately does not transform, register, or join the NASA grid
with any PNS02 geometry. Rasterio and NumPy are imported only by the offline
processor; the deployed Streamlit app reads the small derived JSON/CSV/PNG files.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import struct
import zlib
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE_DIR = REPOSITORY_ROOT / "data" / "demo" / "nasa_site07"
PRODUCT_URL = "https://pgda.gsfc.nasa.gov/products/78"
README_URL = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/README"
SURFACE_URL = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_surf.tif"
SLOPE_URL = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site07/Site07_final_adj_5mpp_slp.tif"
EXPECTED_SOURCE_SHA256 = {
    "surface": "38aaee10bb4da4d63e7427aa1ca25c79bdbc649d212079a04990e135462091f8",
    "slope": "febfe1bf19087f537bba2f7854d40ac83adadba5003f2585b1685cbd90d02219",
}

_ELEVATION_STOPS = ((18, 33, 73), (54, 74, 128), (109, 82, 132),
                    (177, 105, 107), (224, 164, 111), (248, 224, 173))
_SLOPE_STOPS = ((17, 74, 86), (35, 126, 123), (122, 174, 111),
                (228, 177, 88), (184, 75, 59))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _interpolate_palette(stops: tuple[tuple[int, int, int], ...]) -> list[tuple[int, int, int]]:
    colors = []
    segments = len(stops) - 1
    for i in range(255):
        position = i / 254 * segments
        segment = min(int(position), segments - 1)
        fraction = position - segment
        colors.append(tuple(round(stops[segment][channel] * (1 - fraction)
                                  + stops[segment + 1][channel] * fraction)
                             for channel in range(3)))
    return colors


def _write_indexed_png(path: Path, values: Any, valid: Any,
                       minimum: float, maximum: float,
                       stops: tuple[tuple[int, int, int], ...]) -> None:
    """Write one palette-index PNG pixel per source grid cell, without resampling."""
    import numpy as np

    data = np.asarray(values, dtype=np.float32)
    mask = np.asarray(valid, dtype=bool) & np.isfinite(data)
    palette = _interpolate_palette(stops)
    rgb = [(0, 0, 0), *palette]
    plte = bytes(component for color in rgb for component in color)
    scanlines = bytearray()
    span = maximum - minimum
    for row, row_mask in zip(data, mask):
        scanlines.append(0)  # PNG filter type: None
        scaled = np.zeros(row.shape, dtype=np.uint8)
        if span > 0:
            scaled[row_mask] = (1 + np.rint(np.clip((row[row_mask] - minimum) / span,
                                                    0.0, 1.0) * 254)).astype(np.uint8)
        scanlines.extend(scaled.tobytes())

    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    height, width = data.shape
    header = struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)
    encoded = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
               + chunk(b"PLTE", plte) + chunk(b"tRNS", b"\x00")
               + chunk(b"IDAT", zlib.compress(bytes(scanlines), level=6))
               + chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded)


def _stats(values: Any, valid: Any, units: str, histogram_edges: Any) -> dict[str, Any]:
    import numpy as np

    data = np.asarray(values, dtype=np.float64)
    mask = np.asarray(valid, dtype=bool) & np.isfinite(data)
    clean = data[mask]
    if clean.size == 0:
        raise ValueError("Raster contains no finite, unmasked pixels")
    quantiles = np.percentile(clean, [5, 25, 50, 75, 95], method="linear")
    counts, edges = np.histogram(clean, bins=histogram_edges)
    if int(counts.sum()) != int(clean.size):
        raise ValueError("Histogram bins failed to account for every valid source pixel")
    return {
        "units": units,
        "valid_pixel_count": int(clean.size),
        "nodata_or_nonfinite_pixel_count": int(data.size - clean.size),
        "total_pixel_count": int(data.size),
        "valid_fraction": float(clean.size / data.size),
        "minimum": float(clean.min()),
        "maximum": float(clean.max()),
        "mean": float(clean.mean()),
        "median": float(quantiles[2]),
        "standard_deviation_population": float(clean.std(ddof=0)),
        "percentiles_linear": {str(p): float(v) for p, v in zip((5, 25, 50, 75, 95), quantiles)},
        "histogram_edges": [float(x) for x in edges],
        "histogram_counts": [int(x) for x in counts],
    }


def _grid_metadata(dataset: Any) -> dict[str, Any]:
    return {
        "width": dataset.width,
        "height": dataset.height,
        "bands": dataset.count,
        "dtype": dataset.dtypes[0],
        "nodata": "NaN" if isinstance(dataset.nodata, float) and math.isnan(dataset.nodata) else dataset.nodata,
        "transform": list(dataset.transform)[:6],
        "bounds": [dataset.bounds.left, dataset.bounds.bottom,
                   dataset.bounds.right, dataset.bounds.top],
        "resolution": list(dataset.res),
        "crs_wkt": dataset.crs.to_wkt() if dataset.crs else None,
        "tags": dataset.tags(),
    }


def process_site07(surface_path: str | Path, slope_path: str | Path,
                   output_dir: str | Path = DEFAULT_PACKAGE_DIR,
                   download_date: str = "2026-11-15",
                   expected_source_sha256: dict[str, str] | None = None) -> dict[str, Any]:
    """Validate and summarize native Site07 products, then write distributable derivatives."""
    try:
        import numpy as np
        import rasterio
    except ImportError as exc:  # optional offline-only stack
        raise RuntimeError("Offline NASA processing requires Rasterio; install requirements-data.txt") from exc

    surface_path, slope_path, output_dir = Path(surface_path), Path(slope_path), Path(output_dir)
    for path in (surface_path, slope_path):
        if not path.is_file():
            raise FileNotFoundError(f"NASA Site07 source raster not found: {path}")
    source_hashes = {"surface": _sha256(surface_path), "slope": _sha256(slope_path)}
    if expected_source_sha256 is not None:
        mismatches = [key for key, expected in expected_source_sha256.items()
                      if source_hashes.get(key) != expected.lower()]
        if mismatches:
            raise ValueError("NASA Site07 source checksum mismatch for: " + ", ".join(mismatches))

    with rasterio.open(surface_path) as surface, rasterio.open(slope_path) as slope:
        if surface.count != 1 or slope.count != 1:
            raise ValueError("Expected one-band NASA Site07 surface and slope rasters")
        same_grid = (surface.crs == slope.crs and surface.transform == slope.transform
                     and surface.shape == slope.shape and surface.bounds == slope.bounds
                     and surface.res == slope.res)
        if not same_grid:
            raise ValueError("NASA Site07 products are not on the same native grid; row/column pairing refused")

        surface_array = surface.read(1, masked=True).filled(np.nan)
        slope_array = slope.read(1, masked=True).filled(np.nan)
        surface_valid = np.isfinite(surface_array)
        slope_valid = np.isfinite(slope_array)
        surface_stats = _stats(surface_array, surface_valid, "m", 100)
        slope_stats = _stats(slope_array, slope_valid, "degrees", np.arange(0, 62, 1, dtype=float))

        # This verifies which cells could be paired; no joint PNS analysis is performed.
        valid_masks_equal = bool(np.array_equal(surface_valid, slope_valid))
        _write_indexed_png(output_dir / "site07_surface_native_grid.png", surface_array,
                           surface_valid, surface_stats["minimum"], surface_stats["maximum"],
                           _ELEVATION_STOPS)
        _write_indexed_png(output_dir / "site07_slope_native_grid.png", slope_array,
                           slope_valid, slope_stats["minimum"], slope_stats["maximum"],
                           _SLOPE_STOPS)

        source_meta = {
            "surface": _grid_metadata(surface),
            "slope": _grid_metadata(slope),
        }

    broad_bins = []
    for low, high in ((0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 61)):
        count = int(((slope_array >= low) & (slope_array < high) & slope_valid).sum())
        broad_bins.append({"lower_inclusive_deg": low, "upper_exclusive_deg": high,
                           "valid_pixel_count": count,
                           "percent_of_valid_slope_pixels": 100 * count / slope_stats["valid_pixel_count"]})

    provenance = {
        "product": "NASA GSFC PGDA Product 78, High-Resolution LOLA Topography for Lunar South Pole Sites; Site07 (Peak near Shackleton)",
        "product_url": PRODUCT_URL,
        "readme_url": README_URL,
        "source_urls": {"surface": SURFACE_URL, "slope": SLOPE_URL},
        "source_download_date": download_date,
        "source_sha256": source_hashes,
        "processing_script_sha256": None,
        "processor_module_sha256": _sha256(Path(__file__).resolve()),
        "software": {"python": __import__("sys").version.split()[0],
                     "rasterio": rasterio.__version__, "gdal": rasterio.__gdal_version__,
                     "numpy": np.__version__},
        "method": "Read each single-band GeoTIFF on its native grid; masked-read NoData; exclude masked/non-finite samples; calculate full-tile descriptive statistics and fixed-bin histograms; render one PNG cell per source pixel using a linear 255-color palette stretch. No resampling, reprojection, PNS02 geometry, or spatial join.",
        "source_frame_claim": "NASA product page and README state MOON_ME / DE421; embedded raster CRS has an unknown/unnamed datum.",
        "pns02_registration": "None. NASA Site07 evidence is standalone and is not registered to the PNS02 exploration polygon.",
        "limitations": [
            "Summaries describe the complete NASA Site07 raster tile, not PNS02.",
            "NASA documentation says the 5 m polar DEM has a large interpolated fraction (about 90% product-wide); the specific Site07 LDEC raster was not downloaded, so its observed/interpolated proportion is not measured here.",
            "LDEC, total elevation uncertainty, and slope uncertainty rasters were not among the downloaded source files and are not summarized.",
            "The GeoTIFF CRS metadata does not encode its named MOON_ME/DE421 frame; the NASA product documentation provides that product-level statement.",
            "The visualization uses a palette and is not a replacement for source float values; exact summaries and histograms derive from original float32 cells."
        ],
        "attribution": "NASA GSFC PGDA Product 78; cite Barker et al. (2021), DOI 10.1016/j.pss.2020.105119. No NASA logo or endorsement is implied.",
    }
    result = {
        "schema_version": 1,
        "product": provenance["product"],
        "grid": source_meta,
        "grid_alignment": {
            "same_crs": True, "same_affine_transform": True, "same_shape": True,
            "same_bounds": True, "same_resolution": True,
            "same_valid_mask": valid_masks_equal,
            "row_column_pairing_supported_within_nasa_product": True,
            "pns02_overlay_performed": False,
        },
        "elevation": surface_stats,
        "slope": slope_stats,
        "slope_broad_intervals": broad_bins,
        "provenance": provenance,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for key, stats in (("elevation", surface_stats), ("slope", slope_stats)):
        units = stats["units"]
        with (output_dir / f"{key}_histogram.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow([f"lower_edge_{units}", f"upper_edge_{units}", "pixel_count"])
            writer.writerows(zip(stats["histogram_edges"][:-1], stats["histogram_edges"][1:],
                                 stats["histogram_counts"]))
    with (output_dir / "slope_intervals.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(broad_bins[0]))
        writer.writeheader()
        writer.writerows(broad_bins)
    return result


def load_packaged_summary(data_dir: str | Path = DEFAULT_PACKAGE_DIR) -> dict[str, Any]:
    """Load the self-contained derived product used by the deployed app."""
    summary_path = Path(data_dir) / "summary.json"
    if not summary_path.is_file():
        raise FileNotFoundError(f"Packaged NASA Site07 summary missing: {summary_path}")
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("grid_alignment", {}).get("pns02_overlay_performed") is not False:
        raise ValueError("NASA Site07 package has an unsupported or unsafe schema")
    for image in ("site07_surface_native_grid.png", "site07_slope_native_grid.png"):
        if not (Path(data_dir) / image).is_file():
            raise FileNotFoundError(f"Packaged NASA Site07 visualization missing: {Path(data_dir) / image}")
    return data

