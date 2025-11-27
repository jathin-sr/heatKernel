#ifndef STENCIL_OPS_H
#define STENCIL_OPS_H

static inline double heat_stencil(double center, double left, double right,
                                  double top, double bottom,
                                  double alpha, double dt, double dx)
{
    return center + alpha * dt / (dx * dx) * (left + right + top + bottom - 4.0 * center);
}

#endif