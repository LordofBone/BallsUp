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
        with patch("dashboard_simulation.run_simulation_by_strategy") as simulate:
            with self.assertRaisesRegex(ValueError, "up to 750 iterations"):
                run_dashboard_simulation(751, ranges, ["Linear search"])
            simulate.assert_not_called()
            run_dashboard_simulation(751, ranges, ["Binary search"])
            simulate.assert_called_once_with(751, *ranges, {"Binary search": STRATEGIES["Binary search"][0]})

    def test_occupied_slot_rejects_work_before_simulation(self):
        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        selected = list(STRATEGIES)

        def active_simulation(*args):
            with self.assertRaises(SimulationBusyError):
                run_dashboard_simulation(1, ranges, selected)
            return {}

        with patch("dashboard_simulation.run_simulation_by_strategy",
                   side_effect=active_simulation) as simulate:
            run_dashboard_simulation(1, ranges, selected)
            simulate.assert_called_once()

    def test_simulator_failure_releases_slot(self):
        ranges = ((0.5, 1.5), (4000, 7000), (1, 3))
        with patch("dashboard_simulation.run_simulation_by_strategy") as simulate:
            simulate.side_effect = [RuntimeError("failed"), {}]
            with self.assertRaisesRegex(RuntimeError, "failed"):
                run_dashboard_simulation(500, ranges, list(STRATEGIES))
            self.assertEqual({}, run_dashboard_simulation(500, ranges, list(STRATEGIES)))
            self.assertEqual(2, simulate.call_count)


@unittest.skipUnless(importlib.util.find_spec("streamlit") is not None, "GUI dependencies are not installed")
class TestDashboard(unittest.TestCase):
    def test_caption_mean_for_large_finite_plate_strengths(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        dashboard.number_input[0].set_value(1)
        dashboard.multiselect[0].set_value(["Binary search"])
        strengths = {"Minimum strength": 1e308, "Maximum strength": 1.6e308}
        for widget in dashboard.number_input:
            if widget.label in strengths:
                widget.set_value(strengths[widget.label])
        dashboard.button[0].click().run()

        self.assertFalse(dashboard.exception)
        self.assertFalse(dashboard.error)
        self.assertTrue(any("mean plate strength 1.3e+308 N" in caption.value
                            for caption in dashboard.caption), [caption.value for caption in dashboard.caption])

    def test_excess_work_is_rejected_before_simulation(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        dashboard.number_input[0].set_value(501)
        dashboard.button[0].click()
        with patch("dashboard_simulation.run_simulation_by_strategy") as simulate:
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
        with patch("dashboard_simulation.run_simulation_by_strategy",
                   side_effect=active_simulation) as simulate:
            run_dashboard_simulation(1, ranges, list(STRATEGIES))
            simulate.assert_called_once()
        self.assertFalse(dashboard.exception)
        self.assertIn("server is busy", dashboard.warning[0].value)

    def test_simulation_compares_strategies_on_shared_inputs(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        self.assertFalse(dashboard.exception)

        dashboard.multiselect[0].set_value(["Linear search", "Binary search"])
        # The first draw breaks at floor 51. The second never breaks.
        draws = [1.0] * 100 + [1.0, 3150.0] + [2.0] * 100 + [0.5, 7000.0]
        dashboard.number_input[0].set_value(2)
        dashboard.button[0].click()
        with patch("run.random.uniform", side_effect=draws) as uniform:
            dashboard.run(timeout=30)

        self.assertEqual(len(draws), uniform.call_count)

        self.assertFalse(dashboard.exception)
        self.assertEqual(["Linear search", "Binary search"],
                         [tab.label for tab in dashboard.tabs if tab.label in STRATEGIES])
        self.assertEqual(2, len(dashboard.dataframe))
        for table, attempts in zip(dashboard.dataframe, (11, 7)):
            self.assertEqual(100, len(table.value))
            rows = table.value.set_index("floor")
            self.assertEqual(0, rows.loc[1, "starting_breaks"])
            self.assertEqual(float("inf"), rows.loc[1, "efficiency_score"])
            self.assertEqual(100, rows.loc[51, "breaks"])
            self.assertEqual(1, rows.loc[60, "starting_breaks"])
            self.assertEqual(50.0, rows.loc[60, "break_percentage"])
            self.assertEqual(attempts, rows.loc[60, "attempts"])
            self.assertEqual(attempts / 2, rows.loc[60, "average_attempts"])
            self.assertAlmostEqual(attempts / 100, rows.loc[60, "efficiency_score"])

    def test_csv_and_chart_keep_zero_break_floors(self):
        results = {
            1: {"attempts": 0, "breaks": 0, "starting_breaks": 0,
                "average_attempts": 0.0, "break_percentage": 0.0},
            2: {"attempts": 2, "breaks": 1, "starting_breaks": 1,
                "average_attempts": 2.0, "break_percentage": 100.0},
        }
        rows = list(csv.DictReader(io.StringIO(results_csv(results, "Linear search"))))
        self.assertEqual("Linear search", rows[0]["strategy"])
        self.assertEqual("inf", rows[0]["efficiency_score"])
        self.assertEqual("0.02", rows[1]["efficiency_score"])
        figure = make_chart(results, "breaks", "Breaks", "Count", "#34d399", 2, bar=True)
        self.assertEqual(1, len(figure.axes))

    def test_zero_break_run_has_no_qualifying_floor(self):
        dashboard = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        dashboard.number_input[0].set_value(1)
        dashboard.number_input[1].set_value(0.001)
        dashboard.number_input[2].set_value(0.001)
        dashboard.number_input[4].set_value(4000.0)
        dashboard.number_input[6].set_value(1.0)
        dashboard.multiselect[0].set_value(["Linear search"])
        dashboard.button[0].click()

        with patch("streamlit.pyplot") as pyplot:
            dashboard.run()

        self.assertFalse(dashboard.exception)
        self.assertFalse(dashboard.error)
        self.assertEqual("No qualifying floor", dashboard.metric[0].value)
        self.assertEqual("∞", dashboard.metric[1].value)
        self.assertEqual("0", dashboard.metric[3].value)
        self.assertEqual(4, pyplot.call_count)
        for chart, expected_lines in zip(pyplot.call_args_list, (1, 1, 0, 1)):
            axes = chart.args[0].axes[0]
            with self.subTest(chart=axes.get_title(loc="left")):
                self.assertIsNone(axes.get_legend())
                self.assertEqual(expected_lines, len(axes.lines))


if __name__ == "__main__":
    unittest.main()
