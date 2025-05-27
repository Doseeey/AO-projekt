import numpy as np


def calculate_makespan(processing_times, setup_times, job_sequence):
    if job_sequence is None or len(job_sequence) == 0:
        return 0.0
    n_machines = processing_times.shape[0]
    completion_times = np.zeros((n_machines, len(job_sequence)))

    for i, j in enumerate(job_sequence):
        for m in range(n_machines):
            if i == 0:
                setup = 0
            else:
                prev_j = job_sequence[i - 1]
                setup = setup_times[prev_j][j][m]

            if m == 0 and i == 0:
                start_time = 0
            elif m == 0:
                start_time = completion_times[m][i - 1] + setup
            elif i == 0:
                start_time = completion_times[m - 1][i]
            else:
                start_time = max(completion_times[m - 1][i], completion_times[m][i - 1] + setup)

            completion_times[m][i] = start_time + processing_times[m][j]

    return completion_times[-1][-1]
