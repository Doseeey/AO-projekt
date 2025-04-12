import itertools

from load_data import load_data
from calculate_makespan import calculate_makespan
from tabu_search import tabu_search

def find_optimal_seq(TPO, setup_times):
    permutations = list(itertools.permutations(list(range(TPO.shape[1]))))
    best_time, best_permutation = float('inf'), None

    for job_sequence in permutations:
        span = calculate_makespan(TPO, setup_times, job_sequence)
        if span < best_time or best_time == None:
            best_time = span
            best_permutation = job_sequence
    
    return best_permutation, best_time

def pfspwst(problem_from: int=1, problem_to: int=10):
    for n in range(problem_from, problem_to+1):
        TPO, setup_times = load_data(f"Problems/problem{n}.mat")

        if TPO.shape[1] <= 10:
            opt_permutation, opt_time = find_optimal_seq(TPO, setup_times)
            print(f"Optimal Problem {n}: {opt_permutation}, {opt_time}")

        best_permutation, best_time = tabu_search(TPO, setup_times, verbose=False)
        print(f"Problem {n}: {best_permutation}, {best_time}")

# TPO, setup_times = load_data("Problems/problem1.mat")
# best_permutation, best_time = tabu_search(TPO, setup_times, verbose=False)
# print(best_time, best_permutation)

pfspwst(problem_from=1, problem_to=10)