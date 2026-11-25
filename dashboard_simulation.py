"""Work admission shared by all dashboard sessions in this process."""

from threading import BoundedSemaphore

from run import (
    MAX_ITERATIONS,
    binary_search_strategy,
    linear_search_simulation_with_flag,
    precise_halving_strategy_simulation_with_flag,
    run_simulation_with_adjusted_parameters,
)


STRATEGIES = {
    "Linear search": (linear_search_simulation_with_flag, 8),
    "Halving": (precise_halving_strategy_simulation_with_flag, 2),
    "Binary search": (binary_search_strategy, 2),
}
GUI_WORK_BUDGET = 6_000
GUI_MAX_ITERATIONS = GUI_WORK_BUDGET // min(weight for _, weight in STRATEGIES.values())
_simulation_slots = BoundedSemaphore(1)


class SimulationBusyError(RuntimeError):
    """All dashboard simulation slots are occupied."""


def run_dashboard_simulation(iterations, ranges, selected):
    if not isinstance(iterations, int) or not 1 <= iterations <= MAX_ITERATIONS:
        raise ValueError(f"Iterations must be between 1 and {MAX_ITERATIONS:,}.")
    if not selected:
        raise ValueError("Select at least one strategy.")
    strategies, weights = zip(*(STRATEGIES[name] for name in selected))
    max_iterations = GUI_WORK_BUDGET // sum(weights)
    if iterations > max_iterations:
        raise ValueError(f"The selected strategies allow up to {max_iterations:,} iterations per dashboard run.")

    if not _simulation_slots.acquire(blocking=False):
        raise SimulationBusyError("The server is busy running a simulation. Try again in a moment.")
    try:
        return run_simulation_with_adjusted_parameters(iterations, *ranges, strategies)
    finally:
        _simulation_slots.release()
