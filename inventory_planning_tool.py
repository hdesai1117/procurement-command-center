import pandas as pd
import math

df = pd.read_csv("inventory_advanced.csv")

# Days of Supply
df["DaysSupply"] = (
    df["OnHandQty"] /
    df["DailyUsage"]
)

# Reorder Point
df["ReorderPoint"] = (
    df["DailyUsage"] *
    df["LeadTimeDays"]
) + df["SafetyStock"]

# EOQ
def calculate_eoq(row):

    return round(
        math.sqrt(
            (2 * row["AnnualDemand"] * row["OrderCost"])
            / row["HoldingCost"]
        )
    )

df["EOQ"] = df.apply(
    calculate_eoq,
    axis=1
)

# Inventory Status
def inventory_status(row):

    if row["OnHandQty"] < row["ReorderPoint"]:
        return "REORDER NOW"

    elif row["OnHandQty"] < row["ReorderPoint"] * 1.25:
        return "MONITOR"

    return "HEALTHY"

df["Status"] = df.apply(
    inventory_status,
    axis=1
)

print("\nPROCUREMENT INVENTORY PLANNING REPORT")
print("=" * 70)

for _, row in df.iterrows():

    print(f"""
Material: {row['Material']}

Current Inventory: {row['OnHandQty']:,.0f}
Daily Usage: {row['DailyUsage']:,.0f}

Days Supply: {row['DaysSupply']:.1f}

Lead Time: {row['LeadTimeDays']} days
Safety Stock: {row['SafetyStock']:,.0f}

Reorder Point: {row['ReorderPoint']:,.0f}

EOQ Recommendation: {row['EOQ']:,.0f}

Status: {row['Status']}
""")

print("=" * 70)

critical = df[df["Status"] == "REORDER NOW"]

print("\nBUYER ACTION SUMMARY")
print("-" * 70)

if len(critical):

    for _, row in critical.iterrows():

        shortage = (
            row["ReorderPoint"] -
            row["OnHandQty"]
        )

        print(f"""
Material: {row['Material']}

Inventory is BELOW reorder point.

Current Qty:
{row['OnHandQty']:,.0f}

Reorder Point:
{row['ReorderPoint']:,.0f}

Shortfall:
{shortage:,.0f}

Recommended PO Quantity:
{row['EOQ']:,.0f}
""")

else:

    print("No immediate purchasing actions required.")