import numpy as np

def calculate_makespan(processing_times: np.ndarray, setup_times: np.ndarray, job_sequence: np.ndarray):
    n_machines = processing_times.shape[0]
    completion_times = np.zeros((n_machines, len(job_sequence)))

    for i, j in enumerate(job_sequence):
        for m in range(n_machines):
            if i == 0:
                setup = 0  # setup before first 
            else:
                prev_j = job_sequence[i - 1]
                # setup time needed between previous and current job of machine m (sequence-dependent)
                setup = setup_times[prev_j][j][m]
                
            #first job and first machine - input processing time of the job
            if m == 0 and i == 0:
                start_time = processing_times[m][j]
            #nth job and first machine - add processing time to previous job completion
            elif m == 0:
                start_time = completion_times[m][i - 1] + processing_times[m][j]
            #first job and nth machine - add processing time to previous machine completion
            elif i == 0:
                start_time = completion_times[m - 1][i] + processing_times[m][j]
            #nth job and nth machine - add processing time to max from either previous job/machine completion
            else:
                start_time = max(completion_times[m - 1][i], completion_times[m][i - 1]) + processing_times[m][j]

            #include setup time needed to finalize current job
            start_time += setup
            completion_times[m][i] = start_time

    return completion_times[-1][-1] 
