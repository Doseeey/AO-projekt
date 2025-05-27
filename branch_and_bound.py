from proper_cm import calculate_makespan
from collections import deque


def lower_bound(partial_seq, remaining_jobs, P, S):
    current_cost = calculate_makespan(P, S, partial_seq)
    min_additional_cost = 0

    for job in remaining_jobs:
        min_proc = P[:, job].min()
        if partial_seq:
            prev_job = partial_seq[-1]
            min_setup = S[prev_job, job, :].min()
        else:
            min_setup = S[:, job, :].min()
        min_additional_cost += (min_proc + min_setup)

    return current_cost + min_additional_cost


def branch_and_bound_recursive(P, S, verbose=False):
    n_jobs = P.shape[1]
    best_makespan = float('inf')
    best_sequence = None
    count = 0

    def recurse(partial_seq, remaining_jobs):
        nonlocal best_makespan, best_sequence, count

        if not remaining_jobs:
            ms = calculate_makespan(P, S, partial_seq)
            if ms < best_makespan:
                best_makespan = ms
                best_sequence = list(partial_seq)
            return

        bound = lower_bound(partial_seq, remaining_jobs, P, S)
        if bound >= best_makespan:
            count += 1
            return

        for job in remaining_jobs:
            recurse(partial_seq + [job], [j for j in remaining_jobs if j != job])

    recurse([], list(range(n_jobs)))
    if verbose:
        print("Branch & Bound count:", count)
    return best_sequence, best_makespan


def branch_and_bound(P, S, verbose=False):
    n_jobs = P.shape[1]
    best_makespan = float('inf')
    best_sequence = None
    count = 0  # liczba przyciętych gałęzi

    stack = deque()
    stack.append(([], list(range(n_jobs))))  # początkowy stan

    while stack:
        partial_seq, remaining_jobs = stack.pop()

        if not remaining_jobs:
            ms = calculate_makespan(P, S, partial_seq)
            if ms < best_makespan:
                best_makespan = ms
                best_sequence = list(partial_seq)
            continue

        bound = lower_bound(partial_seq, remaining_jobs, P, S)
        if bound >= best_makespan:
            count += 1
            continue

        for job in remaining_jobs:
            new_partial = partial_seq + [job]
            new_remaining = [j for j in remaining_jobs if j != job]
            stack.append((new_partial, new_remaining))

    if verbose:
        print("Branch & Bound count:", count)

    return best_sequence, best_makespan
