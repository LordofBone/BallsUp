import unittest

from run import calculate_impact_force, linear_search_simulation_with_flag, \
    precise_halving_strategy_simulation_with_flag, binary_search_strategy, find_most_efficient_floor_from_results, \
    cumulative_height, run_simulation_with_adjusted_parameters, find_floor_with_most_breaks


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

    def test_linear_search_simulation_with_flag_low_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons
        start_floor = 50

        expected_attempts = 51
        expected_did_break = True
        expected_break_floor = 1
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_precise_halving_strategy_simulation_with_flag_low_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons
        start_floor = 50

        expected_attempts = 7
        expected_did_break = True
        expected_break_floor = 1
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor)
                         )

    def test_binary_search_strategy_low_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons
        start_floor = 50

        expected_attempts = 50
        expected_did_break = True
        expected_break_floor = 1
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_linear_search_simulation_with_flag_mid_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons
        start_floor = 50

        expected_attempts = 2
        expected_did_break = True
        expected_break_floor = 50
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_precise_halving_strategy_simulation_with_flag_mid_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons
        start_floor = 50

        expected_attempts = 7
        expected_did_break = True
        expected_break_floor = 50
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor)
                         )

    def test_binary_search_strategy_mid_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons
        start_floor = 50

        expected_attempts = 2
        expected_did_break = True
        expected_break_floor = 50
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_linear_search_simulation_with_flag_high_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 51
        expected_did_break = True
        expected_break_floor = 100
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_precise_halving_strategy_simulation_with_flag_high_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 7
        expected_did_break = True
        expected_break_floor = 100
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor)
                         )

    def test_binary_search_strategy_high_break(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 7
        expected_did_break = True
        expected_break_floor = 100
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_linear_search_simulation_with_flag_consistent_break_floor_low(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons

        expected_did_break = True
        expected_break_floor = 1

        for floor in range(1, 101):
            attempts, did_break, break_floor = linear_search_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_precise_halving_strategy_simulation_with_flag_consistent_break_floor_low(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons

        expected_did_break = True
        expected_break_floor = 1

        for floor in range(1, 101):
            attempts, did_break, break_floor = precise_halving_strategy_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_binary_search_strategy_consistent_break_floor_low(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.91  # 0.91 kg
        plate_strength = 4  # Can withstand a force of 4 Newtons

        expected_did_break = True
        expected_break_floor = 1

        for floor in range(1, 101):
            attempts, did_break, break_floor = binary_search_strategy(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_linear_search_simulation_with_flag_consistent_break_floor_mid(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons

        expected_did_break = True
        expected_break_floor = 50

        for floor in range(1, 101):
            attempts, did_break, break_floor = linear_search_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_precise_halving_strategy_simulation_with_flag_consistent_break_floor_mid(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons

        expected_did_break = True
        expected_break_floor = 50

        for floor in range(1, 101):
            attempts, did_break, break_floor = precise_halving_strategy_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_binary_search_strategy_consistent_break_floor_mid(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 1  # 1 kg
        plate_strength = 31  # Can withstand a force of 31 Newtons

        expected_did_break = True
        expected_break_floor = 50

        for floor in range(1, 101):
            attempts, did_break, break_floor = binary_search_strategy(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_linear_search_simulation_with_flag_consistent_break_floor_high(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons

        expected_did_break = True
        expected_break_floor = 100

        for floor in range(1, 101):
            attempts, did_break, break_floor = linear_search_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_precise_halving_strategy_simulation_with_flag_consistent_break_floor_high(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons

        expected_did_break = True
        expected_break_floor = 100

        for floor in range(1, 101):
            attempts, did_break, break_floor = precise_halving_strategy_simulation_with_flag(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_binary_search_strategy_consistent_break_floor_high(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.994  # 0.994 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons

        expected_did_break = True
        expected_break_floor = 100

        for floor in range(1, 101):
            attempts, did_break, break_floor = binary_search_strategy(
                floor_heights, ball_weight, plate_strength, floor)

            # Check if the break floor is as expected
            self.assertEqual(expected_break_floor, break_floor)

            # Check if the ball did break
            self.assertEqual(expected_did_break, did_break)

    def test_linear_search_simulation_with_flag_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.993  # 0.993 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_precise_halving_strategy_simulation_with_flag_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.993  # 0.993 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength,
                                                                       start_floor)
                         )

    def test_binary_search_strategy_no_possible_break_skip(self):
        # Set up a test case
        floor_heights = [1 for _ in range(100)]  # All floors are 1 meter high
        ball_weight = 0.993  # 0.993 kg
        plate_strength = 44  # Can withstand a force of 44 Newtons
        start_floor = 50

        expected_attempts = 0
        expected_did_break = False
        expected_break_floor = None
        self.assertEqual((expected_attempts, expected_did_break, expected_break_floor),
                         binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor)
                         )

    def test_find_most_efficient_floor_from_results(self):
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

        self.assertEqual((expected_floor, expected_efficiency_score),
                         find_most_efficient_floor_from_results(simulation_results)
                         )

    def test_full_simulation_low(self):
        # Set up a test case
        num_iterations = 1  # Number of iterations
        ball_weight_range = (0.91, 0.91)  # Ball weight
        plate_strength_range = (4, 4)  # Plate strength
        floor_height_range = (1, 1)  # Floor height

        # List of strategies
        strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                      binary_search_strategy]

        # Run the simulation
        simulation_results = run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range,
                                                                     plate_strength_range,
                                                                     floor_height_range, strategies)

        # Calculate the floor with the most breaks and its number of breaks
        most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)

        # Calculate the most efficient floor and its efficiency score
        most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)

        self.assertEqual(1, most_breaks_floor)
        self.assertEqual(300, most_breaks)
        self.assertEqual(1, most_efficient_floor)
        self.assertEqual(0.6012777777777779, efficiency_score)

    def test_full_simulation_mid(self):
        # Set up a test case
        num_iterations = 1  # Number of iterations
        ball_weight_range = (1, 1)  # Ball weight
        plate_strength_range = (31, 31)  # Plate strength
        floor_height_range = (1, 1)  # Floor height

        # List of strategies
        strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                      binary_search_strategy]

        # Run the simulation
        simulation_results = run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range,
                                                                     plate_strength_range,
                                                                     floor_height_range, strategies)

        # Calculate the floor with the most breaks and its number of breaks
        most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)

        # Calculate the most efficient floor and its efficiency score
        most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)

        self.assertEqual(50, most_breaks_floor)
        self.assertEqual(300, most_breaks)
        self.assertEqual(50, most_efficient_floor)
        self.assertEqual(0.6251666666666666, efficiency_score)

    def test_full_simulation_high(self):
        # Set up a test case
        num_iterations = 1  # Number of iterations
        ball_weight_range = (0.994, 0.994)  # Ball weight
        plate_strength_range = (44, 44)  # Plate strength
        floor_height_range = (1, 1)  # Floor height

        # List of strategies
        strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                      binary_search_strategy]

        # Run the simulation
        simulation_results = run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range,
                                                                     plate_strength_range,
                                                                     floor_height_range, strategies)

        # Calculate the floor with the most breaks and its number of breaks
        most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)

        # Calculate the most efficient floor and its efficiency score
        most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)

        self.assertEqual(100, most_breaks_floor)
        self.assertEqual(300, most_breaks)
        self.assertEqual(100, most_efficient_floor)
        self.assertEqual(0.8539999999999999, efficiency_score)

    def test_full_simulation_no_break(self):
        # Set up a test case
        num_iterations = 1  # Number of iterations
        ball_weight_range = (0.993, 0.993)  # Ball weight
        plate_strength_range = (44, 44)  # Plate strength
        floor_height_range = (1, 1)  # Floor height

        # List of strategies
        strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                      binary_search_strategy]

        # Run the simulation
        simulation_results = run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range,
                                                                     plate_strength_range,
                                                                     floor_height_range, strategies)

        # Calculate the floor with the most breaks and its number of breaks
        most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)

        # Calculate the most efficient floor and its efficiency score
        most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)

        self.assertEqual(None, most_breaks_floor)
        self.assertEqual(0, most_breaks)
        self.assertEqual(1, most_efficient_floor)
        self.assertEqual(float('inf'), efficiency_score)


if __name__ == '__main__':
    unittest.main()
