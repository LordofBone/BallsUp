import unittest

from run import calculate_impact_force, linear_search_simulation_with_flag, \
    precise_halving_strategy_simulation_with_flag, binary_search_strategy, find_most_efficient_floor_from_results, \
    cumulative_height


class TestBallDropSimulation(unittest.TestCase):

    def test_calculate_impact_force(self):
        # Test with known values
        self.assertAlmostEqual(calculate_impact_force(10, 1), 14.0,
                               places=2)

    def test_cumulative_height(self):
        floor_heights = [0.1, 1.2, 5, 7.1, 10]

        # Test with known values
        self.assertAlmostEqual(cumulative_height(floor_heights, 5), 23.4,
                               places=2)

    def test_linear_search_simulation_with_flag(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 46
        expected_did_break = True
        expected_break_floor = 6
        self.assertEqual(linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_precise_halving_strategy_simulation_with_flag(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 6
        expected_did_break = True
        expected_break_floor = 5
        self.assertEqual(precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_binary_search_strategy(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 46
        expected_did_break = True
        expected_break_floor = 6
        self.assertEqual(binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_linear_search_simulation_with_flag_consistent_break_floor(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons

        expected_did_break = True
        expected_break_floor = 6

        for floor in range(1, 101):
            attempts, did_break, break_floor = linear_search_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(break_floor, expected_break_floor)

            # Check if the ball did break
            self.assertEqual(did_break, expected_did_break)

    def test_precise_halving_strategy_simulation_with_flag_consistent_break_floor(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons

        expected_did_break = True
        expected_break_floor = 6

        for floor in range(1, 101):
            attempts, did_break, break_floor = precise_halving_strategy_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(break_floor, expected_break_floor)

            # Check if the ball did break
            self.assertEqual(did_break, expected_did_break)

    def test_binary_search_strategy_consistent_break_floor(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10  # Can withstand a force of 10 Newtons

        expected_did_break = True
        expected_break_floor = 6

        for floor in range(1, 101):
            attempts, did_break, break_floor = binary_search_strategy(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(break_floor, expected_break_floor)

            # Check if the ball did break
            self.assertEqual(did_break, expected_did_break)

    def test_linear_search_simulation_with_flag_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10000  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual(linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_precise_halving_strategy_simulation_with_flag_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10000  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual(precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_binary_search_strategy_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 10000  # Can withstand a force of 10 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual(binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor),
                         (expected_attempts, expected_did_break, expected_break_floor))

    def test_find_most_efficient_floor_from_results_no_possible_break_skip(self):
        simulation_results = \
            {1: {'attempts': 7465,
                 'average_attempts': 7.465,
                 'break_percentage': 56.8,
                 'breaks': 568},
             2: {'attempts': 7346,
                 'average_attempts': 7.346,
                 'break_percentage': 56.8,
                 'breaks': 568},
             3: {'attempts': 7323,
                 'average_attempts': 7.323,
                 'break_percentage': 56.8,
                 'breaks': 568},
             4: {'attempts': 7309,
                 'average_attempts': 7.309,
                 'break_percentage': 56.8,
                 'breaks': 568},
             5: {'attempts': 7389,
                 'average_attempts': 7.389,
                 'break_percentage': 56.49999999999999,
                 'breaks': 565},
             6: {'attempts': 7418,
                 'average_attempts': 7.418,
                 'break_percentage': 56.49999999999999,
                 'breaks': 565},
             7: {'attempts': 7474,
                 'average_attempts': 7.474,
                 'break_percentage': 56.49999999999999,
                 'breaks': 565},
             8: {'attempts': 7525,
                 'average_attempts': 7.525,
                 'break_percentage': 56.49999999999999,
                 'breaks': 565},
             9: {'attempts': 7633,
                 'average_attempts': 7.633,
                 'break_percentage': 56.49999999999999,
                 'breaks': 565},
             10: {'attempts': 7726,
                  'average_attempts': 7.726,
                  'break_percentage': 56.49999999999999,
                  'breaks': 565}}

        expected_floor = 4
        expected_efficiency_score = 0.12867957746478875

        self.assertEqual(find_most_efficient_floor_from_results(simulation_results),
                         (expected_floor, expected_efficiency_score))


if __name__ == '__main__':
    unittest.main()
