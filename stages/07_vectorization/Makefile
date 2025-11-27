include ../../config.mk

.PHONY: run clean force

STAGE_NAME := $(notdir $(CURDIR))
STAGE_RESULTS := $(abspath $(STAGE_RESULTS_DIR))/$(STAGE_NAME)

CFLAGS := $(CFLAGS_O3) -ffast-math -mcpu=apple-m4 -march=native
SOURCES := solver.c
TARGET := solver
CF := clang
$(TARGET): $(SOURCES)
	$(CF) $(CFLAGS) -o $(TARGET) $(SOURCES)

run: force $(TARGET)
	@mkdir -p $(STAGE_RESULTS)
	@echo "=================================================================="
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	@./$(TARGET) $(GRID_SIZE) $(TIME_STEPS) $(ALPHA) $(DX) $(STAGE_RESULTS)

clean:
	rm -f $(TARGET) *.o

force:
	@true