import pandas as pd

df = pd.read_csv("market_data.csv")

metrics = [
    "DieselIndex",
    "OceanFreight",
    "ResinPrice",
    "CopperPrice"
]

print("\nMARKET INTELLIGENCE REPORT")
print("=" * 60)

rising = []

for metric in metrics:

    start = df[metric].iloc[0]
    end = df[metric].iloc[-1]

    pct_change = ((end - start) / start) * 100

    print(f"{metric}: {pct_change:.2f}%")

    if end > start:
        rising.append(metric)

print("=" * 60)

print("\nPROCUREMENT ANALYSIS")

if len(rising) >= 3:

    print("""
Market indicators show broad cost increases.

Likely Impacts:
- Higher supplier quotations
- Increased transportation costs
- Upward pricing pressure

Recommended Actions:
1. Lock pricing where possible
2. Issue RFQs earlier
3. Increase monitoring of key suppliers
4. Evaluate secondary sourcing options
""")

else:

    print("""
Market conditions appear stable.

Continue routine sourcing reviews.
""")