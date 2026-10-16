# Data dictionary

## debt_instruments.csv
One row per instrument *tranche* (a tranche is a slice of an instrument that the state rated differently).

| Column | Meaning |
|---|---|
| instrument_id | Short code used to group rows (PA_BANK, NAVAL, FUND1837, FUND1840, NOTES, TREAS8) |
| instrument | Plain-English name of the debt instrument |
| tranche | Which slice of the instrument this row covers |
| interest_rate | Stated interest rate, as text |
| principal_issued_usd | Face amount originally issued (filled on the first row of an instrument only) |
| final_principal_plus_interest_usd | Principal plus accrued interest at final settlement, in US dollars |
| state_rating | The Texas state's scaled value in dollars per dollar (the "principle of equivalents" rating; 1.00 = par) |
| named_holder | A holder named in the source, if any |
| purpose | What the instrument was issued for |
| source | Where the number came from |
| miller_page | Printed page number in Miller (1916) supporting the row, once checked |
| second_person_verified | YES only after a second person re-entered the number independently and it matched |

The former `UNITEMIZED` remainder ($1,417,680.00, originally found by subtraction) is identified as the 8% treasury bonds of the act of February 5, 1840 (`TREAS8`). Miller (1916), pp. 78-79, gives their principal and interest to July 1, 1850 as exactly $1,417,680 and the state rating as 20 cents. With that row, the rows sum to the published revenue-debt total.

## purpose_of_debt_1836.csv
The Republic's estimated debt on 26 August 1836 by category, from Miller (1916), p. 17.
**Check (resolved as a source discrepancy):** the six categories sum to $1,252,000, but Miller states a total of $1,250,000. The CSV reproduces the printed components. Do not use the stated total in calculations without noting this.
