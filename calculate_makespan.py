import numpy as np

def calculate_makespan(processing_times, setup_times, job_sequence):
    num_machines, num_jobs = processing_times.shape
    completion_times = np.zeros((num_machines, len(job_sequence)))

    for i, job in enumerate(job_sequence):
        for m in range(num_machines):
            if i == 0:
                setup = 0  # setup before first 
            else:
                prev_job = job_sequence[i - 1]
                # setup time needed between previous and current job of machine m
                setup = setup_times[prev_job][job][m]

            if m == 0:
                start_time = completion_times[m][i - 1] if i > 0 else 0
            else:
                start_time = max(completion_times[m - 1][i], completion_times[m][i - 1] if i > 0 else 0)

            start_time += setup
            completion_times[m][i] = start_time + processing_times[m][job]

    return completion_times[-1][-1] 
