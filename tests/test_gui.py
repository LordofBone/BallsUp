import csv
import importlib.util
import io
import unittest
from pathlib import Path

if importlib.util.find_spec("streamlit") is not None:
    from streamlit.testing.v1 import AppTest

    from app import make_chart, results_csv


@unittest.skipUnless(importlib.util.find_spec("streamlit") is not None, "GUI dependencies are not installed")
class TestDashboard(unittest.TestCase):
    def test_simulation_displays_results(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        self.assertFalse(dashboard.exception)

        dashboard.number_input[0].set_value(1)
        dashboard.button[0].click()
        dashboard.run(timeout=30)

        self.assertFalse(dashboard.exception)
        self.assertEqual(4, len(dashboard.metric))
        self.assertEqual(5, len(dashboard.tabs))
        self.assertEqual(100, len(dashboard.dataframe[0].value))

    def test_csv_and_chart_keep_zero_break_floors(self):
        results = {
            1: {"attempts": 0, "breaks": 0, "starting_breaks": 0,
                "average_attempts": 0.0, "break_percentage": 0.0},
            2: {"attempts": 2, "breaks": 1, "starting_breaks": 1,
                "average_attempts": 2.0, "break_percentage": 100.0},
        }
        rows = list(csv.DictReader(io.StringIO(results_csv(results))))
        self.assertEqual("inf", rows[0]["efficiency_score"])
        self.assertEqual("0.02", rows[1]["efficiency_score"])
        figure = make_chart(results, "breaks", "Breaks", "Count", "#34d399", 2, bar=True)
        self.assertEqual(1, len(figure.axes))


if __name__ == "__main__":
    unittest.main()
