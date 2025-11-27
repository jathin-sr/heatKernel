#!/usr/bin/env python3
"""
Copy Optimal Thread Results

This script finds the best performing thread configuration from OpenMP parallel
and architecture-specific runs and copies their results to the main stage directories.
"""

import json
import glob
import os
import shutil
import argparse

def find_best_thread_performance(parent_dir, stage_name):
    """Find the thread directory with the best performance"""
    best_performance = 0
    best_dir = None
    best_thread_count = None
    
    if not os.path.exists(parent_dir):
        print(f"Directory not found: {parent_dir}")
        return best_performance, best_dir, best_thread_count
    
    # Look for thread directories - handle both thread_* and threads_* patterns
    thread_dirs = glob.glob(f"{parent_dir}/thread_*") + glob.glob(f"{parent_dir}/threads_*")
    
    if not thread_dirs:
        print(f"No thread directories found in: {parent_dir}")
        return best_performance, best_dir, best_thread_count
    
    for thread_dir in thread_dirs:
        metrics_file = os.path.join(thread_dir, "metrics.json")
        if os.path.exists(metrics_file):
            try:
                with open(metrics_file) as f:
                    data = json.load(f)
                    performance = data['performance']
                    thread_count = os.path.basename(thread_dir).split('_')[-1]
                    
                    if performance > best_performance:
                        best_performance = performance
                        best_dir = thread_dir
                        best_thread_count = thread_count
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error reading {metrics_file}: {e}")
        else:
            continue
        
    return best_performance, best_dir, best_thread_count

def copy_thread_results(src_dir, dst_dir, stage_name):
    """Copy all relevant files from thread directory to stage directory"""
    if not src_dir or not os.path.exists(src_dir):
        print(f"Source directory doesn't exist for {stage_name}")
        return False
    
    # Create destination directory if it doesn't exist
    os.makedirs(dst_dir, exist_ok=True)
    
    files_copied = []
    
    # Copy all files from the thread directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            files_copied.append(item)
        elif os.path.isdir(src_path):
            # For subdirectories, copy recursively
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            files_copied.append(f"{item}/")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Copy optimal thread results to main stage directories')
    parser.add_argument('--results-dir', default='results/latest',
                       help='Path to results directory (default: results/latest)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be copied without actually copying')
    
    args = parser.parse_args()
    
    results_dir = args.results_dir
    dry_run = args.dry_run
    
    # Stage 8 - OpenMP Parallel
    stage8_parent = f"{results_dir}/stage_results/08_openmp_parallel"
    stage8_best_perf, stage8_best_dir, stage8_threads = find_best_thread_performance(
        stage8_parent, "Stage 8 (OpenMP)"
    )
    
    # Stage 9 - Architecture Specific
    stage9_parent = f"{results_dir}/stage_results/09_arch_specific"
    stage9_best_perf, stage9_best_dir, stage9_threads = find_best_thread_performance(
        stage9_parent, "Stage 9 (Architecture)"
    )
    
    if dry_run:
        print("DRY RUN - No files will be actually copied")
    
    # Copy Stage 8 results
    if stage8_best_dir:
        if dry_run:
            print(f"Would copy Stage 8 from: {stage8_best_dir}")
            print(f"   To: {stage8_parent}")
        else:
            success = copy_thread_results(stage8_best_dir, stage8_parent, "Stage 8")
            if success:
                # Create a note about which thread config was used
                note_file = os.path.join(stage8_parent, "optimal_thread_note.txt")
                with open(note_file, 'w') as f:
                    f.write(f"Optimal thread configuration: {stage8_threads} threads\n")
                    f.write(f"Source: {os.path.basename(stage8_best_dir)}\n")
                    f.write(f"Performance: {stage8_best_perf:,.0f} steps/sec\n")
    else:
        print("No optimal thread configuration found for Stage 8")
    
    # Copy Stage 9 results
    if stage9_best_dir:
        if dry_run:
            print(f"Would copy Stage 9 from: {stage9_best_dir}")
            print(f"To: {stage9_parent}")
        else:
            success = copy_thread_results(stage9_best_dir, stage9_parent, "Stage 9")
            if success:
                # Create a note about which thread config was used
                note_file = os.path.join(stage9_parent, "optimal_thread_note.txt")
                with open(note_file, 'w') as f:
                    f.write(f"Optimal thread configuration: {stage9_threads} threads\n")
                    f.write(f"Source: {os.path.basename(stage9_best_dir)}\n")
                    f.write(f"Performance: {stage9_best_perf:,.0f} steps/sec\n")
    else:
        print("No optimal thread configuration found for Stage 9")
    
if __name__ == "__main__":
    main()