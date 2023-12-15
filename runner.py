import random
import math
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
    floor = start_floor

    # Adjust floor index for zero-based list indexing
    adjusted_floor_index = floor - 1

    # Initially check if the plate breaks or not at the starting floor
    current_force = calculate_impact_force(floor_heights[adjusted_floor_index] * floor, ball_weight)
    # current_force = calculate_impact_force(floor_heights[floor] * floor, ball_weight)
    initial_break = current_force > plate_strength
    attempts += 1

    if initial_break:
        # If it breaks, go down to find the minimum breaking floor
        while floor > 0:
            floor -= 1
            attempts += 1
            current_force = calculate_impact_force(floor_heights[floor] * (floor + 1), ball_weight)
            if current_force <= plate_strength:
                # Found the floor just before it stops breaking
                floor += 1
                break
    else:
        # If it doesn't break, go up to find the breaking floor
        while floor < 99:
            floor += 1
            attempts += 1
            current_force = calculate_impact_force(floor_heights[floor] * (floor + 1), ball_weight)
            if current_force > plate_strength:
                # Found the breaking floor
                break

    did_break = (floor < 100) and (
            calculate_impact_force(floor_heights[floor] * (floor + 1), ball_weight) > plate_strength)
    return attempts, did_break


def precise_halving_strategy_simulation_with_flag(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply the halving strategy to find the approximate breaking floor, then count up to find the minimum breaking floor.
    :param floor_heights: Heights of each floor.
    :param ball_weight: Weight of the ball.
    :param plate_strength: Strength of the plate.
    :param start_floor: Starting floor for the simulation.
    :return: Number of attempts to find the breaking floor and a flag indicating if a break occurred.
    """

    attempts = 0
    floor = start_floor
    step = max(1, start_floor // 2)

    # Halving strategy
    while step >= 1:
        attempts += 1
        current_force = calculate_impact_force(floor_heights[floor - 1] * floor, ball_weight)

        if current_force > plate_strength:
            floor -= step
        else:
            floor = min(floor + step, 99)
        step //= 2

    # Iterative search by counting up
    did_break = False
    while floor < 100:
        current_force = calculate_impact_force(floor_heights[floor] * (floor + 1), ball_weight)
        if current_force > plate_strength:
            did_break = True
            break
        floor += 1
        attempts += 1

    return attempts, did_break


def binary_search_strategy(floor_heights, ball_weight, plate_strength, start_floor):
    """
    Apply the binary search strategy to find the minimum breaking floor.
    :param floor_heights:
    :param ball_weight:
    :param plate_strength:
    :param start_floor:
    :return:
    """

    # Adjust start_floor to zero-based indexing when accessing the list
    start_floor_index = start_floor - 1
    low = 0
    high = len(floor_heights) - 1
    attempts = 0
    did_break = False
    breaking_floor = None

    # Check if the starting floor breaks the plate
    current_force = calculate_impact_force(floor_heights[start_floor_index] * start_floor, ball_weight)
    attempts += 1
    if current_force > plate_strength:
        did_break = True
        breaking_floor = start_floor_index
        # Since the plate broke at the starting floor, search downwards for the actual breaking floor
        while breaking_floor > 0:
            current_force = calculate_impact_force(floor_heights[breaking_floor - 1] * breaking_floor, ball_weight)
            attempts += 1
            if current_force <= plate_strength:
                # Found the actual breaking floor
                break
            breaking_floor -= 1
    else:
        # If the plate does not break at the starting floor, perform binary search upwards
        low = start_floor_index + 1
        while low <= high:
            mid = (low + high) // 2
            attempts += 1
            current_force = calculate_impact_force(floor_heights[mid] * (mid + 1), ball_weight)

            if current_force > plate_strength:
                did_break = True
                # breaking_floor = mid
                high = mid - 1
            else:
                low = mid + 1

    # The breaking_floor needs to be incremented by 1 if a break was found because of zero-based indexing
    return attempts, did_break


def run_simulation_with_adjusted_parameters(num_iterations, ball_weight_range, plate_strength_range, floor_height_range,
                                            strategies):
    """
    Run simulations with a dynamic number of strategies.
    :param num_iterations: Number of iterations to run the simulation.
    :param ball_weight_range: Tuple representing the range of ball weight in kg.
    :param plate_strength_range: Tuple representing the range of plate strength in Newtons.
    :param floor_height_range: Tuple representing the range of floor heights in meters.
    :param strategies: List of strategy functions to use in the simulation.
    :return: Aggregated results for each starting floor and each strategy.
    """
    # Modify the structure of aggregated results
    aggregated_results = {floor: {'attempts': 0, 'breaks': 0} for floor in range(1, 101)}
    total_strategy_executions = num_iterations * len(strategies)

    for _ in range(num_iterations):
        floor_heights = [random.uniform(*floor_height_range) for _ in range(100)]
        ball_weight = random.uniform(*ball_weight_range)
        plate_strength = random.uniform(*plate_strength_range)

        for floor in range(1, 101):
            for strategy in strategies:
                attempts, did_break = strategy(floor_heights, ball_weight, plate_strength, floor)
                aggregated_results[floor]['attempts'] += attempts
                if did_break:
                    aggregated_results[floor]['breaks'] += 1

    # Calculate average attempts and break percentage for each floor
    for floor in aggregated_results:
        aggregated_results[floor]['average_attempts'] = aggregated_results[floor][
                                                            'attempts'] / total_strategy_executions
        aggregated_results[floor]['break_percentage'] = (aggregated_results[floor][
                                                             'breaks'] / total_strategy_executions) * 100

    return aggregated_results


def find_most_efficient_floor_from_results(simulation_results):
    """
    Find the most efficient floor from the simulation results.
    :param simulation_results: Dictionary containing the results from the simulation.
    :return: The most efficient floor and its efficiency score.
    """
    efficiency_scores = {}

    for floor, data in simulation_results.items():
        if data['breaks'] > 0:
            efficiency_score = data['average_attempts'] / data['break_percentage']
            efficiency_scores[floor] = efficiency_score
        else:
            efficiency_scores[floor] = float('inf')  # Set to infinity if no breaks

    # Find the floor with the lowest efficiency score
    most_efficient_floor = min(efficiency_scores, key=efficiency_scores.get)
    return most_efficient_floor, efficiency_scores[most_efficient_floor]


def plot_simulation_results(simulation_results, avg_ball_weight, avg_plate_strength, avg_floor_height,
                            most_efficient_floor,
                            efficiency_score, iterations):
    """
    Plot the simulation results and annotate with the most efficient floor.
    :param simulation_results: Dictionary containing the results from the simulation.
    :param avg_ball_weight: Average weight of the ball used in the simulation.
    :param avg_floor_height: Average height of the floors used in the simulation.
    :param most_efficient_floor: The most efficient starting floor determined from the simulation.
    :param efficiency_score: The efficiency score of the most efficient floor.
    """
    # Extracting data from simulation_results
    floors = list(simulation_results.keys())
    average_attempts = [simulation_results[floor]['average_attempts'] for floor in floors]
    break_percentages = list(reversed([simulation_results[floor]['break_percentage'] for floor in floors]))

    # Creating a plot
    plt.figure(figsize=(15, 6))

    # Plotting average attempts
    plt.subplot(1, 2, 1)
    plt.plot(floors, average_attempts, marker='o', color='b')
    plt.title(
        f'Average Number of Attempts per Floor\n(Avg Ball Weight: {avg_ball_weight} kg, Avg Ball Weight: '
        f'{avg_plate_strength} N, Avg Floor Height: {avg_floor_height} m)')
    plt.xlabel('Floor Number')
    plt.ylabel('Average Attempts')
    plt.grid(True)

    # Plotting break percentage
    plt.subplot(1, 2, 2)
    plt.plot(floors, break_percentages, marker='o', color='r')
    plt.title(
        f'Break Percentage per Floor\n(Avg Ball Weight: {avg_ball_weight} kg, Avg Plate Strength: '
        f'{avg_plate_strength} N, Avg Floor Height: {avg_floor_height} m)')
    plt.xlabel('Floor Number')
    plt.ylabel('Break Percentage (%)')
    plt.grid(True)

    # Annotating with the most efficient floor
    plt.figtext(0.5, 0.01, f"Most Efficient Floor: {most_efficient_floor}, Efficiency Score: {efficiency_score:.6f}, "
                           f"Iterations: {iterations}",
                ha="center", fontsize=12, bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})

    # Display the plot
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Adjustable variables
    NUM_ITERATIONS = 10000  # Number of iterations to run the simulation | Default: 10000
    BALL_WEIGHT_RANGE = (0.01, 2)  # Ball weight range in kg (e.g., from 50g to 100kg) | Default: (0.01, 2)
    PLATE_STRENGTH_RANGE = (0.1, 100)  # Plate strength range in Newtons | Default: (0.1, 100)
    FLOOR_HEIGHT_RANGE = (1, 11)  # Floor height range in meters | Default: (1, 11)

    # List of strategies
    strategies = [linear_search_simulation_with_flag, precise_halving_strategy_simulation_with_flag, binary_search_strategy]

    # Run the simulation
    simulation_results = run_simulation_with_adjusted_parameters(NUM_ITERATIONS, BALL_WEIGHT_RANGE,
                                                                 PLATE_STRENGTH_RANGE,
                                                                 FLOOR_HEIGHT_RANGE, strategies)

    # Pretty-print the results
    pprint(simulation_results)

    # Example usage
    most_efficient_floor, efficiency_score = find_most_efficient_floor_from_results(simulation_results)
    print(f"Most Efficient Floor: {most_efficient_floor}, Efficiency Score: {efficiency_score}")

    # Calculate the average ball weight and floor height used in the simulation
    avg_ball_weight = sum(BALL_WEIGHT_RANGE) / 2  # Average of the BALL_WEIGHT_RANGE
    avg_plate_strength = sum(PLATE_STRENGTH_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE
    avg_floor_height = sum(FLOOR_HEIGHT_RANGE) / 2  # Average of the FLOOR_HEIGHT_RANGE

    # Example usage
    plot_simulation_results(simulation_results, avg_ball_weight, avg_plate_strength, avg_floor_height,
                            most_efficient_floor, efficiency_score, NUM_ITERATIONS)
