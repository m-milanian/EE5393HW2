from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BiquadState:
    B1: float = 0.0
    B2: float = 0.0


def biquad_step(u: float, state: BiquadState) -> Dict[str, float]:
    """
    Signal-level simulation of the concrete biquad CRN.

    Equations:
        X_k = u_k + B1_k/8 + B2_k/8
        Y_k = X_k/8 + B1_k/8 + B2_k/8
        B1_{k+1} = X_k
        B2_{k+1} = B1_k
    """
    B1_before = state.B1
    B2_before = state.B2

    X = u + B1_before / 8.0 + B2_before / 8.0
    Y = X / 8.0 + B1_before / 8.0 + B2_before / 8.0

    state.B1 = X
    state.B2 = B1_before

    return {
        "input": u,
        "B1_before": B1_before,
        "B2_before": B2_before,
        "X_internal": X,
        "Y_output": Y,
        "B1_after": state.B1,
        "B2_after": state.B2,
    }


def simulate_biquad(inputs: List[float]) -> List[Dict[str, float]]:
    state = BiquadState()
    results = []

    for k, u in enumerate(inputs, start=1):
        row = biquad_step(u, state)
        row["cycle"] = k
        results.append(row)

    return results


def print_table(results: List[Dict[str, float]]) -> None:
    print(
        f"{'cycle':>5} | {'input':>10} | {'B1_before':>12} | {'B2_before':>12} | "
        f"{'X_internal':>12} | {'Y_output':>14} | {'B1_after':>12} | {'B2_after':>12}"
    )
    print("-" * 105)
    for r in results:
        print(
            f"{r['cycle']:5d} | "
            f"{r['input']:10.6f} | "
            f"{r['B1_before']:12.6f} | "
            f"{r['B2_before']:12.6f} | "
            f"{r['X_internal']:12.6f} | "
            f"{r['Y_output']:14.6f} | "
            f"{r['B1_after']:12.6f} | "
            f"{r['B2_after']:12.6f}"
        )


def main() -> None:
    inputs = [100, 5, 500, 20, 250]
    results = simulate_biquad(inputs)
    print_table(results)

    print("\nOutputs only:")
    for r in results:
        print(f"Cycle {r['cycle']}: Y = {r['Y_output']}")


if __name__ == "__main__":
    main()