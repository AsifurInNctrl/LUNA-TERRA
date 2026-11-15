from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from src.nasa_site07 import DEFAULT_PACKAGE_DIR, load_packaged_summary


class NASAProductPackageTests(unittest.TestCase):
    def test_packaged_product_is_standalone_and_has_known_full_tile_statistics(self):
        data = load_packaged_summary()
        self.assertEqual(data["product"], "NASA GSFC PGDA Product 78, High-Resolution LOLA Topography for Lunar South Pole Sites; Site07 (Peak near Shackleton)")
        self.assertEqual(data["elevation"]["units"], "m")
        self.assertEqual(data["slope"]["units"], "degrees")
        self.assertEqual(data["elevation"]["valid_pixel_count"], 10_240_000)
        self.assertEqual(data["slope"]["valid_pixel_count"], 10_240_000)
        self.assertEqual(data["elevation"]["nodata_or_nonfinite_pixel_count"], 0)
        self.assertEqual(data["slope"]["nodata_or_nonfinite_pixel_count"], 0)
        self.assertAlmostEqual(data["elevation"]["mean"], 800.018298562455, places=8)
        self.assertAlmostEqual(data["elevation"]["median"], 903.3766174316406, places=8)
        self.assertAlmostEqual(data["slope"]["mean"], 10.734660670320594, places=8)
        self.assertAlmostEqual(data["slope"]["median"], 10.600532531738281, places=5)
        self.assertFalse(data["grid_alignment"]["pns02_overlay_performed"])
        self.assertTrue(data["grid_alignment"]["same_affine_transform"])

    def test_histograms_account_for_every_valid_source_pixel(self):
        data = load_packaged_summary()
        for layer in ("elevation", "slope"):
            hist = data[layer]
            self.assertEqual(len(hist["histogram_edges"]), len(hist["histogram_counts"]) + 1)
            self.assertEqual(sum(hist["histogram_counts"]), hist["valid_pixel_count"])
        self.assertEqual(sum(row["valid_pixel_count"] for row in data["slope_broad_intervals"]), 10_240_000)

    def test_visualizations_are_full_native_grid_pixel_dimensions(self):
        for name in ("site07_surface_native_grid.png", "site07_slope_native_grid.png"):
            payload = (DEFAULT_PACKAGE_DIR / name).read_bytes()
            self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"))
            width = int.from_bytes(payload[16:20], "big")
            height = int.from_bytes(payload[20:24], "big")
            self.assertEqual((width, height), (3200, 3200))

    def test_output_manifest_matches_derived_files_and_source_hashes_are_recorded(self):
        data = load_packaged_summary()
        manifest = DEFAULT_PACKAGE_DIR / "checksums.csv"
        with manifest.open(newline="", encoding="utf-8-sig") as stream:
            for row in csv.DictReader(stream):
                digest = hashlib.sha256((DEFAULT_PACKAGE_DIR / row["file"]).read_bytes()).hexdigest().upper()
                self.assertEqual(digest, row["sha256"])
        self.assertEqual(data["provenance"]["source_sha256"]["surface"],
                         "38aaee10bb4da4d63e7427aa1ca25c79bdbc649d212079a04990e135462091f8")
        self.assertEqual(data["provenance"]["source_sha256"]["slope"],
                         "febfe1bf19087f537bba2f7854d40ac83adadba5003f2585b1685cbd90d02219")
        self.assertFalse(any(DEFAULT_PACKAGE_DIR.glob("*.tif")))

    def test_missing_packaged_summary_is_actionable(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(FileNotFoundError, "Packaged NASA Site07 summary missing"):
                load_packaged_summary(temp)


try:
    import numpy as np
    import rasterio
    from rasterio.transform import from_origin
except ImportError:  # Rasterio belongs to the optional offline processing environment.
    np = None
    rasterio = None


@unittest.skipIf(rasterio is None, "Install optional requirements-data.txt for GeoTIFF processor tests")
class NASAOfflineProcessorTests(unittest.TestCase):
    def _write_raster(self, path: Path, values, transform=None, nodata=-9999):
        array = np.asarray(values, dtype="float32")
        with rasterio.open(path, "w", driver="GTiff", height=array.shape[0], width=array.shape[1],
                           count=1, dtype="float32", crs="EPSG:4326",
                           transform=transform or from_origin(0, 2, 1, 1), nodata=nodata) as ds:
            ds.write(array, 1)

    def test_geotiff_reading_excludes_nodata_and_preserves_native_pixel_grid(self):
        from src.nasa_site07 import process_site07

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            surface = root / "Site07_final_adj_5mpp_surf.tif"
            slope = root / "Site07_final_adj_5mpp_slp.tif"
            self._write_raster(surface, [[1, 2, -9999], [4, 5, 6]])
            self._write_raster(slope, [[10, 20, -9999], [30, 40, 50]])
            result = process_site07(surface, slope, root / "out")
            self.assertTrue(result["grid_alignment"]["same_valid_mask"])
            self.assertEqual(result["elevation"]["valid_pixel_count"], 5)
            self.assertEqual(result["elevation"]["nodata_or_nonfinite_pixel_count"], 1)
            self.assertEqual(result["elevation"]["mean"], 3.6)
            self.assertEqual(result["slope"]["valid_pixel_count"], 5)
            self.assertEqual(result["grid"]["surface"]["width"], 3)
            self.assertEqual(result["grid"]["surface"]["transform"], [1.0, 0.0, 0.0, 0.0, -1.0, 2.0])
            self.assertFalse(result["grid_alignment"]["pns02_overlay_performed"])

    def test_processor_refuses_row_column_pairing_on_shifted_grid(self):
        from src.nasa_site07 import process_site07

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            surface = root / "Site07_final_adj_5mpp_surf.tif"
            slope = root / "Site07_final_adj_5mpp_slp.tif"
            self._write_raster(surface, [[1, 2], [3, 4]])
            self._write_raster(slope, [[10, 20], [30, 40]],
                               transform=from_origin(0.5, 2, 1, 1))
            with self.assertRaisesRegex(ValueError, "not on the same native grid"):
                process_site07(surface, slope, root / "out")


if __name__ == "__main__":
    unittest.main()
