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

To get started with BallsUp, install Python 3.11 or newer and the project dependencies.

### Prerequisites

- Python 3.11 or higher
- Pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LordofBone/BallsUp.git
cd BallsUp
```

2. Create Python virtual environment (optional):
```bash
python -m venv venv
```

3. Activate virtual environment and install requirements (optional):
```bash
source venv/bin/activate
pip install -r requirements-gui.txt
```

Or you can install the requirements globally (non-virtual environment) like so:
```bash
pip install -r requirements-gui.txt
```

### Usage

To open the browser dashboard, run:
```bash
python -m streamlit run app.py
```

By default, the dashboard listens on `127.0.0.1` and is accessible only from the machine running it. Open `http://127.0.0.1:8501` in your browser.

To allow access from another device on your network, override the bind address when launching Streamlit. Replace `192.168.1.10` with the IP address of the network interface you want to use.

```bash
python -m streamlit run app.py --server.address 192.168.1.10
```

Use `--server.address 0.0.0.0` to listen on all IPv4 interfaces. From another device, open the host's network IP address on port `8501`, for example `http://192.168.1.10:8501`.

> **Warning:** Binding to `0.0.0.0` can expose the dashboard on Wi-Fi, Ethernet, and VPN connections, and potentially to the internet if the host is publicly reachable or a router forwards the port. Keep the default `127.0.0.1` for local use. If you need network access, bind to the intended interface and configure your firewall to allow inbound TCP port `8501` only from trusted devices or subnets. Avoid public firewall rules and router port forwarding for this port.

Use the sidebar to set the iteration count, ball weight, plate strength, and floor height ranges. You can also select the search strategies to compare. Each iteration uses the same ball weight, plate strength, and floor heights for every selected strategy. Each strategy tab shows its own charts, summary metrics, per-floor results, and CSV download. Results stay visible while you adjust settings and update when you run again.

The dashboard allows 6,000 work units per run. Each iteration costs 8 units for linear search, 2 for halving, and 2 for binary search. Add the costs of the selected strategies to get the cost per iteration. This allows 500 iterations with all three strategies, 750 with linear search alone, and 3,000 with either halving or binary search alone. The dashboard starts with 500 iterations and all three strategies selected. Each server process runs one simulation at a time. If the slot is occupied, the dashboard displays a busy message and you can retry.

The following simulation timings are medians of three runs at 100 iterations on a Cortex-A76 with Python 3.13.5. They cover computation across all 100 starting floors and exclude chart rendering. The edge cases fix the ball weight and floor height at 1 kg and 1 m, respectively, with plate strength set to 4,400 N, 1 N, or 10,000 N.

| Settings | Linear search | Halving | Binary search | All three |
| --- | ---: | ---: | ---: | ---: |
| Dashboard defaults | 1.331 s | 0.450 s | 0.443 s | 2.092 s |
| Break at floor 100 | 2.549 s | 0.493 s | 0.478 s | 3.400 s |
| Break at floor 1 | 2.417 s | 0.430 s | 0.375 s | 3.126 s |
| No break | 0.116 s | 0.116 s | 0.116 s | 0.246 s |

At the 500-iteration limit with all three strategies, simulation took 10.09 s with the default ranges and 16.82 s in the floor-100 case. Streamlit AppTest measured 11.81 s and 18.12 s from form submission through server-side rendering for those same cases. The budget weights reflect the higher cost of linear search in the edge cases. Actual runtimes depend on the machine and input ranges.

To run the original command-line interface, execute:
```bash
python run.py
```

If you only need the CLI, install `requirements.txt` instead. You can adjust its parameters with command-line options.

