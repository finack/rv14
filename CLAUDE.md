# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Details

- This repository contains scripts for generating aircraft doubler plate designs in DXF and PNG formats
- The scripts use ezdxf library for DXF creation and matplotlib for visualization

## Further Instructions to Claude

- Do not read in PNG or DXF files unless asked
- Use shared functions from doubler_utils.py for common operations
- Follow the shared utility pattern for new reusable functions

## Build/Run Commands

- To run a script: `python3 <script_name>.py`
- Example: `python3 ci-122-doubler.py`
- Use the Makefile for common tasks: `make <target>`
- No linters or tests are currently set up for this project

## Code Style Guidelines

- Use descriptive variable names for dimensions (width, height, etc.)
- Include comments explaining the purpose of complex geometry calculations
- Group related parameters together (e.g., all hole-related dimensions)
- Define reusable functions for common operations (e.g., add_rounded_rect, add_bent_edge)
- Format code with Black (4-space indentation)
- Use type hints where practical
- Include design notes as comments at the top of files

