#ifndef GRID_MANAGEMENT_H
#define GRID_MANAGEMENT_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

static inline double **grid_create_ptr(int size)
{
    double **ptr = (double **)malloc(size * sizeof(double *));
    for (int i = 0; i < size; i++)
    {
        ptr[i] = (double *)calloc(size, sizeof(double));
    }
    return ptr;
}

static inline void grid_destroy_ptr(double **ptr, int size)
{
    for (int i = 0; i < size; i++)
    {
        free(ptr[i]);
    }
    free(ptr);
}

static inline double *grid_create_contig(int size)
{
    double *ptr = (double *)malloc(size * size * sizeof(double));
    memset(ptr, 0, size * size * sizeof(double));
    return ptr;
}

static inline void grid_destroy_contig(double *ptr)
{
    free(ptr);
}

#endif