import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from driftdetect import core


def row(source, key, value):
    return {"source": source, "key": key, "value": value}


class DriftdetectTest(unittest.TestCase):
    def test_empty_rows(self):
        self.assertEqual(core.detect([], ["dev"], core.Counter()), {})

    def test_single_source_no_drift(self):
        table = core.detect([row("dev", "a", "1")], ["dev"], core.Counter())
        self.assertEqual(table, {})

    def test_same_value_no_drift(self):
        rows = [row("dev", "a", "1"), row("staging", "a", "1")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        self.assertEqual(table, {})

    def test_different_value_drifts(self):
        rows = [row("dev", "a", "1"), row("staging", "a", "2")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        self.assertIn("a", table)

    def test_table_maps_sources(self):
        rows = [row("dev", "a", "1"), row("staging", "a", "2")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        self.assertIn("dev", table["a"])
        self.assertIn("staging", table["a"])

    def test_render_has_summary(self):
        rows = [row("dev", "a", "1"), row("staging", "a", "2")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        self.assertIn("drift=", core.render(table, ["dev", "staging"]))


if __name__ == "__main__":
    unittest.main()
