# BallsUp: Plate Break Simulation

BallsUp is a simulation tool designed to determine the most efficient floor from which to drop a ball in order to break a plate positioned on the ground. 
The program utilizes various strategies to minimize the number of attempts required to find the critical breaking point, 
with a configurable range of randomly selected weights of the ball, strengths of the plate and floor heights.

## Features

- Implements binary search, halving, and linear search strategies.
- Determines the most statistically efficient starting floor for a ball drop.
- Customizable simulation parameters (ball weight, plate strength, floor height).
- Outputs both a raw and visual representation of simulation results.

## Getting Started

To get started with BallsUp, you need to have Python installed on your system along with the necessary libraries such as `numpy`, `matplotlib`, and `Pillow`.

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LordofBone/BallsUp.git
cd BallsUp
pip install -r requirements.txt
```

### Usage

To run the simulation, execute the main script:
```bash
python simulation.py
```

You can adjust the simulation parameters by editing the simulation.py file or by setting the variables at runtime.

The simulation parameters are as follows:
```python
NUM_ITERATIONS = 1000  # Number of iterations to run the simulation | Default: 1000
BALL_WEIGHT_RANGE = (0.5, 1.5)  # Ball weight range in kg | Default: (0.5, 1.5)
PLATE_STRENGTH_RANGE = (40, 70)  # Plate strength range in Newtons | Default: (40, 70)
FLOOR_HEIGHT_RANGE = (1, 3)  # Floor height range in meters | Default: (1, 3)
```

They can also be ajusted like so:
```bash
python simulation.py --num_iterations 5000 --ball_weight_min 0.3 --ball_weight_max 2.0 --plate_strength_min 30 --plate_strength_max 80
```

Tests can be run with the following command:
```bash
python run_tests.py
```

### Results

The results will then be show as a matplotlib graph and a text output in the console.
It will show the average number of attempts required to find the critical floor for all the strategies, as well as the break percentage for each floor, 
total breaks of each floor and the efficiency score for each floor.

## Strategies Used

### Binary Search
The Binary Search strategy is a divide-and-conquer approach. It starts by checking the middle floor of a predefined range
(from the lowest to the highest floor). If the ball breaks the plate, the search continues in the lower half of the range, 
narrowing down the floors until the minimum breaking floor is found. If the ball does not break the plate, the search moves to the upper half. 
This method efficiently zeroes in on the critical breaking point.

### Halving
The Halving strategy is a heuristic approach that starts from a specific floor and then halves the distance to the ground, 
either moving up or down based on whether the plate breaks. The process repeats, halving the distance each time, 
until it hones in on the floor just high enough to break the plate. This strategy is a quick way to approximate the breaking point.

### Linear Search
The Linear Search strategy involves sequentially checking each floor, either moving upwards or downwards from a starting point. 
This method is straightforward and exhaustive, as it checks every floor until it finds the exact point where the plate breaks. 
While potentially slower than other methods, it guarantees finding the precise breaking point.

## Contributing

Contributions to the project are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).