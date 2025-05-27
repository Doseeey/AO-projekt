from proper_cm import calculate_makespan
import itertools


def find_optimal_seq(TPO, setup_times):
    permutations = list(itertools.permutations(list(range(TPO.shape[1]))))
    best_time, best_permutation = float('inf'), None

    for job_sequence in permutations:
        span = calculate_makespan(TPO, setup_times, job_sequence)
        if span < best_time or best_time == None:
            best_time = span
            best_permutation = job_sequence

    return best_permutation, best_time
