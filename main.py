from load_data import load_data
from calculate_makespan import calculate_makespan
import itertools
from tabu_search import tabu_search

# def find_optimal_seq(TPO, setup_times):
#     permutations = list(itertools.permutations(list(range(TPO.shape[1]))))
#     best_time, best_permutation = float('inf'), None

#     for job_sequence in permutations:
#         span = calculate_makespan(TPO, setup_times, job_sequence)
#         if span < best_time or best_time == None:
#             best_time = span
#             best_permutation = job_sequence
    
#     return best_time, best_permutation


# #Only for smallest problems
# # opt_time, opt_permutation = find_optimal_seq(TPO, setup_times)
# # print(opt_time, opt_permutation)

def pfspwst(problem_from: int=1, problem_to: int=800):
    for n in range(problem_from, problem_to+1):
        TPO, setup_times = load_data(f"Problems/problem{n}.mat")
        best_permutation, best_time = tabu_search(TPO, setup_times, verbose=False)
        print(f"Problem {n}: {best_permutation}, {best_time}")

# TPO, setup_times = load_data("Problems/problem1.mat")

# best_permutation, best_time = tabu_search(TPO, setup_times, verbose=False)

# print(best_time, best_permutation)

pfspwst()