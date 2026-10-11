"""
Analysis: Who took the haircut? Republic of Texas debt settlement (1850-1856).

Run from the repository's top folder:   python analysis/analysis.py

What it does
1. Loads data/debt_instruments.csv
2. Checks the data against totals published in the TSHA entry (tie-out checks)
3. Compares, for each instrument, what the STATE'S OWN SCALING would have paid
   with what a flat federal pro-rata payment of $7.75 million would have paid
4. Saves a table and a chart to the outputs/ folder

KEY ASSUMPTION (must be stated in the paper): the federal payment is treated as a
flat percentage of every instrument's final principal-plus-interest. TSHA says the
$7.75M was prorated among holders of the unscaled revenue debt; confirm with Miller
and the text of the Act of Feb 28, 1855 that the proration was uniform.
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Published totals from TSHA "Debt of the Republic of Texas" (used for tie-out checks)
REVENUE_DEBT_TOTAL = 10_078_703.21     # federal interpretation of revenue debt
STATE_SCALED_TOTAL = 4_467_756.41      # that debt if the state's ratings were accepted
FEDERAL_APPROPRIATION = 7_750_000.00   # Act of February 28, 1855
PUBLISHED_STATE_RATE = 0.443           # 44.3 cents on the dollar
PUBLISHED_FEDERAL_RATE = 0.769         # 76.9 cents on the dollar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "data", "debt_instruments.csv"))
df = df.rename(columns={"final_principal_plus_interest_usd": "final_amount"})

federal_rate = FEDERAL_APPROPRIATION / REVENUE_DEBT_TOTAL
print(f"Federal flat rate implied by $7.75M / ${REVENUE_DEBT_TOTAL:,.2f} = {federal_rate:.4f}")
print(f"State overall rate implied = {STATE_SCALED_TOTAL / REVENUE_DEBT_TOTAL:.4f}\n")

def check(label, ok):
    print(("PASS  " if ok else "FAIL  ") + label)

itemized = df.loc[df.instrument_id != "UNITEMIZED", "final_amount"].sum()
unitemized = df.loc[df.instrument_id == "UNITEMIZED", "final_amount"].sum()
check("Published state rate matches 44.3%",
      abs(STATE_SCALED_TOTAL / REVENUE_DEBT_TOTAL - PUBLISHED_STATE_RATE) < 0.001)
check("Published federal rate matches 76.9%",
      abs(federal_rate - PUBLISHED_FEDERAL_RATE) < 0.001)
# NOTE: the UNITEMIZED row is derived by subtraction, so "itemized + remainder = total"
# would always pass and proves nothing. The real test is below: does the state's published
# scaled total leave a sensible rating (between 0 and 1) for the remainder?
_scaled_itemized = (df.loc[df.instrument_id != "UNITEMIZED", "final_amount"]
                    * df.loc[df.instrument_id != "UNITEMIZED", "state_rating"]).sum()
_implied_remainder_rate = (STATE_SCALED_TOTAL - _scaled_itemized) / unitemized
check("Implied state rating on the unitemized remainder is between 0 and 1",
      0 <= _implied_remainder_rate <= 1)
print(f"      (implied rating on remainder = {_implied_remainder_rate:.3f}; "
      "a low or odd value suggests a missing or mistyped row)")
print(f"\nItemized rows sum to ${itemized:,.2f}; unexplained remainder ${unitemized:,.2f}")
print("(Resolve the remainder from Miller before publishing results that depend on it.)\n")

df["state_scaled_amount"] = df["final_amount"] * df["state_rating"]
df["federal_amount"] = df["final_amount"] * federal_rate

by_inst = (df.groupby("instrument_id", sort=False)
             .agg(final_amount=("final_amount", "sum"),
                  state_scaled_amount=("state_scaled_amount", "sum"),
                  federal_amount=("federal_amount", "sum")))
by_inst["state_effective_rate"] = by_inst.state_scaled_amount / by_inst.final_amount
by_inst["federal_minus_state"] = by_inst.federal_amount - by_inst.state_scaled_amount
# The remainder has no rating yet, so its state columns are meaningless until resolved.
by_inst.loc["UNITEMIZED", ["state_scaled_amount", "state_effective_rate", "federal_minus_state"]] = float("nan")

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
pd.set_option("display.width", 200)
print(by_inst)

os.makedirs(os.path.join(ROOT, "outputs"), exist_ok=True)
by_inst.to_csv(os.path.join(ROOT, "outputs", "results_by_instrument.csv"))

plot = by_inst.drop(index="UNITEMIZED").copy()
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(plot.index, plot.state_effective_rate * 100, label="State's own rating", alpha=0.8)
ax.axhline(federal_rate * 100, linestyle="--", color="black",
           label=f"Flat federal rate ({federal_rate*100:.1f} cents)")
ax.set_ylabel("Cents paid per dollar of principal + interest")
ax.set_title("State scaling vs flat federal payout, by instrument")
ax.legend()
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(ROOT, "outputs", "state_vs_federal_rate.png"), dpi=200)
print("\nSaved outputs/results_by_instrument.csv and outputs/state_vs_federal_rate.png")
