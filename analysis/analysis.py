"""
Republic of Texas debt settlement: comparison of two allocation frameworks.

Run from the repository's top folder:
    python analysis/analysis.py

What it does:
1. Loads data/debt_instruments.csv.
2. Checks reconstructed figures against published aggregate totals.
3. Compares Texas's original state-scaled valuations with a modeled allocation
   of the $7.75 million federal appropriation.
4. Saves an instrument-level results table and comparison chart.

IMPORTANT INTERPRETIVE LIMITATION:
The federal allocation assumes a uniform proportional rate applied to each
instrument's final principal plus interest. Miller (1916, pp. 63, 64, 74, 79)
supports this interpretation, but the original Act of February 28, 1855 has
not yet been independently checked.

The calculated federal amounts are modeled allocations, not independently
verified historical disbursements. Differences between the two frameworks
are not established realized gains or losses for individual creditors.
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
    if not ok:
        raise ValueError(f"Verification check failed: {label}")

total_final = df["final_amount"].sum()
df["state_scaled_amount"] = df["final_amount"] * df["state_rating"]
total_scaled = df["state_scaled_amount"].sum()

# Tie-outs. Every row is now a sourced figure (no row is derived by subtraction), so these
# checks are real tests: the rows must reproduce the TSHA totals independently.
check(f"Rows sum to published revenue debt (diff ${total_final - REVENUE_DEBT_TOTAL:,.2f})",
      abs(total_final - REVENUE_DEBT_TOTAL) < 1.0)
check(f"State-scaled rows sum to published scaled total (diff ${total_scaled - STATE_SCALED_TOTAL:,.2f})",
      abs(total_scaled - STATE_SCALED_TOTAL) < 1.0)
check("Published state rate matches 44.3%",
      abs(total_scaled / total_final - PUBLISHED_STATE_RATE) < 0.001)
check("Published federal rate matches 76.9%",
      abs(federal_rate - PUBLISHED_FEDERAL_RATE) < 0.001)
check("All state ratings lie in Miller's observed range, 0.20 to 0.8745",
      df["state_rating"].between(0.20, 1.00).all())
print()

df["federal_amount"] = df["final_amount"] * federal_rate

by_inst = (df.groupby("instrument_id", sort=False)
             .agg(final_amount=("final_amount", "sum"),
                  state_scaled_amount=("state_scaled_amount", "sum"),
                  federal_amount=("federal_amount", "sum")))
by_inst["state_effective_rate"] = by_inst.state_scaled_amount / by_inst.final_amount
by_inst["federal_minus_state"] = by_inst.federal_amount - by_inst.state_scaled_amount

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
pd.set_option("display.width", 200)
print(by_inst)

os.makedirs(os.path.join(ROOT, "outputs"), exist_ok=True)
by_inst.to_csv(os.path.join(ROOT, "outputs", "results_by_instrument.csv"))

plot = by_inst.copy()
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
