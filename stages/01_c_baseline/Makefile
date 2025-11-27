include ../../config.mk

.PHONY: run clean force

STAGE_NAME := $(notdir $(CURDIR))
STAGE_RESULTS := $(abspath $(STAGE_RESULTS_DIR))/$(STAGE_NAME)

CFLAGS := $(CFLAGS_O0)
SOURCES := solver.c
TARGET := solver

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)
	
run: force $(TARGET)
	@mkdir -p $(STAGE_RESULTS)
	@echo "=================================================================="
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	@./$(TARGET) $(GRID_SIZE) $(TIME_STEPS) $(ALPHA) $(DX) $(STAGE_RESULTS)

clean:
	rm -f $(TARGET) *.o

force:
	@true