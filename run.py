import math
import random
from pprint import pprint

import matplotlib.pyplot as plt


def calculate_impact_force(height, weight):
    """
    Calculate the impact force of the ball.
    :param height: Drop height in meters.
    :param weight: Weight of the ball in kg.
    :return: Impact force in Newtons.
    """
    g = 9.8  # Gravity in m/s^2
    velocity = math.sqrt(2 * g * height)
    return weight * velocity


# Function to calculate the cumulative height up to a given floor
def cumulative_height(floor_heights, floor):
    return sum(floor_heights[:floor])


def linear_search_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply a linear search strategy to find the minimum breaking floor from a given start floor.
    :param floor_heights: Heights of each floor.
    :param ball_weight: Weight of the ball.
    :param plate_strength: Strength of the plate.
    :param start_floor: Starting floor for the simulation.
    :return: Number of attempts to find the minimum breaking floor and a flag indicating if a break occurred.
    """
    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        return attempts, did_break, breaking_floor

    floor = start_floor

    # Initially check if the plate breaks or not at the starting floor
    current_force = calculate_impact_force(cumulative_height(floor_heights, floor), ball_weight)
    initial_break = current_force > plate_strength
    attempts += 1

    if initial_break:
        # If it breaks, go down to find the minimum breaking floor
        while floor > 1:
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
        while floor < 100:

            attempts += 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, floor + 1), ball_weight)
            floor += 1
            if current_force > plate_strength:
                breaking_floor = floor
                did_break = True
                # Found the breaking floor
                break

    return attempts, did_break, breaking_floor


def precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor):
    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        return attempts, did_break, breaking_floor

    # Set initial high and low bounds for halving
    high = len(floor_heights) - 1
    low = 0
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

    # Check the floor if low and high have converged
    if low == high:
        attempts += 1
        current_force = calculate_impact_force(cumulative_height(floor_heights, low), ball_weight)
        if current_force > plate_strength:
            did_break = True
            breaking_floor = low

    # If the halving strategy did not find a breaking floor, perform a linear search upwards
    if not did_break:
        for f in range(start_floor, len(floor_heights)):
            current_force = calculate_impact_force(cumulative_height(floor_heights, f), ball_weight)
            attempts += 1
            if current_force > plate_strength:
                did_break = True
                breaking_floor = f
                break

    # Verify the breaking floor by checking the floor below, if a breaking floor was found
    if did_break and breaking_floor is not None and breaking_floor > 0:
        current_force = calculate_impact_force(cumulative_height(floor_heights, breaking_floor - 1), ball_weight)
        attempts += 1
        if current_force <= plate_strength:
            breaking_floor -= 1

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
    attempts = 0
    did_break = False
    breaking_floor = None

    # Calculate the maximum possible force (at the highest floor)
    max_force = calculate_impact_force(cumulative_height(floor_heights, len(floor_heights)), ball_weight)
    if max_force <= plate_strength:
        # If the max force doesn't break the plate, exit early
        return attempts, did_break, breaking_floor

    low = 0
    high = len(floor_heights) - 1
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
            mid = (low + high) // 2
            attempts += 1
            current_force = calculate_impact_force(cumulative_height(floor_heights, mid), ball_weight)

            if current_force > plate_strength:
                did_break = True
                breaking_floor = mid
                high = mid - 1
            else:
                low = mid + 1

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


def plot_simulation_results(simulation_results, avg_ball_weight, avg_plate_strength, avg_floor_height,
                            most_efficient_floor, efficiency_score, iterations):
    """
    Plot the simulation results and annotate with the most efficient floor.
    :param simulation_results: Dictionary containing the results from the simulation.
    :param avg_ball_weight: Average weight of the ball used in the simulation.
    :param avg_plate_strength: Average strength of the plate used in the simulation.
    :param avg_floor_height: Average height of the floors used in the simulation.
    :param most_efficient_floor: The most efficient starting floor determined from the simulation.
    :param efficiency_score: The efficiency score of the most efficient floor.
    :param iterations: Number of iterations used in the simulation.
    """
    # Extracting data from simulation_results
    floors = list(simulation_results.keys())
    average_attempts = [simulation_results[floor]['average_attempts'] for floor in floors]
    break_percentages = [simulation_results[floor]['break_percentage'] for floor in floors]
    total_breaks_per_floor = [simulation_results[floor]['breaks'] for floor in floors]
    efficiency_scores = [
        data['average_attempts'] / data['break_percentage'] if data['break_percentage'] > 0 else float('inf') for
        floor, data in simulation_results.items()]

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
        f'Average Number of Attempts per Floor\n(Avg Ball Weight: {avg_ball_weight} kg, Avg Plate Strength: '
        f'{avg_plate_strength} N, Avg Floor Height: {avg_floor_height} m)',
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
        plt.axvline(x=most_efficient_floor, color='k', linestyle='--')
        plt.text(most_efficient_floor, plt.ylim()[1] * 0.9, f'Most Efficient Floor: {most_efficient_floor}', ha='right',
                 fontsize=annotation_fontsize)

    # Annotating with the most efficient floor
    plt.figtext(0.5, 0.02,
                f"Most Efficient Floor: {most_efficient_floor}, Efficiency Score: {efficiency_score:.6f}, Iterations: "
                f"{iterations}", ha="center", fontsize=annotation_fontsize,
                bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})

    # Display the plot
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Adjustable variables
    NUM_ITERATIONS = 1  # Number of iterations to run the simulation | Default: 10000
    BALL_WEIGHT_RANGE = (0.01, 2)  # Ball weight range in kg (e.g., from 50g to 100kg) | Default: (0.01, 2)
    PLATE_STRENGTH_RANGE = (0.1, 100)  # Plate strength range in Newtons | Default: (0.1, 100)
    FLOOR_HEIGHT_RANGE = (1, 11)  # Floor height range in meters | Default: (1, 11)

    # List of strategies
    strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag,
                  binary_search_strategy]

    # Run the simulation
    simulation_results = run_simulation_with_adjusted_parameters(NUM_ITERATIONS, BALL_WEIGHT_RANGE,
                                                                 PLATE_STRENGTH_RANGE,
                                                                 FLOOR_HEIGHT_RANGE, strategies)

    # Pretty-print the results
    pprint(simulation_results)

    # Calculate the floor with the most breaks and its number of breaks
    most_breaks_floor, most_breaks = find_floor_with_most_breaks(simulation_results)
    print(f"Floor with Most Breaks: {most_breaks_floor}, Number of Breaks: {most_breaks}")

    # Calculate the most efficient floor and its efficiency score
    most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)
    print(f"Most Efficient Floor: {most_efficient_floor}, Efficiency Score: {efficiency_score}")

    # Calculate the average ball weight and floor height used in the simulation
    avg_ball_weight = sum(BALL_WEIGHT_RANGE) / 2  # Average of the BALL_WEIGHT_RANGE
    avg_plate_strength = sum(PLATE_STRENGTH_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE
    avg_floor_height = sum(FLOOR_HEIGHT_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE

    # Plot the results
    plot_simulation_results(simulation_results, avg_ball_weight, avg_plate_strength, avg_floor_height,
                            most_efficient_floor, efficiency_score, NUM_ITERATIONS)
