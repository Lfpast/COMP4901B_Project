# Tests Directory

This directory contains test scripts for the project.

## Test Files

### `test_maps.py`
Quick test script for Google Maps functionality.

**Usage:**
```bash
cd /home/smallveg/COMP4901B_Project
python3 tests/test_maps.py
```

**What it does:**
1. Searches for coffee shops in Central, Hong Kong
2. Displays detailed information about the results
3. Creates an interactive map visualization in `examples/test_coffee_map.html`

**Expected output:**
- Console output with place information
- HTML map file in the `examples/` directory

## Running Tests

Make sure you have:
1. API keys configured in `.env` file
2. All dependencies installed: `pip install -r requirements.txt`
3. Run from the project root directory

## Adding New Tests

When adding new test files:
1. Follow the naming convention: `test_*.py`
2. Add proper imports and path setup
3. Save all output files to the `examples/` directory
4. Include clear print statements for test progress
5. Update this README with test description

