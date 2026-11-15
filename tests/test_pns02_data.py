import unittest
from pathlib import Path

from src.pns02_data import candidates, load_pns02_data, overlap_summary


class PNS02DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_pns02_data()

    def test_loads_source_feature_counts_and_crs(self):
        self.assertEqual(len(self.data["psr_geoms"]), 141)
        self.assertEqual(self.data["display_crs"].name, "Moon2000_spole")
        self.assertTrue(self.data["transformed"])

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


if __name__ == "__main__":
    unittest.main()
