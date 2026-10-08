# Assignment 3: Solutions and Completed Code

All explanations, notebook text, and filenames in this package are in English.

## Reading order

1. `Assignment_3_Solutions.md`: complete derivations and answers to the three theoretical questions, with the computational implementation explained.
2. `assignment3_bond_futures.ipynb`: the written solutions plus numerical verification and a 30-day CTD scenario, with outputs included.
3. `hw3_products.ipynb`: the instructor's examples, with the six TODO implementations completed and outputs updated.
4. `fixedincomelib/product/linear_products.py` and `product_display_visitor.py`: the completed product classes and visitor.

## Additional files

- `bond_futures.py`: standard-library-only bond-futures calculations.
- `validate_solution.py`: eight additional contract and numerical checks.
- `solution.patch`: changes to the two upstream source files.
- `fixedincomelib/`: the instructor's source structure and required code.
- `requirements.txt`, `LICENSE`, and `UPSTREAM_README.md`: upstream dependencies, license, and project description. The upstream screenshot directory is omitted because these notebooks do not depend on it.

## Numerical results

| Quantity | Result |
|---|---:|
| Accrued interest at delivery | 1.000000 |
| Dirty forward price | 100.500000 |
| Clean forward price BF | 99.500000 |
| Conversion factor K | 0.8624648692 |
| Normalized forward BF/K | 115.3670179 |
| Implied repo for F = 115.3670 | 1.9999383% |

## Running the examples

Run from the extracted `assignment3_english` directory. The instructor recommends Python 3.11. Create an environment and install the original requirements:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python bond_futures.py
python validate_solution.py
python -m jupyter notebook
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open each notebook and select Run All.

## Validation

The supplied outputs were generated with Python 3.12.14, QuantLib 1.41, pandas 2.2.3, and NumPy 2.3.5. The instructor's `requirements.txt` is retained for reproduction in the requested environment.

All eight code cells across both notebooks were executed sequentially in a Python interpreter, and every instructor assertion passed. Outputs were written back to the notebooks. Execution did not use a separate Jupyter kernel. All eight additional validation tests passed.

Checks cover accrual fractions, payment defaults, index currencies, tenor business-day adjustment, serialization, visitor dispatch, and repo inversion across coupon payments and shifted valuation dates.

The theoretical calculations assume semiannual yield compounding, simple-interest repo, three months equal to 0.25 years, and an initial valuation date immediately after a coupon payment. The scenario basket is an illustrative construction, not supplied market data.

## Source

[Jerry0108-SJ/FRE-GY-9743-Assignments-3](https://github.com/Jerry0108-SJ/FRE-GY-9743-Assignments-3), commit `5847d1b4860177e0b4747ecbd696e28edc7a4c14`.
