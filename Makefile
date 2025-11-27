include config.mk
include pipeline.mk

.DEFAULT_GOAL := help

.PHONY: run clean help setup_dirs plots

run: setup_dirs
	@for stage in $(PIPELINE_STAGES); do \
		$(MAKE) -C stages/$$stage run \
			GRID_SIZE=$(GRID_SIZE) \
			TIME_STEPS=$(TIME_STEPS) \
			ALPHA=$(ALPHA) \
			DX=$(DX) \
			RESULTS_DIR=$(abspath $(RESULTS_DIR)) \
			STAGE_RESULTS_DIR=$(abspath $(STAGE_RESULTS_DIR)); \
	done

	@$(MAKE) copy-optimal
	@$(MAKE) generate_report
	@echo "Results: $(RESULTS_DIR)/pipeline_summary.md"

run_%: setup_dirs
	@cd stages/$* && \
	$(MAKE) run \
		GRID_SIZE=$(GRID_SIZE) \
		TIME_STEPS=$(TIME_STEPS) \
		ALPHA=$(ALPHA) \
		DX=$(DX) \
		RESULTS_DIR=$(abspath $(RESULTS_DIR)) \
		STAGE_RESULTS_DIR=$(abspath $(STAGE_RESULTS_DIR))

# Generate minimal report
generate_report:
	@mkdir -p $(RESULTS_DIR)
	@echo "# Pipeline Results" > $(RESULTS_DIR)/pipeline_summary.md
	@echo "Generated: $(shell date)" >> $(RESULTS_DIR)/pipeline_summary.md
	@echo "" >> $(RESULTS_DIR)/pipeline_summary.md
	@echo "| Stage | Time (s) | Time/Step (ms) | Performance (steps/s) |" >> $(RESULTS_DIR)/pipeline_summary.md
	@echo "|-------|----------|----------------|----------------------|" >> $(RESULTS_DIR)/pipeline_summary.md
	@for stage in $(PIPELINE_STAGES); do \
		metrics_file="$(STAGE_RESULTS_DIR)/$$stage/metrics.json"; \
		if [ -f "$$metrics_file" ]; then \
			time=$$(grep '"total_time"' $$metrics_file | cut -d: -f2 | tr -d ', '); \
			time_per_step=$$(grep '"time_per_step"' $$metrics_file | cut -d: -f2 | tr -d ', '); \
			performance=$$(grep '"performance"' $$metrics_file | cut -d: -f2 | tr -d ', '); \
			echo "| $$stage | $$time | $$time_per_step | $$performance |" >> $(RESULTS_DIR)/pipeline_summary.md; \
		else \
			echo "| $$stage | NOT RUN | NOT RUN | NOT RUN |" >> $(RESULTS_DIR)/pipeline_summary.md; \
		fi; \
	done

# Setup directories
setup_dirs:
	@mkdir -p $(RESULTS_DIR) $(STAGE_RESULTS_DIR)

# Archive current results
archive:
	@if [ -d "$(RESULTS_DIR)" ]; then \
		TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
		ARCHIVE_PATH="results/archive/results_$$TIMESTAMP"; \
		mkdir -p "results/archive"; \
		cp -r "$(RESULTS_DIR)" "$$ARCHIVE_PATH"; \
	else \
		echo "No results to archive"; \
	fi

clean:
	@for stage in $(PIPELINE_STAGES); do \
		if [ -d "stages/$$stage" ]; then \
			$(MAKE) -C stages/$$stage clean; \
		fi; \
	done
	@rm -rf $(RESULTS_DIR)

# Generate all plots
plots:
	@python src/visualization/plot_arch_threads.py
	@python src/visualization/plot_thread_scaling.py
	@python src/visualization/plot_optimization_evolution.py
	@echo "All plots generated in $(RESULTS_DIR)/performance_plots/"

copy-optimal:
	@python src/utils/report_helper.py

# Help
help:
	@echo "Available targets:"
	@echo "  run       - Run all stages"
	@echo "  run_STAGE     - Run specific stage"
	@echo "  clean         - Clean all build artifacts"
	@echo "  help          - Show this help"
	@echo ""
	@echo "Available stages:"
	@for stage in $(PIPELINE_STAGES); do \
		echo "  - $$stage"; \
	done