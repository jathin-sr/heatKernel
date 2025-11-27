import json
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_thread_scaling(results_dir="results/latest/stage_results/08_openmp_parallel", output_dir="results/latest/performance_plots"):
    """Plot OpenMP thread scaling analysis"""
    os.makedirs(output_dir, exist_ok=True)
    
    threads = []
    performances = []
    total_times = []
    efficiencies = []
    
    # Find all thread directories
    thread_dirs = glob.glob(f"{results_dir}/threads_*")
    
    for thread_dir in sorted(thread_dirs, key=lambda x: int(x.split('_')[-1])):
        metrics_file = os.path.join(thread_dir, "metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file) as f:
                data = json.load(f)
                
                # Extract thread count from directory name
                thread_count = int(os.path.basename(thread_dir).split('_')[-1])
                threads.append(thread_count)
                
                # Get performance data
                performances.append(data['performance'])
                total_times.append(data['total_time'])
    
    if not threads:
        print("No thread scaling data found!")
        return
    
    # Calculate speedup and efficiency
    single_thread_time = None
    single_thread_perf = None
    
    # Find single thread data
    for i, thread_count in enumerate(threads):
        if thread_count == 1:
            single_thread_time = total_times[i]
            single_thread_perf = performances[i]
            break
    
    if single_thread_time is None:
        print("Single thread data not found!")
        return
    
    # Calculate speedup and efficiency
    speedups = [single_thread_time / time for time in total_times]
    efficiencies = [(speedup / thread_count) * 100 for speedup, thread_count in zip(speedups, threads)]
    
    # Create subplots
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(30, 10))
    
    # Plot 1: Performance vs Threads
    ax1.plot(threads, performances, 'bo-', linewidth=2, markersize=6)
    ax1.set_xlabel('Number of Threads')
    ax1.set_ylabel('Performance (steps/second)')
    ax1.set_title('OpenMP Thread Scaling: Performance', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(threads)

    # Mark optimal thread count
    optimal_idx = np.argmax(performances)
    ax1.plot(threads[optimal_idx], performances[optimal_idx], 'ro', markersize=10, 
             label=f'Optimal: {threads[optimal_idx]} threads\n({performances[optimal_idx]:,.0f} steps/s)')
    ax1.legend()
    
    # Add value labels for key points
    for i, (thread, perf) in enumerate(zip(threads, performances)):
        if thread in [1, 2, 4, 8, threads[optimal_idx]]:
            ax1.annotate(f'{perf:,.0f}', (thread, perf), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=9)
    
    # Plot 2: Speedup vs Threads
    ax2.plot(threads, speedups, 'ro-', linewidth=2, markersize=6, label='Actual Speedup')
    ax2.set_xlabel('Number of Threads')
    ax2.set_ylabel('Speedup (vs Single Thread)')
    ax2.set_title('OpenMP Thread Scaling: Speedup', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(threads)
    ax2.legend()

    # Mark optimal speedup
    ax2.plot(threads[optimal_idx], speedups[optimal_idx], 'ro', markersize=10,
             label=f'Optimal: {speedups[optimal_idx]:.1f}x')
    
    # Add overall analysis
    fig.suptitle(f'OpenMP Thread Scaling Analysis\nOptimal: {threads[optimal_idx]} threads', 
                 fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/thread_scaling_analysis.png', dpi=150, bbox_inches='tight')

if __name__ == "__main__":
    plot_thread_scaling()