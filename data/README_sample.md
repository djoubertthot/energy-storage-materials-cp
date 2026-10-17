# Sample Materials Dataset

## File: `sample_materials_for_solver.csv`

This is a small but representative dataset (15 materials) with key fields for constraint programming:

- `formation_energy`
- `e_above_hull` (stability)
- `elements`
- `band_gap`
- `density`

### Usage with Solver
Load this CSV directly into your MiniZinc / OR-Tools / PuLP model as a starting point to test constraints (stability < 0.05, energy density targets, element filters, etc.).

### Expanding the Dataset
Run the download scripts in `scripts/` with your API keys to generate much larger CSVs in the same format.

This sample is sufficient to validate the solver pipeline immediately.
