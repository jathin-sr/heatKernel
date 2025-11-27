include ../../config.mk

.PHONY: run clean force

STAGE_NAME := $(notdir $(CURDIR))
STAGE_RESULTS := $(abspath $(STAGE_RESULTS_DIR))/$(STAGE_NAME)

CFLAGS_BASE := -std=c99 -Wall  -mtune=native
CFLAGS_O3 := $(CFLAGS_BASE) -O3 -march=native -ffast-math -mtune=native

# Architecture-specific tuning flags
CFLAGS_M_ULTRA := $(CFLAGS_BASE) -O3 -mcpu=apple-m1 -ffast-math -flto
CFLAGS_M_MAX := $(CFLAGS_BASE) -O3 -mcpu=apple-m1 -ffast-math -flto -fomit-frame-pointer -funroll-loops
CFLAGS_GENERIC := $(CFLAGS_BASE) -O3 -march=native -ffast-math
CFLAGS_AGGRESSIVE := $(CFLAGS_BASE) -O3 -march=native -ffast-math -flto -fomit-frame-pointer -funroll-loops -fno-math-errno

LDFLAGS := $(OPENMP_LDFLAGS) -lm
LDFLAGS_LTO := $(OPENMP_LDFLAGS) -flto -lm

SOURCES := solver.c
TARGET := solver

# Detect Apple Silicon
UNAME_M := $(shell uname -m)
ifeq ($(UNAME_M),arm64)
    APPLE_SILICON := 1
    # Try to detect specific M-series
    ifeq ($(shell sysctl -n machdep.cpu.brand_string | grep -o "M[0-9]"),M1)
        CPU_TYPE := apple-m1
    else ifeq ($(shell sysctl -n machdep.cpu.brand_string | grep -o "M[0-9]"),M2)
        CPU_TYPE := apple-m2  
    else ifeq ($(shell sysctl -n machdep.cpu.brand_string | grep -o "M[0-9]"),M3)
        CPU_TYPE := apple-m3
    else ifeq ($(shell sysctl -n machdep.cpu.brand_string | grep -o "M[0-9]"),M4)
        CPU_TYPE := apple-m4
    else
        CPU_TYPE := apple-a14  # Fallback
    endif
else
    APPLE_SILICON := 0
    CPU_TYPE := native
endif

# Default build - auto-detect best for current architecture
$(TARGET): $(SOURCES)
	@echo "Building with architecture-specific optimization..."
	@echo "Detected architecture: $(UNAME_M), CPU: $(CPU_TYPE)"
	
	@if [ "$(APPLE_SILICON)" = "1" ]; then \
		echo "Using Apple Silicon optimizations..."; \
		$(CC) $(CFLAGS_M_MAX) $(OPENMP_CFLAGS) -o $(TARGET) $(SOURCES) $(LDFLAGS_LTO); \
	else \
		echo "Using generic native optimizations..."; \
		$(CC) $(CFLAGS_AGGRESSIVE) $(OPENMP_CFLAGS) -o $(TARGET) $(SOURCES) $(LDFLAGS); \
	fi

# Run thread scaling with best optimization
run: force $(TARGET)
	@mkdir -p $(STAGE_RESULTS)
	@echo "=================================================================="
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	@echo "Architecture: $(UNAME_M), CPU: $(CPU_TYPE)"
	
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

clean:
	rm -f $(TARGET) $(TARGET)_.* *.o

force:
	@true