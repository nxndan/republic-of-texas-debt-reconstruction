# The Republic of Texas Debt Settlement, 1850-1856

A small reconstructed dataset and analysis of how the Republic of Texas's revenue debt was scaled by the State of Texas and then settled by the U.S. Congress.

**Authors:** Nandan Ramaswamy [add co-authors here if they contributed]
**Contact:** contact.nandanr@gmail.com
**Status:** Working draft. Data have not yet been independently verified (see "Verification status").

## Research question
Texas scaled each debt instrument by its estimated value when issued (its "principle of equivalents" rating). Rated tranches range from 20 to 87.45 cents on the dollar, and two small tranches were rated at par. Congress instead appropriated one sum, $7.75 million, against a revenue debt of about $10.08 million, or about 76.9 cents on the dollar. Which instruments gained or lost relative to the state's own ratings?

## Data
- `data/debt_instruments.csv`: nine rows covering six instruments (PA_BANK, NAVAL, FUND1837, FUND1840, NOTES, TREAS8), with final principal plus interest, state ratings, and Miller page references.
- `data/purpose_of_debt_1836.csv`: what the Republic's early debt financed, as of 26 August 1836.
- `data/DATA_DICTIONARY.md`: column definitions.
- `data/SOURCES.md`: sources and the proration evidence.

All figures are transcribed from published secondary sources (E. T. Miller, *A Financial History of Texas*, 1916, and Miller's *Handbook of Texas* entry). No archival records were used for numbers.

## Verification status
- `purpose_of_debt_1836.csv`: every row was independently re-entered and matched (`second_person_verified = YES`).
- `debt_instruments.csv`: **no row is verified yet.** Every row is marked `NO`, and the page references have not yet been checked against the page scans.
- The 1836 categories sum to $1,252,000, but Miller prints a total of $1,250,000. The CSV reproduces the printed components, so do not use the stated total in calculations.

## Reproduce
```
pip install -r requirements.txt
python analysis/analysis.py
```
The script runs tie-out checks against the published totals (revenue debt of $10,078,703.21 and state-scaled total of $4,467,756.41), then writes `outputs/results_by_instrument.csv` and `outputs/state_vs_federal_rate.png`.

## Results
State-scaled value versus a flat federal payout, by instrument (US dollars):

| instrument_id | final_amount | state_scaled_amount | federal_amount | state_effective_rate | federal_minus_state |
|---|---|---|---|---|---|
| PA_BANK | 960,498.00 | 839,955.50 | 738,573.14 | 0.87 | -101,382.36 |
| NAVAL | 1,622,404.70 | 811,202.35 | 1,247,545.06 | 0.50 | 436,342.71 |
| FUND1837 | 1,687,094.80 | 1,189,753.80 | 1,297,288.39 | 0.71 | 107,534.59 |
| FUND1840 | 1,674,380.42 | 502,314.13 | 1,287,511.70 | 0.30 | 785,197.57 |
| NOTES | 2,716,645.29 | 840,994.65 | 2,088,959.32 | 0.31 | 1,247,964.67 |
| TREAS8 | 1,417,680.00 | 283,536.00 | 1,090,122.39 | 0.20 | 806,586.39 |
| **Total** | **10,078,703.21** | **4,467,756.43** | **7,750,000.00** | **0.44** | **3,282,243.57** |

Under the flat federal rate (about 0.769), PA_BANK is the only instrument that receives less than the state's own rating would have paid. The five others receive more, and the largest gains in dollars go to the treasury notes (NOTES) and the 1840 treasury bonds (TREAS8). The state-scaled total here differs from the published $4,467,756.41 by about two cents due to rounding.

![State vs Federal Rate Chart](outputs/state_vs_federal_rate.png)

## Key assumption and limitations
- **Uniform proration (unconfirmed).** The federal payment is modeled as a flat percentage of each instrument's final principal plus interest. Miller (1916, pp. 63, 64, 74, 79) describes the revenue debt as paid pro rata at 76 9/10 cents on the dollar under the Act of February 28, 1855, which supports this, but it is a secondary source. The text of the Act has not yet been read.
- **Secondary-source numbers.** All amounts come from Miller and the TSHA entry, not from the original records.
- **Remainder resolved.** The former unitemized remainder ($1,417,680.00) is identified as the 8% treasury bonds of February 5, 1840 (TREAS8), from Miller pp. 78-79. With this row, the instruments sum to the published revenue-debt total. The row itself is not yet independently verified.
- **No present-value adjustment.** All amounts are nominal, as of final settlement.
- **Holders not covered.** The analysis compares instruments, not who ultimately held them.

## Paper
`paper/PAPER_OUTLINE.md` contains the outline. The full draft has not been written yet.

## License
Code: MIT (see `LICENSE`). Data and text: please cite this repository.
