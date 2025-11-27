GRID_SIZE := 200
TIME_STEPS := 20000
ALPHA := 0.2
DX := 0.01

CC := gcc
CFLAGS_O0 := -O0
CFLAGS_O3 := -O3

OPENMP_CFLAGS := -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include
OPENMP_LDFLAGS := -L/opt/homebrew/opt/libomp/lib -lomp

RESULTS_DIR := results/latest
STAGE_RESULTS_DIR := $(RESULTS_DIR)/stage_results
ARCHIVE_DIR := results/archive

.PHONY: help