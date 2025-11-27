#ifndef METRICS_H
#define METRICS_H

#include <stdio.h>
#include <stdlib.h>

static inline void save_metrics_detailed(const char *output_dir, double total_time, double stencil_time,
                                         double boundary_time, double swap_time, double other_time, int size, int timesteps, const char *stage_name)
{
    char filename[256];
    snprintf(filename, sizeof(filename), "%s/metrics.json", output_dir);

    FILE *file = fopen(filename, "w");
    if (file)
    {
        fprintf(file, "{\n");
        fprintf(file, "  \"stage\": \"%s\",\n", stage_name);
        fprintf(file, "  \"grid_size\": %d,\n", size);
        fprintf(file, "  \"time_steps\": %d,\n", timesteps);
        fprintf(file, "  \"total_time\": %.6f,\n", total_time);
        fprintf(file, "  \"time_per_step\": %.6f,\n", total_time / timesteps * 1000);
        fprintf(file, "  \"performance\": %.6f,\n", timesteps / total_time);
        fprintf(file, "  \"breakdown\": {\n");
        fprintf(file, "    \"stencil_time\": %.6f,\n", stencil_time);
        fprintf(file, "    \"boundary_time\": %.6f,\n", boundary_time);
        fprintf(file, "    \"swap_time\": %.6f,\n", swap_time);
        fprintf(file, "    \"other_time\": %.6f\n", other_time);
        fprintf(file, "  }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
}

#endif