import unittest

from src.earth_analog_evidence import (
    DIMENSIONS,
    EARTH_ANALOGS,
    STATUS,
    validate_evidence_records,
)


class EarthAnalogEvidenceTests(unittest.TestCase):
    def test_each_candidate_has_purpose_verifiable_source_limitations_and_dimensions(self):
        validate_evidence_records()
        self.assertEqual(len(EARTH_ANALOGS), 5)
        for candidate in EARTH_ANALOGS:
            with self.subTest(candidate=candidate["id"]):
                self.assertTrue(candidate["purpose"].strip())
                self.assertTrue(candidate["sources"])
                self.assertTrue(any(source["url"].startswith("https://") for source in candidate["sources"]))
                self.assertTrue(candidate["limitations"])
                self.assertTrue(all(item.strip() for item in candidate["limitations"]))
                self.assertTrue(candidate["dimensions"])
                self.assertTrue(set(candidate["dimensions"]).issubset(DIMENSIONS))
                self.assertIn(STATUS, candidate.get("status", STATUS))

    def test_records_do_not_define_a_score_or_ranking(self):
        forbidden = {"score", "similarity_score", "rank", "ranking"}
        for candidate in EARTH_ANALOGS:
            with self.subTest(candidate=candidate["id"]):
                self.assertTrue(forbidden.isdisjoint(candidate))

    def test_lake_bonney_is_a_separate_supporting_extension(self):
        mcmurdo = next(candidate for candidate in EARTH_ANALOGS if candidate["id"] == "mcmurdo")
        extension = mcmurdo["supporting_extension"]
        self.assertEqual(extension["name"], "West Lake Bonney (separate sub-ice research extension)")
        self.assertIn("not interchangeable", extension["limitation"])
        self.assertIn("McMurdo Dry Valleys", mcmurdo["name"])


if __name__ == "__main__":
    unittest.main()
