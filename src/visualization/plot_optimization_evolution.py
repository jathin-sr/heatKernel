import json
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_optimization_journey(results_dir="results/latest", output_dir="results/latest/performance_plots"):
    """Plot complete optimization journey with line+bar combination"""
    os.makedirs(output_dir, exist_ok=True)
    
    stages = []
    stage_names = []  # Clean names for display
    performances = []
    times_per_step = []
    
    # Get all stage directories in order
    stage_dirs = []
    for i in range(0, 10):  # 00 to 09
        stage_dir = f"{results_dir}/stage_results/{i:02d}_*"
        matching_dirs = glob.glob(stage_dir)
        if matching_dirs:
            stage_dirs.append(matching_dirs[0])
    
    # Special handling for OpenMP - use best thread performance
    openmp_best_performance = 0
    openmp_best_dir = None
    
    # Find best OpenMP thread performance
    openmp_threads_dir = f"{results_dir}/stage_results/08_openmp_parallel"
    if os.path.exists(openmp_threads_dir):
        thread_dirs = glob.glob(f"{openmp_threads_dir}/threads_*")
        for thread_dir in thread_dirs:
            metrics_file = os.path.join(thread_dir, "metrics.json")
            if os.path.exists(metrics_file):
                with open(metrics_file) as f:
                    data = json.load(f)
                    if data['performance'] > openmp_best_performance:
                        openmp_best_performance = data['performance']
                        openmp_best_dir = thread_dir

    # Special handling for M4 architecture - use best thread performance
    arch_best_performance = 0
    arch_best_dir = None

    # Find best OpenMP thread performance
    arch_threads_dir = f"{results_dir}/stage_results/09_arch_specific"
    if os.path.exists(arch_threads_dir):
        thread_dirs = glob.glob(f"{arch_threads_dir}/threads_*")
        for thread_dir in thread_dirs:
            metrics_file = os.path.join(thread_dir, "metrics.json")
            if os.path.exists(metrics_file):
                with open(metrics_file) as f:
                    data = json.load(f)
                    if data['performance'] > arch_best_performance:
                        arch_best_performance = data['performance']
                        arch_best_dir = thread_dir
    
    # Load data for all stages
    for stage_dir in stage_dirs:
        stage_name = os.path.basename(stage_dir)
        
        # For OpenMP, use best thread performance
        if stage_name.startswith('08_') and openmp_best_dir:
            metrics_file = os.path.join(openmp_best_dir, "metrics.json")
            if os.path.exists(metrics_file):
                with open(metrics_file) as f:
                    data = json.load(f)
                    stages.append(stage_name)
                    stage_names.append(f"Stage 8")  # Simple stage number
                    performances.append(data['performance'])
                    times_per_step.append(data['time_per_step'])
                    continue
        
        if stage_name.startswith('09_') and arch_best_dir:
            metrics_file = os.path.join(arch_best_dir, "metrics.json")
            if os.path.exists(metrics_file):
                with open(metrics_file) as f:
                    data = json.load(f)
                    stages.append(stage_name)
                    stage_names.append(f"Stage 9")  # Simple stage number
                    performances.append(data['performance'])
                    times_per_step.append(data['time_per_step'])
                    continue
        
        # For other stages, use normal metrics
        metrics_file = os.path.join(stage_dir, "metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file) as f:
                data = json.load(f)
                stages.append(stage_name)
                
                # Create simple stage numbers
                if stage_name.startswith('00_'):
                    clean_name = "Stage 0"
                elif stage_name.startswith('01_'):
                    clean_name = "Stage 1" 
                elif stage_name.startswith('02_'):
                    clean_name = "Stage 2"
                elif stage_name.startswith('03_'):
                    clean_name = "Stage 3"
                elif stage_name.startswith('04_'):
                    clean_name = "Stage 4"
                elif stage_name.startswith('05_'):
                    clean_name = "Stage 5"
                elif stage_name.startswith('06_'):
                    clean_name = "Stage 6"
                elif stage_name.startswith('07_'):
                    clean_name = "Stage 7"
                elif stage_name.startswith('08_'):
                    clean_name = "Stage 8"
                elif stage_name.startswith('09_'):
                    clean_name = "Stage 9"
                
                stage_names.append(clean_name)
                performances.append(data['performance'])
                times_per_step.append(data['time_per_step'])
    
    if not stages:
        print("No stage results found!")
        return
    
    # Create unique colors for each stage
    colors = plt.cm.Set3(np.linspace(0, 1, len(stages)))
    
    # Calculate metrics
    baseline_perf = performances[0]
    speedups = [perf / baseline_perf for perf in performances]
    
    # Create the combined plot (only 2 subplots)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    
    # Plot 1: Performance progression (Line + Bar)
    x_pos = np.arange(len(stages))
    width = 0.6
    
    # Bar chart for absolute performance
    bars = ax1.bar(x_pos, performances, width=width, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('Performance (steps/second)', fontweight='bold', fontsize=12)
    ax1.set_title('Complete Optimization Journey: Absolute Performance', 
                  fontweight='bold', fontsize=16, pad=20)
    
    # Line chart above bars for trend (offset upward)
    line_y_offset = max(performances) * 0.10  # 5% above highest bar
    line_y_values = [perf + line_y_offset for perf in performances]
    
    ax1.plot(x_pos, line_y_values, 'ro-', linewidth=3, markersize=10, 
             markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2)
    
    # Add arrows connecting line to bars
    """for i, (line_y, bar_y) in enumerate(zip(line_y_values, performances)):
        ax1.annotate('', 
                    xy=(i, bar_y),           # Arrow end point (top of bar)
                    xytext=(i, line_y),      # Arrow start point (line point)
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5, alpha=0.7))"""
    
    # Customize x-axis - use simple stage numbers as labels
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(stage_names, rotation=0, ha='center', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, perf) in enumerate(zip(bars, performances)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{perf:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Add improvement annotations (without arrows)
    improvements = [0]  # Baseline has 0% improvement
    for i in range(1, len(performances)):
        improvement = (performances[i] / performances[i-1] - 1) * 100
        improvements.append(improvement)
        
        if improvement > 1:  # Only show significant improvements
            ax1.text(i, performances[i] + (line_y_offset * 1.5),  # Position above bar but below line
                    f'+{improvement:.0f}%', 
                    ha='center', va='top',
                    fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
        else:  # Only show significant improvements
            ax1.text(i, performances[i] + (line_y_offset * 0.5),  # Position above bar but below line
                    f'{improvement:.0f}%', 
                    ha='center', va='bottom',
                    fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))

    # Plot 2: Cumulative Speedup (Bar chart only - no lines, no legend)
    bars2 = ax2.bar(x_pos, speedups, width=width, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('Speedup vs Baseline (x times faster)', fontweight='bold', fontsize=12)
    ax2.set_title('Cumulative Speedup Progression', fontweight='bold', fontsize=16, pad=20)
    
    # Use simple stage numbers as x-axis labels
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(stage_names, rotation=0, ha='center', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (bar, speedup) in enumerate(zip(bars2, speedups)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{speedup:.1f}x', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    # Save plots
    plt.savefig(f'{output_dir}/complete_optimization_journey.png', dpi=150, bbox_inches='tight')
    #plt.show()
    
    # Print comprehensive analysis
    print("="*90)
    print("COMPLETE OPTIMIZATION JOURNEY ANALYSIS")
    print("="*90)
    print(f"{'Stage':<15} {'Performance':<15} {'Speedup':<10} {'Improvement':<12}")
    print("-"*90)
    
    for i, (stage_name, perf, speedup, imp) in enumerate(zip(stage_names, performances, speedups, improvements)):
        if i == 0:
            print(f"{stage_name:<15} {perf:>14,.0f} {speedup:>9.1f}x {'Baseline':>12}")
        else:
            print(f"{stage_name:<15} {perf:>14,.0f} {speedup:>9.1f}x {imp:>11.1f}%")
    
    print("-"*90)
    total_speedup = speedups[-1]
    print(f"{'FINAL RESULT':<15} {performances[-1]:>14,.0f} {total_speedup:>9.1f}x")
    print("="*90)
    
    # Print OpenMP thread info if available
    if openmp_best_performance > 0:
        if openmp_best_dir:
            thread_count = os.path.basename(openmp_best_dir).split('_')[-1]
            print(f"Best Thread Count: {thread_count} threads")

if __name__ == "__main__":
    plot_optimization_journey()