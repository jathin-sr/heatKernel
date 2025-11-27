#ifndef BOUNDARY_CONDITIONS_H
#define BOUNDARY_CONDITIONS_H

#include <stdlib.h>

static inline void neumann_boundaries_ptr(double **data, int size)
{
    for (int i = 0; i < size; i++)
    {
        data[i][0] = data[i][1];               // left
        data[i][size - 1] = data[i][size - 2]; // right
    }
    for (int j = 0; j < size; j++)
    {
        data[0][j] = data[1][j];               // top
        data[size - 1][j] = data[size - 2][j]; // bottom
    }
}

static inline void neumann_boundaries_contig(double *data, int size)
{
    for (int i = 0; i < size; i++)
    {
        data[i * size] = data[i * size + 1];                   // left
        data[i * size + size - 1] = data[i * size + size - 2]; // right
    }

    for (int j = 0; j < size; j++)
    {
        data[j] = data[size + j];                                  // top
        data[(size - 1) * size + j] = data[(size - 2) * size + j]; // bottom
    }
}

#endif