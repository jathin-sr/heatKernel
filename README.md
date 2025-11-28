# heatKernel

Performance Engineering of a Finite Difference Stencil Kernel

![heatKernel](results/archive/results_20251127_222556/performance_plots/complete_optimization_journey.png)

---

**Updates**: This project is in continuous state and more stages will be added based on my learnings

---

This project benchmarks and optimizes a **2D heat equation finite-difference stencil**, a memory-bound kernel central to scientific computing and HPC microbenchmarks. The repository includes Python, C, and progressively optimized implementations.


## Mathematical Model

**Governing PDE:**
```
∂T/∂t = α (∂²T/∂x² + ∂²T/∂y²)
```

**Discretization (5-point stencil):**
```
T(i,j)^{n+1} = T(i,j)^n + αΔt * ((T(i+1,j) + T(i-1,j) + T(i,j+1) + T(i,j-1) − 4*T(i,j)) / Δx²)
```

**Stability Criterion:**
```
Δt ≤ Δx² / (4α)
```

## Repository Layout
```text
.
├── src/                                   #C source files for optimization stages
│   ├── core/                              #common C functions for all stages
│   ├── utils/                             #report-generation helpers
│   └── visualization/                     #plot-generation functions
│
├── stages/                                #stage-wise implementations
│
├── results/
│   └── archive/                           #historical results
│       └── results_{timestamp}/           #all results from a specific run
│           └── performance_plots/         #all plots from the specific run
│           └── stage_results/             #all stage results from the specific run
│           └── pipeline_summary.md        #summary of the specific run
│
├── Makefile                               #main orchestrator
├── pipeline.mk                            #pipeline automation
└── config.mk                              #grid, steps, compiler configuration
```

## Optimization Stages
- 00_python_baseline: pure Python/NumPy reference.  
- 01_c_baseline: direct C translation.  
- 02_compiler_O3: `-O3` and `-march=native`.  
- 03_loop: loop reversing  
- 04_cache_utilization: unnecessary matrix computation improvements.  
- 05_contiguous_memory: AoS→SoA.  
- 06_cache_blocking: temporal and spatial blocking for better cache fit.  
- 07_vectorization: nforced SIMD via clang loop-vectorization pragmas.  
- 08_openmp_parallel: multithreaded version.  
- 09_arch_specific: final hardware-tuned variant.  

## Running the Pipeline

Run entire pipeline:  
```sh
make run
```

Generate plots for the latest results:  
```sh
make plots
```

Archive the latest results:  
```sh
make archive
```

Clear the latest results directory:  
```sh
make clear
```

Dependencies: GCC or Clang, OpenMP support, Python 3.x, NumPy, Make.  
Python dependencies are listed in `requirements.txt`.

## Performance Results

### Summary Table for grid size = 500
| Stage | Time (s) | Time/Step (ms) | Performance (steps/s) |
|-------|----------|----------------|----------------------|
| 00_python_baseline | 2630.50918507576 | 131.525459253788 | 7.6030907299 |
| 01_c_baseline | 28.582657 | 1.429133 | 699.725012 |
| 02_compiler_O3 | 25.335345 | 1.266767 | 789.410999 |
| 03_loop | 5.238677 | 0.261934 | 3817.757804 |
| 04_cache_utilization | 1.475546 | 0.073777 | 13554.304644 |
| 05_contiguous_memory | 1.071941 | 0.053597 | 18657.743290 |
| 06_cache_blocking | 1.002275 | 0.050114 | 19954.603278 |
| 07_vectorization | 0.971561 | 0.048578 | 20585.429016 |
| 08_openmp_parallel | 0.238776 | 0.011939 | 83760.511944 |
| 09_arch_specific | 0.239977 | 0.011999 | 83341.320210 | 

For detailed performance results for grid size 100, see the [pipeline summary](results/archive/results_20251125_225537/pipeline_summary.md).

For detailed performance results for grid size 200, see the [pipeline summary](results/archive/results_20251127_223540/pipeline_summary.md).

### Scaling 
Plot for grid size 100:  
![heatKernel](results/archive/results_20251125_225537/performance_plots/complete_optimization_journey.png) 

Plot for grid size 200:  
![heatKernel](results/archive/results_20251127_223540/performance_plots/complete_optimization_journey.png) 

Plot for grid size 500:  
![heatKernel](results/archive/results_20251127_222556/performance_plots/complete_optimization_journey.png) 

## Hardware Details
- CPU: M4 ARMv9.2-A with 3nm proces tech
- Cores: 10 [4 performance (P) / 6 efficiency (E)]
- L1 cache(KB): 128 (P)/64 (E)
- L2 cache(MB): 16 (P)/4 (E)
- GPU cores: 8
- Theoritical FP32 FLOPS (TFLOPS): 4.26
- Compiler: GCC and clang  
- OS: macos  

## Future Work
- 3D stencil solver
- Roofline performance model
- MPI multi-node version 

## Authors

- [@jathin-sr](https://www.github.com/jathin-sr) 

## License
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