The simulation parameters are as follows:
```python
NUM_ITERATIONS = 1000  # Number of iterations to run the simulation | Default: 1000
BALL_WEIGHT_RANGE = (0.5, 1.5)  # Ball weight range in kg | Default: (0.5, 1.5)
PLATE_STRENGTH_RANGE = (4000, 7000)  # Plate strength range in Newtons | Default: (4000, 7000)
FLOOR_HEIGHT_RANGE = (1, 3)  # Floor height range in meters | Default: (1, 3)
```

The force estimate assumes the ball stops in 0.01 seconds after impact. `NUM_ITERATIONS` must be between 1 and 10,000; range endpoints must be positive, finite, and in ascending order.

They can also be adjusted like so:
```bash
python run.py --num_iterations 5000 --ball_weight_min 0.3 --ball_weight_max 2.0 --plate_strength_min 3000 --plate_strength_max 8000 --floor_height_min 0.5 --floor_height_max 5.0
```

Tests can be run with the following command:
```bash
python run_tests.py
```

### Results

The CLI prints the per-floor results and summary in the console and opens a Matplotlib graph. Matplotlib automatically selects an available backend on desktop Linux, Windows, macOS, and Raspberry Pi OS. Displaying the CLI graph requires a graphical session and a supported Python GUI toolkit, which the pip requirements do not install. For the system Python on Debian, Ubuntu, or Raspberry Pi OS, install Tk support with `sudo apt install python3-tk` if no other supported GUI toolkit is available. Without a usable interactive backend, Matplotlib can fall back to Agg and no graph window will open. The browser dashboard renders the charts within the page and does not need a desktop Matplotlib backend.
It will show the average number of attempts required to find the critical floor for all the strategies, as well as the break percentage for each floor, 
total breaks of each floor and the efficiency score for each floor, pooled across all strategies.

## Strategies Used

### Binary Search
The Binary Search strategy is a divide-and-conquer approach. It starts by checking the middle floor of a predefined range
(from the lowest to the highest floor). If the ball breaks the plate, the search continues in the lower half of the range, 
narrowing down the floors until the minimum breaking floor is found. If the ball does not break the plate, the search moves to the upper half. 
This method efficiently zeroes in on the critical breaking point.

### Halving
The Halving strategy is a heuristic approach that starts from a specific floor and then halves the distance to the ground, 
either moving up or down based on whether the plate breaks. The process repeats, halving the distance each time, 
until it hones in on the floor just high enough to break the plate. This strategy is a quick way to approximate the breaking point as a start, 
but then it linearly counts to find the exact floor as a final fine tune.

### Linear Search
The Linear Search strategy involves sequentially checking each floor, either moving upwards or downwards from a starting point. 
This method is straightforward and exhaustive, as it checks every floor until it finds the exact point where the plate breaks. 
While potentially slower than other methods, it guarantees finding the precise breaking point.

## Determining the Most Efficient Floor

The simulation includes a function `find_most_efficient_floor_from_results` to determine the most efficient floor to start the ball drop from. 
This function calculates an efficiency score for each floor based on the results of the simulation. Here's how it works:

1. **Efficiency Score Calculation**: The efficiency score for each floor is calculated by dividing the average number of attempts (to find the breaking point) by the break percentage at that floor. The break percentage is the ratio of the number of times the plate breaks when dropped from that floor to the total number of drops from that floor. This score aims to balance the need for a high chance of breaking the plate against the desire to minimize the number of attempts.

2. **Handling Zero Breaks**: If there are no breaks from a particular starting floor (which would lead to a division by zero), the efficiency score for that floor is set to infinity. This effectively ranks floors with no breaks as the least efficient.

3. **Identifying the Most Efficient Floor**: The floor with the lowest efficiency score is identified as the most efficient starting floor. A lower score indicates that fewer attempts are needed on average to break the plate, while still maintaining a high likelihood of breakage.

This approach provides a balanced measure of efficiency, taking into account both the effectiveness of breaking the plate and the effort (number of attempts) required to achieve this outcome. The most efficient floor is thus the one that optimizes these two factors.


## Contributing

Contributions to the project are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).
