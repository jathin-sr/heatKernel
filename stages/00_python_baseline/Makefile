include ../../config.mk

.PHONY: run clean force

STAGE_NAME := $(notdir $(CURDIR))
STAGE_RESULTS := $(abspath $(STAGE_RESULTS_DIR))/$(STAGE_NAME)

PYTHON := python3

run: force
	@mkdir -p $(STAGE_RESULTS)
	@echo "Running $(STAGE_NAME) with grid=$(GRID_SIZE), steps=$(TIME_STEPS)"
	@$(PYTHON) solver.py \
		--size $(GRID_SIZE) \
		--timesteps $(TIME_STEPS) \
		--alpha $(ALPHA) \
		--dx $(DX) \
		--output-dir $(STAGE_RESULTS)

clean:
	rm -f *.pyc __pycache__/*

force:
	@true