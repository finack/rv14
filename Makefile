.PHONY: all clean help ci-122 ci-105 ga-37 ga-57x

PYTHON = python3
BUILD_DIR = build

all: setup ci-105 ci-122 ga-37 ga-57x

setup:
	mkdir -p $(BUILD_DIR)

ci-122: setup
	$(PYTHON) ci-122-doubler.py

ci-105: setup
	$(PYTHON) ci-105-doubler.py

ga-37: setup
	$(PYTHON) ga-37-doubler.py

ga-57x: setup
	$(PYTHON) ga-57x-doubler.py

clean:
	rm -rf $(BUILD_DIR)/*

help:
	@echo "Available targets:"
	@echo "  all       - Generate all doubler files (default)"
	@echo "  ci-122    - Generate CI-122 doubler files"
	@echo "  ci-105    - Generate CI-105 doubler files"
	@echo "  ga-37     - Generate GA-37 doubler files"
	@echo "  ga-57x    - Generate GA-57X doubler files"
	@echo "  clean     - Remove all generated files"
	@echo "  help      - Display this help message"
