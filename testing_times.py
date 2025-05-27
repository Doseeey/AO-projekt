import time
from load_data import load_data
from solvers import or_tools_solver, tabu_search, branch_and_bound, brute_force


def benchmark_solver(name, solver_func, *args, **kwargs):
    start = time.time()
    sequence, makespan = solver_func(*args, **kwargs)
    end = time.time()
    duration = end - start
    sequence = [int(x) for x in sequence]
    print(f"{name}: | Makespan: {makespan:.4f} | Time: {duration:.4f} seconds | Sequence: {sequence}")
    return sequence, makespan, duration


if __name__ == "__main__":
    data = [(n, load_data(f"Problems/problem{n}.mat")) for n in [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]]

    for i, (TPO, S) in data:
        print(f"\n\nProblem {i}:")
        benchmark_solver("OR-Tools      ", or_tools_solver, TPO, S, precision=5)
        benchmark_solver("Tabu Search   ", tabu_search, TPO, S, verbose=False)
        if TPO.shape[1] <= 10:
            benchmark_solver("Brute Force   ", brute_force, TPO, S)
            benchmark_solver("Branch & Bound", branch_and_bound, TPO, S)
