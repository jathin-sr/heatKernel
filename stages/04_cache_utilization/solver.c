// stages/01_c_baseline/solver.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../src/core/timing.h"
#include "../../src/core/grid_management.h"
#include "../../src/core/boundary_conditions.h"
#include "../../src/core/stencil_ops.h"
#include "../../src/core/metrics.h"

int main(int argc, char *argv[])
{
    int size = atoi(argv[1]);
    int timesteps = atoi(argv[2]);
    double alpha = atof(argv[3]);
    double dx = atof(argv[4]);
    const char *output_dir = argv[5];

    double dt = 0.24 * dx * dx / alpha; // to ensure stability

    double **T = grid_create_ptr(size);
    double **T_new = grid_create_ptr(size);

    int center = size / 2;
    T[center][center] = 100.0;

    struct timespec start, end;
    struct timespec stencil_start, stencil_end;
    struct timespec boundary_start, boundary_end;
    struct timespec swap_start, swap_end;

    double total_stencil_time = 0.0;
    double total_boundary_time = 0.0;
    double total_swap_time = 0.0;

    get_time(&start);

    for (int step = 0; step < timesteps; step++)
    {
        get_time(&stencil_start);
        for (int i = 1; i < size - 1; i++)
        {
            for (int j = 1; j < size - 1; j++)
            {
                T_new[i][j] = heat_stencil(T[i][j], T[i + 1][j], T[i - 1][j], T[i][j + 1], T[i][j - 1], alpha, dt, dx);
            }
        }
        get_time(&stencil_end);
        total_stencil_time += time_diff(&stencil_start, &stencil_end);

        // Boundaries
        get_time(&boundary_start);
        neumann_boundaries_ptr(T_new, size);
        get_time(&boundary_end);
        total_boundary_time += time_diff(&boundary_start, &boundary_end);

        // Swapping
        get_time(&swap_start);
        double **tmp = T;
        T = T_new;
        T_new = tmp;
        get_time(&swap_end);
        total_swap_time += time_diff(&swap_start, &swap_end);
    }

    get_time(&end);
    double total_time = time_diff(&start, &end);
    double other_time = total_time - total_boundary_time - total_stencil_time - total_swap_time;

    // Saving
    save_metrics_detailed(output_dir, total_time, total_stencil_time, total_boundary_time, total_swap_time, other_time, size, timesteps, "01_c_baseline");

    // Cleanup
    grid_destroy_ptr(T, size);
    grid_destroy_ptr(T_new, size);

    return 0;
}