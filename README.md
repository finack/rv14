# RV-14 and GA Aircraft Doubler Scripts

This repository contains Python scripts for creating antenna doubler plates for various aircraft models, including RV-14 and GA models. The scripts generate both DXF files (for CAD software) and PDF files for printing.

## Setup

```bash
# Install required dependencies
pip3 install 'ezdxf[draw]'
```

## Usage

The repository includes a Makefile for easy generation of doubler files:

```bash
# Generate all doubler files
make

# Generate specific doubler (e.g. CI-122)
make ci-122

# Clean generated files
make clean

# Display help
make help
```

All generated files are placed in the `build` directory.

## Scripts

- **ci-105-doubler.py**: Script for CI-105 antenna doubler
- **ci-122-doubler.py**: Script for CI-122 antenna doubler
- **ga-37-doubler.py**: Script for GA-37 antenna doubler
- **ga-57x-doubler.py**: Script for GA-57X antenna doubler
- **doubler_utils.py**: Shared utility functions for all doublers

## Purpose

These scripts generate doubler plates that reinforce the aircraft skin around antenna installations. The DXF files are ready-to-use templates for manufacturing, while the PDF files can be printed at 1:1 scale for verification or templates.

## Printing

The generated PDF files include these scale references for proper printing:

1. A 1-inch calibration square that should measure exactly 1 inch when printed
2. Horizontal and vertical scale rulers with 0.25-inch markings
3. Extended canvas margins to ensure the rulers are fully visible

These scale references ensure proper scale for manufacturing and easy measurement.

## 3D Printed Tooling

The `tooling/` directory contains OpenSCAD models for 3D printed jigs and tools:

- **DrillGuideBlock.scad**: Drill guide block (31.8mm x 50.8mm x 25mm) with a #12 drill hole for elevator horn drilling
- **ElevatorHornSpacer.scad**: Small spacer (12.5mm x 5.8mm x 7.5mm) for elevator horn assembly, with embossed text label
- **WasherWrench.scad**: Dual-ended wrench for AN960 aviation washers (#6, #8, and #10 sizes) with relief slits for flexibility
- **FloatArmBendTool.scad**: Wire bending tool for IE-F385B fuel sender float arm (0.090" stainless wire). Three-station design:
  - Station 1 (top): 19.5mm tip bend
  - Station 2 (front): 95.3mm section bend
  - Station 3 (back): Diagonal bend (15.1mm offset over 90mm)

### Exporting STL Files

To export an OpenSCAD model for 3D printing:

```bash
openscad -o output.stl tooling/WasherWrench.scad
```

