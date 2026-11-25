import csv
import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from dashboard_simulation import STRATEGIES, SimulationBusyError, run_dashboard_simulation

if importlib.util.find_spec("streamlit") is not None:
    from streamlit.testing.v1 import AppTest

    from app import make_chart, results_csv


class TestDashboardWorkBudget(unittest.TestCase):
    def test_strategy_selection_changes_iteration_limit(self):
        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        with patch("dashboard_simulation.run_simulation_with_adjusted_parameters") as simulate:
            with self.assertRaisesRegex(ValueError, "up to 750 iterations"):
                run_dashboard_simulation(751, ranges, ["Linear search"])
            simulate.assert_not_called()
            run_dashboard_simulation(751, ranges, ["Binary search"])
            simulate.assert_called_once_with(751, *ranges, (STRATEGIES["Binary search"][0],))

    def test_occupied_slot_rejects_work_before_simulation(self):
        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        selected = list(STRATEGIES)

        def active_simulation(*args):
            with self.assertRaises(SimulationBusyError):
                run_dashboard_simulation(1, ranges, selected)
            return {}

        with patch("dashboard_simulation.run_simulation_with_adjusted_parameters",
                   side_effect=active_simulation) as simulate:
            run_dashboard_simulation(1, ranges, selected)
            simulate.assert_called_once()

    def test_simulator_failure_releases_slot(self):
        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        with patch("dashboard_simulation.run_simulation_with_adjusted_parameters") as simulate:
            simulate.side_effect = [RuntimeError("failed"), {}]
            with self.assertRaisesRegex(RuntimeError, "failed"):
                run_dashboard_simulation(500, ranges, list(STRATEGIES))
            self.assertEqual({}, run_dashboard_simulation(500, ranges, list(STRATEGIES)))
            self.assertEqual(2, simulate.call_count)


@unittest.skipUnless(importlib.util.find_spec("streamlit") is not None, "GUI dependencies are not installed")
class TestDashboard(unittest.TestCase):
    def test_excess_work_is_rejected_before_simulation(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        dashboard.number_input[0].set_value(501)
        dashboard.button[0].click()
        with patch("dashboard_simulation.run_simulation_with_adjusted_parameters") as simulate:
            dashboard.run()
            simulate.assert_not_called()
        self.assertFalse(dashboard.exception)
        self.assertIn("up to 500 iterations", dashboard.error[0].value)

    def test_busy_dashboard_rejects_second_simulation(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        dashboard.button[0].click()

        def active_simulation(*args):
            dashboard.run()
            return {}

        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        with patch("dashboard_simulation.run_simulation_with_adjusted_parameters",
                   side_effect=active_simulation) as simulate:
            run_dashboard_simulation(1, ranges, list(STRATEGIES))
            simulate.assert_called_once()
        self.assertFalse(dashboard.exception)
        self.assertIn("server is busy", dashboard.warning[0].value)

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
