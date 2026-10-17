# Energy Storage Materials CP Solver

Constraint Programming model for selecting energy storage materials based on thermodynamic stability, availability, cost, and performance.

## Content
- `model.mzn` : MiniZinc-style constraint model
- `stability_data.md` : Consolidated stability data (oxides, alloys, hydrides...)
- `materials_project_example.py` : Example script to query Materials Project

## Usage
Use with a constraint solver (MiniZinc, OR-Tools, etc.) to optimize material combinations.
