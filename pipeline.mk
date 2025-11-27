# Pipeline stage definitions      00_python_baseline \ 
PIPELINE_STAGES := \
    01_c_baseline \
    02_compiler_O3 \
    03_loop \
    04_cache_utilization \
    05_contiguous_memory \
    06_cache_blocking \
    07_vectorization \
    08_openmp_parallel \
    09_arch_specific

PIPELINE_TARGETS := $(addprefix run_,$(PIPELINE_STAGES))
CLEAN_TARGETS := $(addprefix clean_,$(PIPELINE_STAGES))

.PHONY: $(PIPELINE_TARGETS) $(CLEAN_TARGETS)