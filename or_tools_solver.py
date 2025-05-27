from ortools.sat.python import cp_model


def solve_flowshop(TPO_float, S_float, precision=3):
    scale = 10 ** precision
    # Scale float data to integers
    TPO = [[int(round(p * scale)) for p in row] for row in TPO_float]
    S = [[[int(round(s * scale)) for s in row] for row in mat] for mat in S_float]

    num_machines = len(TPO)
    num_jobs = len(TPO[0])
    max_time = sum(map(sum, TPO)) + max(map(max, map(max, S))) * num_jobs  # a safe upper bound

    model = cp_model.CpModel()
    start = {}
    end = {}
    intervals = {}

    for j in range(num_jobs):
        for m in range(num_machines):
            start[(j, m)] = model.NewIntVar(0, max_time, f'start_j{j}_m{m}')
            end[(j, m)] = model.NewIntVar(0, max_time, f'end_j{j}_m{m}')
            intervals[(j, m)] = model.NewIntervalVar(
                start[(j, m)], TPO[m][j], end[(j, m)], f'int_j{j}_m{m}'
            )

    order = {}
    for i in range(num_jobs):
        for j in range(i + 1, num_jobs):
            o_ij = model.NewBoolVar(f'order_{i}_before_{j}')
            o_ji = model.NewBoolVar(f'order_{j}_before_{i}')
            order[(i, j)] = o_ij
            order[(j, i)] = o_ji
            model.Add(o_ij + o_ji == 1)

    for m in range(num_machines):
        for i in range(num_jobs):
            for j in range(i + 1, num_jobs):
                o_ij = order[(i, j)]
                o_ji = order[(j, i)]
                model.Add(end[(i, m)] + S[i][j][m] <= start[(j, m)]).OnlyEnforceIf(o_ij)
                model.Add(end[(j, m)] + S[j][i][m] <= start[(i, m)]).OnlyEnforceIf(o_ji)

    for m in range(num_machines):
        model.AddNoOverlap([intervals[(j, m)] for j in range(num_jobs)])

    for j in range(num_jobs):
        for m in range(num_machines - 1):
            model.Add(end[(j, m)] <= start[(j, m + 1)])

    makespan = model.NewIntVar(0, max_time, 'makespan')
    model.AddMaxEquality(makespan, [end[(j, num_machines - 1)] for j in range(num_jobs)])
    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        seq = sorted(range(num_jobs), key=lambda j: solver.Value(start[(j, 0)]))
        best_permutation = seq
        best_time = solver.Value(makespan) / scale
        return best_permutation, best_time
    else:
        print('No solution found.')
        return None, None
