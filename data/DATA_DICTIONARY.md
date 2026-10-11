# Data dictionary

## debt_instruments.csv
One row per instrument *tranche* (a tranche is a slice of an instrument that the state rated differently).

| Column | Meaning |
|---|---|
| instrument_id | Short code used to group rows (PA_BANK, NAVAL, FUND1837, FUND1840, NOTES, UNITEMIZED) |
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

The row `UNITEMIZED` is **derived by subtraction** (published revenue-debt total minus the itemized rows). It is not a source figure. Replace it with real rows from Miller.

## purpose_of_debt_1836.csv
The Republic's estimated debt on 26 August 1836 by category, from Miller (1916), p. 17.
**Check:** the six categories sum to $1,252,000, but the source states a total of $1,250,000. Confirm on the page scan whether this is rounding in the source or an OCR/typing error before using the total.
