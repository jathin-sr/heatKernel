import os
import time
import json
import numpy as np
import argparse

def heat_equation_solver(size=100, timesteps=250, alpha=0.2, dx=0.01):

    dt = 0.24 * dx * dx / alpha
    T = np.zeros((size, size))
    center = size // 2
    T[center, center] = 100.0
    
    total_stencil_time = 0.0
    total_boundary_time = 0.0
    total_swap_time = 0.0
    
    start_time = time.time()

    for step in range(1, timesteps + 1):
        T_new = np.zeros_like(T)
        
        start_stencil_time = time.time()
        for i in range(1, size-1):
            for j in range(1, size-1):
                T_new[i,j] = T[i,j] + alpha * dt/(dx*dx) * (T[i+1,j] + T[i-1,j] + T[i,j+1] + T[i,j-1] - 4*T[i,j])
        total_stencil_time += time.time() - start_stencil_time
        
        start_boundary_time = time.time()
        T_new[0,:] = T_new[1,:]
        T_new[-1,:] = T_new[-2,:]  
        T_new[:,0] = T_new[:,1]
        T_new[:,-1] = T_new[:,-2]
        total_boundary_time += time.time() - start_boundary_time

        start_swap_time = time.time()
        T = T_new
        total_swap_time += time.time() - start_swap_time
    
    total_time = time.time() - start_time

    return {
            'total_time': total_time,
            'stencil_time': total_stencil_time,
            'boundary_time': total_boundary_time,
            'swap_time': total_swap_time,
            'other_time': total_time - total_stencil_time - total_boundary_time - total_swap_time,
        }

parser = argparse.ArgumentParser(description='PDE Solver - Python Baseline')
parser.add_argument('--size', type=int, default=100)
parser.add_argument('--timesteps', type=int, default=200)
parser.add_argument('--alpha', type=float, default=0.2)
parser.add_argument('--dx', type=float, default=0.01)
parser.add_argument('--output-dir', default='.')
args = parser.parse_args()

print(f"Running 00_python_baseline with grid= {args.size}, steps={args.timesteps}")
results = heat_equation_solver(args.size, args.timesteps, args.alpha, args.dx)

# Metrics
os.makedirs(args.output_dir, exist_ok=True)
with open(f'{args.output_dir}/metrics.json', 'w') as f:
    json.dump({
        'stage': 'python_baseline',
        'grid_size': args.size,
        'time_steps': args.timesteps,
        'total_time': results['total_time'],
        'time_per_step': results['total_time'] / args.timesteps * 1000,
        'performance': args.timesteps / results['total_time'],
        'breakdown': {
            'stencil_time': results['stencil_time'],
            'boundary_time': results['boundary_time'],
            'swap_time': results['swap_time'],
            'other_time': results['other_time'],
        }
    }, f, indent=2)