#ifndef TIMING_H
#define TIMING_H

#include <time.h>
#include <sys/time.h>

static inline void get_time(struct timespec *ts)
{
    clock_gettime(CLOCK_MONOTONIC, ts);
}

static inline double time_diff(struct timespec *start, struct timespec *end)
{
    return (end->tv_sec - start->tv_sec) + (end->tv_nsec - start->tv_nsec) / 1e9;
}

#endif