# BallsUp

BallsUp simulates dropping a ball from different floors to find the lowest floor that breaks a plate. Compare linear search, halving, and binary search across randomized ball weights, plate strengths, and floor heights.

## Quick start

With Python 3.11 or newer, create and activate a virtual environment.

```bash
git clone https://github.com/LordofBone/BallsUp.git
cd BallsUp
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use `.\.venv\Scripts\Activate.ps1` for the activation step.

Install the dashboard dependencies and start Streamlit from the repository root.

```bash
python -m pip install -r requirements-gui.txt
python -m streamlit run app.py
```

Open [the local dashboard](http://127.0.0.1:8501). Use the sidebar to choose strategies, iterations, and input ranges. Each strategy runs against the same sampled inputs and gets its own charts, per-floor results, and CSV download. The dashboard allows 500 iterations with all three strategies, 750 with linear search alone, or 3,000 with halving or binary search alone. Each server process runs one simulation at a time.

<details>
<summary>Access from another device</summary>

The dashboard binds to `127.0.0.1` by default. To use it from a trusted device on your network, bind to the host's LAN IP address. Replace the example address with yours.

```bash
python -m streamlit run app.py --server.address 192.168.1.10
```

Open `http://192.168.1.10:8501` from the other device. Limit inbound TCP port 8501 to trusted devices or subnets and avoid public port forwarding.

</details>

## Command line

For a CLI-only setup, install `requirements.txt`. If you installed the dashboard dependencies, you can already run the CLI.

```bash
python run.py
python run.py --help
```

The CLI defaults to 1,000 iterations, with ball weights of 0.5–1.5 kg, plate strengths of 4,000–7,000 N, and floor heights of 1–3 m. Pass `--num_iterations` to set a count from 1 to 10,000. Range endpoints must be positive, finite, and in ascending order.

The CLI prints pooled results and opens a Matplotlib chart when an interactive backend is available. On Debian, Ubuntu, or Raspberry Pi OS, `sudo apt install python3-tk` adds Tk support for the system Python. The dashboard renders charts in the browser.

## Tests

Install the dashboard dependencies to run the full suite.

```bash
python run_tests.py
```

Run the dashboard suite on its own with `python run_gui_tests.py`. This runner fails if a dashboard test is skipped.

In VS Code, open this README in the editor and select the command text inside a code block. Open the Command Palette and choose **Terminal: Run Selected Text in Active Terminal**. Use a terminal with the appropriate shell and virtual environment active for the command you’re running. [VS Code terminal documentation](https://code.visualstudio.com/docs/terminal/basics#_run-selected-text)

## How results are ranked

- **Linear search** checks adjacent floors from the chosen starting floor.
- **Halving** repeatedly adjusts the floor by smaller steps, then checks adjacent floors to find the threshold.
- **Binary search** narrows the candidate interval until it finds the lowest breaking floor.

The force estimate assumes the ball stops in 0.01 seconds on impact. To rank starting floors, the simulation divides average attempts by the break percentage. Lower scores are better. A zero break percentage gives an infinite score.

<details>
<summary>Dashboard benchmarks</summary>

The following simulation timings are medians of three runs at 100 iterations on a Cortex-A76 with Python 3.13.5. They cover computation across all 100 starting floors and exclude chart rendering. The edge cases fix the ball weight and floor height at 1 kg and 1 m, respectively, with plate strength set to 4,400 N, 1 N, or 10,000 N.

| Settings | Linear search | Halving | Binary search | All three |
| --- | ---: | ---: | ---: | ---: |
| Dashboard defaults | 1.331 s | 0.450 s | 0.443 s | 2.092 s |
| Break at floor 100 | 2.549 s | 0.493 s | 0.478 s | 3.400 s |
| Break at floor 1 | 2.417 s | 0.430 s | 0.375 s | 3.126 s |
| No break | 0.116 s | 0.116 s | 0.116 s | 0.246 s |

At the 500-iteration limit with all three strategies, simulation took 10.09 s with the default ranges and 16.82 s in the floor-100 case. Streamlit AppTest measured 11.81 s and 18.12 s from form submission through server-side rendering for those same cases. The budget weights reflect the higher cost of linear search in the edge cases. Actual runtimes depend on the machine and input ranges.

</details>

## License

[GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
