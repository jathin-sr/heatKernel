include ../../config.mk

.PHONY: run clean force

STAGE_NAME := $(notdir $(CURDIR))
STAGE_RESULTS := $(abspath $(STAGE_RESULTS_DIR))/$(STAGE_NAME)

CFLAGS_BASE := -std=c99 -Wall
CFLAGS_O3 := $(CFLAGS_BASE) -O3 -march=native -ffast-math

CFLAGS := $(CFLAGS_O3) -ffast-math -mcpu=apple-m4 $(OPENMP_CFLAGS)
LDFLAGS := $(OPENMP_LDFLAGS)
SOURCES := solver.c
TARGET := solver

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES) $(LDFLAGS) -lm

NUM_CORES := $(shell sysctl -n hw.ncpu 2>/dev/null || echo 4)
run_: force $(TARGET)
	@mkdir -p $(STAGE_RESULTS)
	@echo "=================================================================="
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	@OMP_NUM_THREADS=5 ./$(TARGET) $(GRID_SIZE) $(TIME_STEPS) $(ALPHA) $(DX) $(STAGE_RESULTS)

# Run with thread scaling from 1 to 20
run: force $(TARGET)
	@mkdir -p $(STAGE_RESULTS)
	@echo "=================================================================="
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	
	@for threads in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
		THREAD_DIR="$(STAGE_RESULTS)/threads_$$threads"; \
		mkdir -p "$$THREAD_DIR"; \
		OMP_NUM_THREADS=$$threads ./$(TARGET) $(GRID_SIZE) $(TIME_STEPS) $(ALPHA) $(DX) "$$THREAD_DIR" 2>/dev/null || true; \
		if [ -f "$$THREAD_DIR/metrics.json" ]; then \
			time=$$(grep '"total_time"' "$$THREAD_DIR/metrics.json" | grep -o '[0-9]*\.\?[0-9]*' | head -1); \
			performance=$$(grep '"performance"' "$$THREAD_DIR/metrics.json" | grep -o '[0-9]*\.\?[0-9]*' | head -1); \
		else \
			echo "  Threads: $$threads, FAILED"; \
		fi; \
	done
	
	@$(MAKE) generate-thread-report

# Generate thread scaling report
generate-thread-report:
	@echo "# Thread Scaling Analysis" > $(STAGE_RESULTS)/thread_scaling_report.md
	@echo "Generated: $(shell date)" >> $(STAGE_RESULTS)/thread_scaling_report.md
	@echo "" >> $(STAGE_RESULTS)/thread_scaling_report.md
	@echo "| Threads | Time (s) | Performance (steps/s) | Speedup |" >> $(STAGE_RESULTS)/thread_scaling_report.md
	@echo "|---------|----------|----------------------|---------|" >> $(STAGE_RESULTS)/thread_scaling_report.md
	
	@single_thread_time=0; \
	for threads in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
		metrics_file="$(STAGE_RESULTS)/threads_$$threads/metrics.json"; \
		if [ -f "$$metrics_file" ]; then \
			time=$$(grep '"total_time"' $$metrics_file | grep -o '[0-9]*\.\?[0-9]*' | head -1); \
			performance=$$(grep '"performance"' $$metrics_file | grep -o '[0-9]*\.\?[0-9]*' | head -1); \
			if [ "$$threads" = "1" ]; then \
				single_thread_time=$$time; \
			fi; \
			if [ -n "$$single_thread_time" ] && [ "$$single_thread_time" != "0" ]; then \
				speedup=$$(echo "scale=2; $$single_thread_time / $$time" | bc -l 2>/dev/null || echo "0"); \
				else \
				speedup="N/A"; \
			fi; \
			echo "| $$threads | $$time | $$performance | $$speedup |" >> $(STAGE_RESULTS)/thread_scaling_report.md; \
		else \
			echo "| $$threads | FAILED | FAILED | FAILED |" >> $(STAGE_RESULTS)/thread_scaling_report.md; \
		fi; \
	done
	
	@echo "" >> $(STAGE_RESULTS)/thread_scaling_report.md

clean:
	rm -f $(TARGET) *.o

force:
	@true