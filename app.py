"""Browser-based dashboard for the BallsUp simulation."""

import csv
import io
import math

import streamlit as st
from matplotlib.figure import Figure

from run import (
    MAX_ITERATIONS,
    binary_search_strategy,
    find_floor_with_most_breaks,
    find_most_efficient_floor_from_results,
    linear_search_simulation_with_flag,
    precise_halving_strategy_simulation_with_flag,
    run_simulation_with_adjusted_parameters,
)


STRATEGIES = {
    "Linear search": linear_search_simulation_with_flag,
    "Halving": precise_halving_strategy_simulation_with_flag,
    "Binary search": binary_search_strategy,
}


def results_csv(results):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(("floor", "attempts", "breaks", "starting_breaks", "average_attempts", "break_percentage", "efficiency_score"))
    for floor, data in results.items():
        score = data["average_attempts"] / data["break_percentage"] if data["break_percentage"] else math.inf
        writer.writerow((floor, data["attempts"], data["breaks"], data["starting_breaks"],
                         data["average_attempts"], data["break_percentage"], score))
    return output.getvalue()


def make_chart(results, field, title, label, color, best_floor, bar=False):
    figure = Figure(figsize=(10, 3.2), dpi=130, facecolor="#111827")
    axes = figure.subplots()
    axes.set_facecolor("#111827")
    floors = list(results)
    values = [results[floor][field] for floor in floors]
    if bar:
        axes.bar(floors, values, color=color, width=0.8, alpha=0.9)
    else:
        axes.plot(floors, values, color=color, linewidth=2.3)
        axes.fill_between(floors, values, color=color, alpha=0.12)
    axes.axvline(best_floor, color="#fbbf24", linestyle="--", linewidth=1.4,
                 label=f"Best start · floor {best_floor}")
    axes.set_title(title, color="#f8fafc", fontsize=13, fontweight="bold", loc="left", pad=16)
    axes.set_xlabel("Starting floor" if field != "breaks" else "Breaking floor", color="#94a3b8")
    axes.set_ylabel(label, color="#94a3b8")
    axes.tick_params(colors="#94a3b8", labelsize=8)
    axes.grid(axis="y", color="#334155", alpha=0.55)
    axes.set_axisbelow(True)
    for spine in axes.spines.values():
        spine.set_visible(False)
    axes.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f8fafc", fontsize=8)
    figure.tight_layout()
    return figure


def display_results(results, iterations, ranges, strategy_count):
    best_floor, efficiency = find_most_efficient_floor_from_results(results)
    most_breaks_floor, most_breaks = find_floor_with_most_breaks(results)

    st.subheader("Simulation results")
    columns = st.columns(4)
    columns[0].metric("Best starting floor", best_floor)
    columns[1].metric("Efficiency score", f"{efficiency:.6f}" if math.isfinite(efficiency) else "∞")
    columns[2].metric("Most breaks at floor", most_breaks_floor if most_breaks_floor is not None else "—")
    columns[3].metric("Breaks at that floor", f"{most_breaks:,}")
    st.caption(f"{iterations:,} iterations · {strategy_count} strategies · mean ball weight {sum(ranges[0]) / 2:g} kg · "
               f"mean plate strength {sum(ranges[1]) / 2:g} N · mean floor height {sum(ranges[2]) / 2:g} m")

    chart_specs = (
        ("average_attempts", "Average attempts per starting floor", "Attempts", "#38bdf8", False),
        ("break_percentage", "Break percentage per starting floor", "Break percentage (%)", "#fb7185", False),
        ("breaks", "Total breaks per actual breaking floor", "Total breaks", "#34d399", True),
    )
    tabs = st.tabs(("Attempts", "Break chance", "Total breaks", "Efficiency", "Raw data"))
    for tab, (field, title, label, color, bar) in zip(tabs, chart_specs):
        with tab:
            st.pyplot(make_chart(results, field, title, label, color, best_floor, bar), clear_figure=True)

    efficiency_results = {
        floor: {"score": data["average_attempts"] / data["break_percentage"]
                if data["break_percentage"] else math.nan}
        for floor, data in results.items()
    }
    with tabs[3]:
        st.pyplot(make_chart(efficiency_results, "score", "Efficiency score per floor · lower is better",
                               "Score", "#c084fc", best_floor), clear_figure=True)
        st.caption("Floors with no starting breaks have an infinite score and are omitted from this chart.")
    with tabs[4]:
        rows = [dict(floor=floor, **data,
                     efficiency_score=data["average_attempts"] / data["break_percentage"]
                     if data["break_percentage"] else math.inf)
                for floor, data in results.items()]
        st.dataframe(rows, hide_index=True, width="stretch")
        st.download_button("Download CSV", results_csv(results), "ballsup-results.csv", "text/csv")


def main():
    st.set_page_config(page_title="BallsUp · Simulation studio", page_icon="🎯", layout="wide")
    st.markdown("""<style>
        .stApp { background: #0b1220; color: #e2e8f0; }
        [data-testid="stSidebar"] { background: #111c2e; }
        [data-testid="stMetric"] { background: #17243a; border: 1px solid #29405f;
            border-radius: 14px; padding: 18px; }
        .hero { padding: 20px 0 12px; }
        .hero h1 { font-size: 2.8rem; margin-bottom: 0; letter-spacing: -.04em; }
        .hero p { color: #94a3b8; font-size: 1.1rem; margin-top: .35rem; }
    </style>""", unsafe_allow_html=True)
    st.markdown('<div class="hero"><h1>BallsUp</h1><p>Explore the smartest floor to start a plate-break search.</p></div>',
                unsafe_allow_html=True)

    with st.sidebar:
        st.header("Simulation setup")
        st.caption("Set the ranges, then run a fresh simulation.")
        with st.form("simulation"):
            iterations = st.number_input("Iterations", min_value=1, max_value=MAX_ITERATIONS, value=1000, step=100)
            st.subheader("Ball weight · kg")
            weight_min = st.number_input("Minimum weight", min_value=0.0, value=0.5, format="%.6f")
            weight_max = st.number_input("Maximum weight", min_value=0.0, value=1.5, format="%.6f")
            st.subheader("Plate strength · N")
            strength_min = st.number_input("Minimum strength", min_value=0.0, value=4000.0, format="%.6f")
            strength_max = st.number_input("Maximum strength", min_value=0.0, value=7000.0, format="%.6f")
            st.subheader("Floor height · m")
            height_min = st.number_input("Minimum height", min_value=0.0, value=1.0, format="%.6f")
            height_max = st.number_input("Maximum height", min_value=0.0, value=3.0, format="%.6f")
            selected = st.multiselect("Strategies", list(STRATEGIES), default=list(STRATEGIES))
            submitted = st.form_submit_button("Run simulation", width="stretch", type="primary")

    if submitted:
        ranges = ((weight_min, weight_max), (strength_min, strength_max), (height_min, height_max))
        if not selected:
            st.error("Select at least one strategy.")
        else:
            try:
                with st.spinner("Running simulations across 100 floors…"):
                    results = run_simulation_with_adjusted_parameters(iterations, *ranges,
                                                                       [STRATEGIES[name] for name in selected])
            except ValueError as error:
                st.error(str(error))
            else:
                st.session_state["analysis"] = (results, iterations, ranges, len(selected))

    if "analysis" in st.session_state:
        display_results(*st.session_state["analysis"])
    else:
        st.info("Choose your parameters in the sidebar and run the simulation to see the charts and per-floor results.")


if __name__ == "__main__":
    main()
