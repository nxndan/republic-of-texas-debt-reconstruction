# Who Took the Haircut? The Republic of Texas Debt Settlement, 1850-1856

A small reconstructed dataset and analysis of how the Republic of Texas's debt was scaled by the state and settled by the U.S. Congress.

**Authors:** [NAME(S)] **Contact:** [school or personal email you are comfortable making public]

## Research question
Texas scaled each debt instrument by its estimated value when issued (rated from 25 to 87.45 cents on the dollar). Congress instead paid one amount, $7.75 million, against a revenue debt of about $10.08 million (about 76.9 cents on the dollar). Which instruments gained or lost relative to the state's own ratings?

## Data
- `data/debt_instruments.csv`: debt instruments, amounts, interest, and state ratings.
- `data/purpose_of_debt_1836.csv`: what the Republic's early debt financed.
- `data/DATA_DICTIONARY.md` and `data/SOURCES.md`: definitions and sources.

All figures come from publicly available sources (see `data/SOURCES.md`). Rows are marked `second_person_verified` once independently re-entered.

## Reproduce
```
pip install -r requirements.txt
python analysis/analysis.py
```
Outputs are written to `outputs/`.

## Results
[PASTE the table from outputs/results_by_instrument.csv and embed outputs/state_vs_federal_rate.png here after the data is verified.]

## Key assumption and limitations
The federal payment is modeled as a flat percentage of each instrument's final principal plus interest. This must be confirmed against the Act of February 28, 1855. [List any rows still unresolved.]

## Paper
`paper/` contains the written analysis: [LINK]

## License
Code: MIT (see `LICENSE`). Data and text: please cite this repository.
