.PHONY: all clean help ci-122 ci-105 ga-37 ga-57x

# Python interpreter
PYTHON = python3

# Source files
SCRIPTS = ci-122-doubler.py ci-105-doubler.py ga-37-doubler.py ga-57x-doubler.py

# Output directory
BUILD_DIR = build

# Default target
all: setup $(SCRIPTS:.py=)

# Create build directory if it doesn't exist
setup:
	mkdir -p $(BUILD_DIR)

# Generate individual targets
ci-122: setup
	$(PYTHON) ci-122-doubler.py

ci-105: setup
	$(PYTHON) ci-105-doubler.py

ga-37: setup
	$(PYTHON) ga-37-doubler.py

ga-57x: setup
	$(PYTHON) ga-57x-doubler.py

# Clean build directory
clean:
	rm -rf $(BUILD_DIR)/*

# Help target
help:
	@echo "Available targets:"
	@echo "  all       - Generate all doubler files (default)"
	@echo "  ci-122    - Generate CI-122 doubler files"
	@echo "  ci-105    - Generate CI-105 doubler files"
	@echo "  ga-37     - Generate GA-37 doubler files"
	@echo "  ga-57x    - Generate GA-57X doubler files"
	@echo "  clean     - Remove all generated files"
	@echo "  help      - Display this help message"
