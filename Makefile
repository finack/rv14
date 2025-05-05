.PHONY: all clean

# Python interpreter
PYTHON = python3

# Source files
SCRIPTS = ci-122-doubler.py ci-105-doubler.py ga-37-doubler.py ga-57x-doubler.py

# Output directory
BUILD_DIR = build

# Output files - These will be determined dynamically
DXF_FILES = $(BUILD_DIR)/ci-122-doubler-v0.1.dxf \
            $(BUILD_DIR)/ci-105-doubler-v0.3.dxf \
            $(BUILD_DIR)/ga-37-doubler-v0.2.dxf \
            $(BUILD_DIR)/ga-57x-doubler-v0.2.dxf

PNG_FILES = $(BUILD_DIR)/ci-122-doubler-v0.1.png \
            $(BUILD_DIR)/ci-105-doubler-v0.3.png \
            $(BUILD_DIR)/ga-37-doubler-v0.2.png \
            $(BUILD_DIR)/ga-57x-doubler-v0.2.png

# Default target
all: setup $(DXF_FILES) $(PNG_FILES)

# Create build directory if it doesn't exist
setup:
	mkdir -p $(BUILD_DIR)

# Generate DXF and PNG files by running all scripts
$(BUILD_DIR)/ci-122-doubler-v0.1.dxf $(BUILD_DIR)/ci-122-doubler-v0.1.png: ci-122-doubler.py doubler_utils.py
	$(PYTHON) ci-122-doubler.py

$(BUILD_DIR)/ci-105-doubler-v0.3.dxf $(BUILD_DIR)/ci-105-doubler-v0.3.png: ci-105-doubler.py doubler_utils.py
	$(PYTHON) ci-105-doubler.py

$(BUILD_DIR)/ga-37-doubler-v0.2.dxf $(BUILD_DIR)/ga-37-doubler-v0.2.png: ga-37-doubler.py doubler_utils.py
	$(PYTHON) ga-37-doubler.py

$(BUILD_DIR)/ga-57x-doubler-v0.2.dxf $(BUILD_DIR)/ga-57x-doubler-v0.2.png: ga-57x-doubler.py doubler_utils.py
	$(PYTHON) ga-57x-doubler.py

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
	@echo "  all       - Generate all DXF and PNG files (default)"
	@echo "  ci-122    - Generate CI-122 doubler files"
	@echo "  ci-105    - Generate CI-105 doubler files"
	@echo "  ga-37     - Generate GA-37 doubler files"
	@echo "  ga-57x    - Generate GA-57X doubler files"
	@echo "  clean     - Remove all generated files"
	@echo "  help      - Display this help message"