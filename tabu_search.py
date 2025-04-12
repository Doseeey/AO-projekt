from calculate_makespan import calculate_makespan
import numpy as np

def tabu_search(processing_times: np.ndarray, setup_times: np.ndarray, max_iter: int=100, tabu_size: int=10, verbose: bool=True):
    n_jobs = processing_times.shape[1]

    #random starting point x0
    current_solution = np.random.permutation(n_jobs)

    best_solution = current_solution
    best_makespan = calculate_makespan(processing_times, setup_times, best_solution)

    tabu_list = []

    for n in range(max_iter):
        neighborhood = [] #(neighbor, makespan, move)

        #generate neighborhood
        for i in range(n_jobs):
            for j in range(i+1, n_jobs):
                if (i, j) not in tabu_list:
                    neighbor = current_solution.copy()

                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbor_makespan = calculate_makespan(processing_times, setup_times, neighbor)

                    move = (i, j)

                    neighborhood.append((neighbor, neighbor_makespan, move))
                    

        if not neighborhood:
            if verbose:
                print(f"Iteration {n}: No move available.")
            break

        #get the best solution from neighborhood
        neighborhood.sort(key=lambda x: x[1])
        current_solution, current_makespan, current_move = neighborhood[0]
        
        if current_makespan < best_makespan:
            best_solution, best_makespan = current_solution, current_makespan
            tabu_list = []

        tabu_list.append(current_move)

        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        
        if verbose:
            print(f"Iteration {n}: Current best solution {best_makespan:.2f}")

    
    return best_solution, best_makespan
