import unittest
import shutil
import tempfile
from pathlib import Path

from pyproj import CRS, Transformer
from shapely.geometry import box

from src.pns02_data import (candidates, default_psr_record, load_pns02_data,
                            ordered_psr_records, overlap_summary,
                            pns02_site_candidates, viewport_bounds,
                            unique_candidate, default_selection_label,
                            _read_layer, _transform_geometries)


class PNS02DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_pns02_data()

    def test_loads_source_feature_counts_and_crs(self):
        self.assertEqual(len(self.data["psr_geoms"]), 141)
        self.assertEqual(self.data["display_crs"].name, "Moon2000_spole")
        self.assertTrue(self.data["transformed"])

    def test_transformation_targets_packaged_exploration_crs(self):
        crs_path = self.data["root"] / "Landing_Sites" / "ExplorationArea_2km.prj"
        self.assertTrue(self.data["display_crs"].equals(CRS.from_wkt(crs_path.read_text(encoding="utf-8"))))
        self.assertTrue(self.data["psr_crs"].equals(CRS.from_wkt((self.data["root"] / "PSR_Volatile_Estimates" / "PSR_volatile_abundance_final.prj").read_text(encoding="utf-8"))))

    def test_pns02_area_and_five_intersections(self):
        idx = candidates(self.data)
        self.assertEqual(len(idx), 1)
        rows = overlap_summary(self.data, idx[0])
        self.assertEqual({int(r["Id_1"]) for r in rows}, {324, 325, 330, 335, 338})

    def test_source_attributes_preserved(self):
        fields = set(self.data["psr_attrs"][0])
        self.assertTrue({"Id_1", "meanAge", "Volatiles_", "Volatiles1", "Shape_Area"} <= fields)

    def test_transform_geometry_is_valid(self):
        self.assertTrue(all(g.is_valid for g in self.data["psr_geoms"]))

    def test_known_transformed_bounds_match_baseline(self):
        expected = {
            338: (22880.455003, -15672.716376, 23023.317923, -15470.829192),
            335: (22841.130839, -16429.196498, 22888.372925, -16364.281193),
            325: (21864.597826, -17205.073546, 21969.954946, -17110.380953),
            324: (23477.478814, -17631.805923, 23652.960381, -17449.126254),
            330: (22113.253618, -18136.126004, 22246.342232, -17977.351592),
        }
        by_id = {int(a["Id_1"]): g for a, g in zip(self.data["psr_attrs"], self.data["psr_geoms"])}
        for feature_id, bounds in expected.items():
            for actual, baseline in zip(by_id[feature_id].bounds, bounds):
                self.assertAlmostEqual(actual, baseline, delta=0.001)

    def test_overlap_fractions_match_baseline(self):
        area_i = candidates(self.data)[0]
        actual = {int(r["Id_1"]): r["overlap_pct"] for r in overlap_summary(self.data, area_i)}
        expected = {338: 0.6754996194, 335: 100.0, 325: 100.0,
                    324: 71.1328493341, 330: 100.0}
        self.assertEqual(set(actual), set(expected))
        for feature_id, fraction in expected.items():
            self.assertAlmostEqual(actual[feature_id], fraction, delta=1e-8)

    def test_transform_does_not_modify_raw_source_geometries(self):
        folder = self.data["root"] / "PSR_Volatile_Estimates"
        _, source_geometries, source_crs = _read_layer(folder, "PSR_volatile_abundance_final")
        source_bounds = [g.bounds for g in source_geometries]
        transformer = Transformer.from_crs(source_crs, self.data["display_crs"], always_xy=True)
        transformed = _transform_geometries(source_geometries, transformer)
        self.assertEqual([g.bounds for g in source_geometries], source_bounds)
        self.assertTrue(all(src is not dst for src, dst in zip(source_geometries, transformed)))
        self.assertEqual(len(transformed), 141)

    def test_transform_preserves_z_dimension(self):
        from shapely.geometry import Polygon
        source = Polygon([(0, 0, 7), (1, 0, 8), (1, 1, 9), (0, 0, 7)])
        same_crs = CRS.from_epsg(4326)
        transformer = Transformer.from_crs(same_crs, same_crs, always_xy=True)
        result = _transform_geometries([source], transformer)[0]
        self.assertTrue(result.has_z)
        self.assertEqual([coord[2] for coord in result.exterior.coords], [7, 8, 9, 7])

    def test_default_selection_is_first_source_order_overlap(self):
        area_i = candidates(self.data)[0]
        rows = overlap_summary(self.data, area_i)
        expected = min(r["source_record"] for r in rows) - 1
        selected = default_psr_record(self.data, area_i)
        self.assertEqual(selected, expected)
        self.assertIn(self.data["psr_source_records"][selected],
                      {r["source_record"] for r in rows})
        self.assertEqual(len(rows), 5)

    def test_duplicate_ids_have_unique_source_record_labels(self):
        ids = [a["Id_1"] for a in self.data["psr_attrs"]]
        duplicate_id = next(value for value in ids if ids.count(value) > 1)
        indexes = [i for i, value in enumerate(ids) if value == duplicate_id]
        labels = [f"Record {self.data['psr_source_records'][i]} | Id_1={ids[i]}"
                  for i in indexes]
        self.assertGreater(len(indexes), 1)
        self.assertEqual(len(labels), len(set(labels)))

    def test_source_record_numbers_survive_ordering(self):
        area_i = candidates(self.data)[0]
        order = ordered_psr_records(self.data, area_i)
        self.assertEqual(sorted(self.data["psr_source_records"][i] for i in order),
                         list(range(1, 142)))
        overlap_records = {r["source_record"] for r in overlap_summary(self.data, area_i)}
        self.assertEqual([self.data["psr_source_records"][i] for i in order[:5]],
                         sorted(overlap_records))

    def test_viewport_uses_area_bounds_without_mutating_geometry_or_overlap(self):
        area_i = candidates(self.data)[0]
        geometry = self.data["area_geoms"][area_i]
        before_bounds = geometry.bounds
        before_overlaps = overlap_summary(self.data, area_i)
        xmin, xmax, ymin, ymax = viewport_bounds(geometry, 0.1)
        x0, y0, x1, y1 = before_bounds
        self.assertAlmostEqual(xmin, x0 - (x1 - x0) * 0.1)
        self.assertAlmostEqual(xmax, x1 + (x1 - x0) * 0.1)
        self.assertAlmostEqual(ymin, y0 - (y1 - y0) * 0.1)
        self.assertAlmostEqual(ymax, y1 + (y1 - y0) * 0.1)
        self.assertEqual(geometry.bounds, before_bounds)
        self.assertEqual(overlap_summary(self.data, area_i), before_overlaps)

    def test_pns02_point_is_uniquely_named_and_inside_area(self):
        area_i = candidates(self.data)[0]
        matches = pns02_site_candidates(self.data, area_i)
        self.assertEqual(len(matches), 1)
        point_i = matches[0]
        self.assertEqual(self.data["site_attrs"][point_i]["Name"], "PNS02")
        self.assertTrue(self.data["area_geoms"][area_i].covers(self.data["site_geoms"][point_i]))

    def test_all_five_overlap_ids_and_feature_count_remain(self):
        self.assertEqual(len(self.data["psr_geoms"]), 141)
        rows = overlap_summary(self.data, candidates(self.data)[0])
        self.assertEqual({int(r["Id_1"]) for r in rows}, {324, 325, 330, 335, 338})

    def test_missing_shapefile_components_are_actionable(self):
        source = self.data["root"] / "PSR_Volatile_Estimates"
        for suffix in (".shp", ".shx", ".dbf", ".prj"):
            with self.subTest(missing=suffix), tempfile.TemporaryDirectory() as temp:
                dest = Path(temp) / "PSR_Volatile_Estimates"
                shutil.copytree(source, dest)
                (dest / f"PSR_volatile_abundance_final{suffix}").unlink()
                with self.assertRaisesRegex(FileNotFoundError, suffix.replace(".", r"\.")):
                    _read_layer(dest, "PSR_volatile_abundance_final")

    def test_pns02_candidate_must_be_unique(self):
        unique = {"area_attrs": [{"Name": "PNS02"}]}
        self.assertEqual(unique_candidate(unique), 0)
        with self.assertRaisesRegex(ValueError, "No exploration-area feature"):
            unique_candidate({"area_attrs": [{"Name": "PNS01"}]})
        with self.assertRaisesRegex(ValueError, "select one explicitly"):
            unique_candidate({"area_attrs": [{"Name": "PNS02"}, {"Name": "PNS02"}]})

    def test_no_overlap_is_empty_and_does_not_create_default(self):
        area_i = candidates(self.data)[0]
        no_overlap = dict(self.data)
        no_overlap["psr_geoms"] = [box(1e7, 1e7, 1e7 + 1, 1e7 + 1) for _ in self.data["psr_geoms"]]
        self.assertEqual(overlap_summary(no_overlap, area_i), [])
        with self.assertRaisesRegex(ValueError, "No positive-area PSR overlap"):
            default_psr_record(no_overlap, area_i)

    def test_duplicate_ids_keep_distinct_selector_identifiers(self):
        ids = [a["Id_1"] for a in self.data["psr_attrs"]]
        duplicate = next(value for value in ids if ids.count(value) > 1)
        indexes = [i for i, value in enumerate(ids) if value == duplicate]
        labels = [default_selection_label(self.data, i) for i in indexes]
        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual([self.data["psr_source_records"][i] for i in indexes],
                         sorted(self.data["psr_source_records"][i] for i in indexes))


if __name__ == "__main__":
    unittest.main()
