from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class BiquadState:
    """
    B1 and B2 are the two stored delay values available at the beginning of a cycle.
    """
    B1: float = 0.0
    B2: float = 0.0


def biquad_cycle(u: float, state: BiquadState) -> Tuple[float, float, BiquadState]:
    """
    One RGB cycle of the biquad filter.

    Equations inferred from Figure 2(b):
        X_k = u_k + B1_k/8 + B2_k/8
        Y_k = X_k/8 + B1_k/8 + B2_k/8
        B1_{k+1} = X_k
        B2_{k+1} = B1_k
    """
    X = u + state.B1 / 8.0 + state.B2 / 8.0
    Y = X / 8.0 + state.B1 / 8.0 + state.B2 / 8.0

    new_state = BiquadState(B1=X, B2=state.B1)
    return X, Y, new_state


def simulate_biquad(inputs: List[float]) -> List[dict]:
    """
    Simulate the filter for a list of inputs.
    """
    state = BiquadState(B1=0.0, B2=0.0)
    results = []

    for k, u in enumerate(inputs, start=1):
        B1_old = state.B1
        B2_old = state.B2

        X, Y, state = biquad_cycle(u, state)

        results.append({
            "cycle": k,
            "input": u,
            "B1_before": B1_old,
            "B2_before": B2_old,
            "X_internal": X,
            "Y_output": Y,
            "B1_after": state.B1,
            "B2_after": state.B2,
        })

    return results


def print_results(results: List[dict]) -> None:
    print(
        f"{'cycle':>5} | {'input':>10} | {'B1_before':>12} | {'B2_before':>12} | "
        f"{'X_internal':>12} | {'Y_output':>14} | {'B1_after':>12} | {'B2_after':>12}"
    )
    print("-" * 105)

    for row in results:
        print(
            f"{row['cycle']:5d} | "
            f"{row['input']:10.6f} | "
            f"{row['B1_before']:12.6f} | "
            f"{row['B2_before']:12.6f} | "
            f"{row['X_internal']:12.6f} | "
            f"{row['Y_output']:14.6f} | "
            f"{row['B1_after']:12.6f} | "
            f"{row['B2_after']:12.6f}"
        )


def main() -> None:
    inputs = [100, 5, 500, 20, 250]
    results = simulate_biquad(inputs)
    print_results(results)

    print("\nOutputs only:")
    outputs = [row["Y_output"] for row in results]
    for k, y in enumerate(outputs, start=1):
        print(f"Cycle {k}: Y = {y}")


if __name__ == "__main__":
    main()