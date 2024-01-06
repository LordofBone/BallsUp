import argparse
import logging
import math
import random
from pprint import pprint

import matplotlib

matplotlib.use('Qt5Agg')  # Or another backend like 'GTK3Agg', 'WXAgg', etc.
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_impact_force(height, weight):
    """
    Calculate the impact force of the ball.
    :param height: Drop height in meters.
    :param weight: Weight of the ball in kg.
    :return: Impact force in Newtons.
    """
    g = 9.8  # Gravity in m/s^2
    velocity = math.sqrt(2 * g * height)
    force = weight * velocity
    logging.debug(f"Calculated impact force: Height = {height} m, Weight = {weight} kg, Force = {force} N")
    return force


def cumulative_height(floor_heights, floor):
    """
    Calculate the cumulative height up to a given floor.
    :param floor_heights: List of heights for each floor.
    :param floor: Target floor number.
    :return: Cumulative height up to the given floor.
    """
    cumulative_height_calc = sum(floor_heights[:floor])
    logging.debug(f"Cumulative height calculated up to floor {floor}: {cumulative_height_calc} m")
    return cumulative_height_calc


def linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply a linear search strategy to find the minimum breaking floor from a given start floor.
    :param floor_heights: Heights of each floor.
    :param ball_weight: Weight of the ball.
    :param plate_strength: Strength of the plate.
    :param start_floor: Starting floor for the simulation.
    :return: Number of attempts to find the minimum breaking floor and a flag indicating if a break occurred.
    """
    logging.debug(f"Starting Linear Search Strategy from floor {start_floor}")

    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        logging.debug("Maximum force doesn't break the plate. Exiting early.")
        return attempts, did_break, breaking_floor

    floor = start_floor

    # Initially check if the plate breaks or not at the starting floor
    current_force = calculate_impact_force(cumulative_height(floor_heights, floor), ball_weight)
    initial_break = current_force > plate_strength
    attempts += 1

    if initial_break:
        # If it breaks, go down to find the minimum breaking floor
        logging.debug("Initial break detected. Searching downwards for minimum breaking floor.")
        while floor > 0:
            attempts += 1
            floor -= 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, floor), ball_weight)

            if current_force <= plate_strength:
                # Found the floor just before it stops breaking
                did_break = True
                floor += 1
                breaking_floor = floor
                break
    else:
        # If it doesn't break, go up to find the breaking floor
        logging.debug("No initial break. Searching upwards for breaking floor.")
        while floor < 100:

            attempts += 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, floor + 1), ball_weight)
            floor += 1
            if current_force > plate_strength:
                breaking_floor = floor
                did_break = True
                # Found the breaking floor
                break

    logging.debug(
        f"Linear Search Result: {attempts} attempts, Break occurred: {did_break}, Breaking floor: {breaking_floor}")
    return attempts, did_break, breaking_floor


def precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply the precise halving strategy to find the minimum breaking floor from a given start floor.
    :param floor_heights:
    :param ball_weight:
    :param plate_strength:
    :param start_floor:
    :return:
    """
    logging.debug(f"Starting Precise Halving Strategy from floor {start_floor}")

    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        logging.debug("Maximum force doesn't break the plate. Exiting early.")
        return attempts, did_break, breaking_floor

    # Set initial high and low bounds for halving
    low = 0
    high = len(floor_heights)
    floor = start_floor

    # Halving strategy
    while low < high:
        attempts += 1
        current_force = calculate_impact_force(cumulative_height(floor_heights, floor), ball_weight)

        if current_force > plate_strength:
            # If current force breaks the plate, decrease the high bound and set breaking_floor
            high = floor - 1
            did_break = True
            breaking_floor = floor  # Set breaking_floor to the current floor
        else:
            # If current force doesn't break the plate, increase the low bound
            low = floor + 1

        # Update the floor based on new high and low
        floor = (low + high) // 2

        logging.debug(f"Current floor: {floor}, Low bound: {low}, High bound: {high}")

    # Check the floor if low and high have converged
    if low == high:
        attempts += 1
        current_force = calculate_impact_force(cumulative_height(floor_heights, low), ball_weight)
        if current_force > plate_strength:
            did_break = True
            breaking_floor = low

    # If the halving strategy did not find a breaking floor, perform a linear search upwards
    if not did_break:
        logging.debug("No break found in halving strategy. Switching to linear search upwards.")
        for f in range(start_floor, len(floor_heights)):
            current_force = calculate_impact_force(cumulative_height(floor_heights, f), ball_weight)
            attempts += 1
            if current_force > plate_strength:
                did_break = True
                breaking_floor = f
                break

    logging.debug(
        f"Precise Halving Strategy Result: {attempts} attempts, Break occurred: {did_break}, "
        f"Breaking floor: {breaking_floor}")
    return attempts, did_break, breaking_floor


def binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply the binary search strategy to find the minimum breaking floor.
    :param floor_heights:
    :param ball_weight:
    :param plate_strength:
    :param start_floor:
    :return:
    """
    logging.debug(f"Starting Binary Search Strategy from floor {start_floor}")

    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        logging.debug("Maximum force doesn't break the plate. Exiting early.")
        return attempts, did_break, breaking_floor

    low = 0
    high = len(floor_heights)
    attempts = 0
    did_break = False
    breaking_floor = None

    # Check if the starting floor breaks the plate
    current_force = calculate_impact_force(cumulative_height(floor_heights, start_floor), ball_weight)
    attempts += 1
    if current_force > plate_strength:
        did_break = True
        breaking_floor = start_floor
        # Since the plate broke at the starting floor, search downwards for the actual breaking floor
        while breaking_floor > 1:
            logging.debug(f"Searching between floors {low} and {high}, Current floor: {breaking_floor}")
            breaking_floor -= 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, breaking_floor), ball_weight)
            attempts += 1
            if current_force <= plate_strength:
                breaking_floor += 1
                # Found the actual breaking floor
                break
    else:
        # If the plate does not break at the starting floor, perform binary search upwards
        low = start_floor + 1
        while low <= high:
            logging.debug(f"Searching between floors {low} and {high}")
            mid = (low + high) // 2
            attempts += 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, mid), ball_weight)

            if current_force > plate_strength:
                did_break = True
                breaking_floor = mid
                high = mid - 1
            else:
                low = mid + 1

    logging.debug(
        f"Binary Search Result: {attempts} attempts, Break occurred: {did_break}, Breaking floor: {breaking_floor}")
    return attempts, did_break, breaking_floor


def run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range, plate_strength_range, floor_height_range,
                                            strategy_roster):
    """
    Run simulations with a dynamic number of strategies.
    :param num_iterations: Number of iterations to run the simulation.
    :param ball_weight_range: Tuple representing the range of ball weight in kg.
    :param plate_strength_range: Tuple representing the range of plate strength in Newtons.
    :param floor_height_range: Tuple representing the range of floor heights in meters.
    :param strategy_roster: List of strategy functions to use in the simulation.
    :return: Aggregated results for each starting floor and each strategy.
    """
    aggregated_results = {floor: {'attempts': 0, 'breaks': 0} for floor in range(1, 101)}
    break_results = {floor: {'breaks': 0} for floor in range(1, 101)}
    total_strategy_executions = num_iterations * len(strategy_roster)

    for _ in range(num_iterations):
        floor_heights = [random.uniform(*floor_height_range) for _ in range(100)]
        ball_weight = random.uniform(*ball_weight_range)
        plate_strength = random.uniform(*plate_strength_range)

        for floor in range(1, 101):
            for strategy in strategy_roster:
                attempts, did_break, breaking_floor = strategy(floor_heights, ball_weight, plate_strength, floor)
                aggregated_results[floor]['attempts'] += attempts
                if did_break:
                    break_results[breaking_floor]['breaks'] += 1

    total_attempts = sum(data['attempts'] for floor, data in aggregated_results.items())

    # Calculate average attempts and break percentage for each floor
    for floor in aggregated_results:
        aggregated_results[floor]['average_attempts'] = aggregated_results[floor][
                                                            'attempts'] / total_strategy_executions

        aggregated_results[floor]['breaks'] = (break_results[floor]['breaks'])

        try:
            aggregated_results[floor]['break_percentage'] = (aggregated_results[floor]['breaks'] / total_attempts) * 100
        except ZeroDivisionError:
            aggregated_results[floor]['break_percentage'] = 0

    return aggregated_results


def find_most_efficient_floor_from_results(simulation_results_to_analyze):
    """
    Find the most efficient floor from the simulation results.
    :param simulation_results_to_analyze: Dictionary containing the results from the simulation.
    :return: The most efficient floor and its efficiency score.
    """
    efficiency_scores = {}

    for floor, data in simulation_results_to_analyze.items():
        try:
            efficiency_score_calc = data['average_attempts'] / data['break_percentage']
            efficiency_scores[floor] = efficiency_score_calc
        except ZeroDivisionError:
            efficiency_scores[floor] = float('inf')  # Set to infinity if no breaks

    # Find the floor with the lowest efficiency score
    most_efficient_floor_calc = min(efficiency_scores, key=efficiency_scores.get)
    return most_efficient_floor_calc, efficiency_scores[most_efficient_floor_calc]


def find_floor_with_most_breaks(aggregated_results):
    """
    Find the floor with the most breaks.
    :param aggregated_results: Dictionary containing the results from the simulation.
    :return: Floor with the most breaks and the number of breaks.
    """
    max_breaks = 0
    floor_with_most_breaks = None

    for floor, data in aggregated_results.items():
        if data['breaks'] > max_breaks:
            max_breaks = data['breaks']
            floor_with_most_breaks = floor

    return floor_with_most_breaks, max_breaks


def plot_simulation_results(simulation_results_to_plot, avg_ball_weight_to_plot, avg_plate_strength_to_plot,
                            avg_floor_height_to_plot,
                            most_efficient_floor_to_plot, efficiency_score_to_plot, iterations):
    """
    Plot the simulation results and annotate with the most efficient floor.
    :param simulation_results_to_plot: Dictionary containing the results from the simulation.
    :param avg_ball_weight_to_plot: Average weight of the ball used in the simulation.
    :param avg_plate_strength_to_plot: Average strength of the plate used in the simulation.
    :param avg_floor_height_to_plot: Average height of the floors used in the simulation.
    :param most_efficient_floor_to_plot: The most efficient starting floor determined from the simulation.
    :param efficiency_score_to_plot: The efficiency score of the most efficient floor.
    :param iterations: Number of iterations used in the simulation.
    """
    # Extracting data from simulation_results
    floors = list(simulation_results_to_plot.keys())
    average_attempts = [simulation_results_to_plot[floor]['average_attempts'] for floor in floors]
    break_percentages = [simulation_results_to_plot[floor]['break_percentage'] for floor in floors]
    total_breaks_per_floor = [simulation_results_to_plot[floor]['breaks'] for floor in floors]
    efficiency_scores = [
        data['average_attempts'] / data['break_percentage'] if data['break_percentage'] > 0 else float('inf') for
        floor, data in simulation_results_to_plot.items()]

    # Creating a plot window with 4 subplots
    plt.figure(figsize=(15, 20))

    # Adjust the font sizes for the titles, labels, and ticks here:
    title_fontsize = 8
    label_fontsize = 6
    ticks_fontsize = 6
    annotation_fontsize = 8

    # Plotting average attempts
    plt.subplot(4, 1, 1)
    plt.plot(floors, average_attempts, marker='o', color='b')
    plt.title(
        f'Average Number of Attempts per Floor\n(Avg Ball Weight: {avg_ball_weight_to_plot} kg, Avg Plate Strength: '
        f'{avg_plate_strength_to_plot} N, Avg Floor Height: {avg_floor_height_to_plot} m)',
        fontsize=title_fontsize)
    plt.xlabel('Floor Number', fontsize=label_fontsize)
    plt.ylabel('Average Attempts', fontsize=label_fontsize)
    plt.xticks(fontsize=ticks_fontsize)
    plt.yticks(fontsize=ticks_fontsize)
    plt.grid(True)

    # Plotting break percentage
    plt.subplot(4, 1, 2)
    plt.plot(floors, break_percentages, marker='o', color='r')
    plt.title(f'Break Percentage per Floor', fontsize=title_fontsize)
    plt.xlabel('Floor Number', fontsize=label_fontsize)
    plt.ylabel('Break Percentage (%)', fontsize=label_fontsize)
    plt.xticks(fontsize=ticks_fontsize)
    plt.yticks(fontsize=ticks_fontsize)
    plt.grid(True)

    # Plotting total breaks per floor
    plt.subplot(4, 1, 3)
    plt.bar(floors, total_breaks_per_floor, color='g')
    plt.title('Total Breaks per Actual Breaking Floor', fontsize=title_fontsize)
    plt.xlabel('Floor Number', fontsize=label_fontsize)
    plt.ylabel('Total Breaks', fontsize=label_fontsize)
    plt.xticks(fontsize=ticks_fontsize)
    plt.yticks(fontsize=ticks_fontsize)
    plt.grid(True)

    # Plotting efficiency scores
    plt.subplot(4, 1, 4)
    plt.plot(floors, efficiency_scores, marker='o', color='m')
    plt.title('Efficiency Score per Floor (lower is better)', fontsize=title_fontsize)
    plt.xlabel('Floor Number', fontsize=label_fontsize)
    plt.ylabel('Efficiency Score', fontsize=label_fontsize)
    plt.xticks(fontsize=ticks_fontsize)
    plt.yticks(fontsize=ticks_fontsize)
    plt.grid(True)

    # Highlight the most efficient floor in each plot
    for i in range(1, 5):
        plt.subplot(4, 1, i)
        plt.axvline(x=most_efficient_floor_to_plot, color='k', linestyle='--')
        plt.text(most_efficient_floor_to_plot, plt.ylim()[1] * 0.9, f'Most Efficient Floor: '
                                                                    f'{most_efficient_floor_to_plot}', ha='right',
                 fontsize=annotation_fontsize)

    # Annotating with the most efficient floor
    plt.figtext(0.5, 0.02,
                f"Most Efficient Floor: {most_efficient_floor_to_plot}, Efficiency Score: "
                f"{efficiency_score_to_plot:.6f},"
                f"Iterations: {iterations}", ha="center", fontsize=annotation_fontsize,
                bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})

    # Display the plot
    plt.tight_layout()
    # Get the current figure's manager for Qt backend
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()  # Maximizes the window for Qt5
    plt.show()


if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run the plate break simulation.")
    parser.add_argument("--num_iterations", type=int, default=1000,
                        help="Number of iterations to run the simulation.")
    parser.add_argument("--ball_weight_min", type=float, default=0.5, help="Minimum ball weight in kg.")
    parser.add_argument("--ball_weight_max", type=float, default=1.5, help="Maximum ball weight in kg.")
    parser.add_argument("--plate_strength_min", type=float, default=40, help="Minimum plate strength in Newtons.")
    parser.add_argument("--plate_strength_max", type=float, default=70, help="Maximum plate strength in Newtons.")
    parser.add_argument("--floor_height_min", type=float, default=1, help="Minimum floor height in meters.")
    parser.add_argument("--floor_height_max", type=float, default=3, help="Maximum floor height in meters.")

    args = parser.parse_args()

    # Extract values from args
    NUM_ITERATIONS = args.num_iterations
    BALL_WEIGHT_RANGE = (args.ball_weight_min, args.ball_weight_max)
    PLATE_STRENGTH_RANGE = (args.plate_strength_min, args.plate_strength_max)
    FLOOR_HEIGHT_RANGE = (args.floor_height_min, args.floor_height_max)

    # List of strategies
    strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                  binary_search_strategy]

    logging.info("Starting the simulation.")
    # Run the simulation
    simulation_results = run_simulation_with_adjusted_parameters(NUM_ITERATIONS, BALL_WEIGHT_RANGE,
                                                                 PLATE_STRENGTH_RANGE,
                                                                 FLOOR_HEIGHT_RANGE, strategies)

    # Pretty-print the results
    pprint(simulation_results)

    # Calculate the floor with the most breaks and its number of breaks
    most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)
    logging.info(f"Floor with Most Breaks: {most_breaks_floor}, Number of Breaks: {most_breaks}")

    # Calculate the most efficient floor and its efficiency score
    most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)
    logging.info(f"Most Efficient Floor: {most_efficient_floor}, Efficiency Score: {efficiency_score}")

    # Calculate the average ball weight and floor height used in the simulation
    avg_ball_weight = sum(BALL_WEIGHT_RANGE) / 2  # Average of the BALL_WEIGHT_RANGE
    avg_plate_strength = sum(PLATE_STRENGTH_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE
    avg_floor_height = sum(FLOOR_HEIGHT_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE

    # Plot the results
    plot_simulation_results(simulation_results, avg_ball_weight, avg_plate_strength, avg_floor_height,
                            most_efficient_floor, efficiency_score, NUM_ITERATIONS)

    logging.info("Simulation completed.")
