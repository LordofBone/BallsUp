# BallsUp: Plate Break Simulation

BallsUp is a simulation tool designed to determine the most efficient floor from which to drop a ball in order to break a plate positioned on the ground. 
The program utilizes various strategies to minimize the number of attempts required to find the critical breaking point, adapting to different weights of the ball and strengths of the plate.

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