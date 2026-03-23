from collections import Counter
import random

def build_fibonacci_crn(num_steps=12):
    """
    Reactions for stage k:
        X_k -> T_k
        Y_k -> X_{k+1} + Y_{k+1}
        T_k -> Y_{k+1}
    """
    reactions = []
    for k in range(num_steps):
        reactions.append((Counter({f"X{k}": 1}), Counter({f"T{k}": 1})))
        reactions.append((Counter({f"Y{k}": 1}), Counter({f"X{k+1}": 1, f"Y{k+1}": 1})))
        reactions.append((Counter({f"T{k}": 1}), Counter({f"Y{k+1}": 1})))
    return reactions


def is_enabled(state, reactants):
    for sp, c in reactants.items():
        if state[sp] < c:
            return False
    return True


def fire_reaction(state, reactants, products):
    new_state = state.copy()
    for sp, c in reactants.items():
        new_state[sp] -= c
        if new_state[sp] == 0:
            del new_state[sp]
    for sp, c in products.items():
        new_state[sp] += c
    return new_state


def simulate_crn(x0, y0, num_steps=12, seed=0, verbose=False):
    random.seed(seed)
    state = Counter({f"X0": x0, f"Y0": y0})
    reactions = build_fibonacci_crn(num_steps)

    fired = 0
    while True:
        enabled = [(rct, prd) for (rct, prd) in reactions if is_enabled(state, rct)]
        if not enabled:
            break
        rct, prd = random.choice(enabled)
        state = fire_reaction(state, rct, prd)
        fired += 1
        if verbose:
            print(f"Fired: {dict(rct)} -> {dict(prd)}")
            print(f"State: {dict(state)}\n")

    return state, fired


def direct_fibonacci_pair(x0, y0, num_steps=12):
    x, y = x0, y0
    history = [(x, y)]
    for _ in range(num_steps):
        x, y = y, x + y
        history.append((x, y))
    return history


def report_case(x0, y0, num_steps=12, seed=0):
    print("=" * 60)
    print(f"Initial values: ({x0}, {y0})")
    print(f"Number of steps: {num_steps}\n")

    history = direct_fibonacci_pair(x0, y0, num_steps)
    print("Direct iteration history:")
    for k, (x, y) in enumerate(history):
        print(f"step {k:2d}: (X{k if k <= num_steps else ''}, Y{k if k <= num_steps else ''}) = ({x}, {y})")

    state, fired = simulate_crn(x0, y0, num_steps=num_steps, seed=seed, verbose=False)

    x_final = state.get(f"X{num_steps}", 0)
    y_final = state.get(f"Y{num_steps}", 0)

    print("\nCRN terminal state (nonzero species only):")
    for sp in sorted(state.keys(), key=lambda s: (s[0], int(s[1:]))):
        print(f"{sp}: {state[sp]}")

    print(f"\nTotal one-molecule reaction firings: {fired}")
    print(f"Final output after {num_steps} steps:")
    print(f"X{num_steps} = {x_final}")
    print(f"Y{num_steps} = {y_final}")

    expected_x, expected_y = history[-1]
    assert x_final == expected_x and y_final == expected_y, "CRN output does not match direct iteration."
    print("Check passed: CRN output matches direct Fibonacci iteration.\n")


if __name__ == "__main__":
    report_case(0, 1, num_steps=12, seed=1)
    report_case(3, 7, num_steps=12, seed=2)