import pandas as pd

# =====================================================
# Load Supplier Data
# =====================================================

df = pd.read_csv("supplier_scorecard.csv")

# If AnnualVolume is missing, create it
if "AnnualVolume" not in df.columns:
    print("\nWARNING: AnnualVolume column not found.")
    print("Using default value of 100000 units.\n")

    df["AnnualVolume"] = 100000

# =====================================================
# Price Score
# Lower cost = better
# =====================================================

min_cost = df["UnitCost"].min()
max_cost = df["UnitCost"].max()

if max_cost == min_cost:
    df["PriceScore"] = 100
else:
    df["PriceScore"] = (
        (max_cost - df["UnitCost"])
        / (max_cost - min_cost)
    ) * 100

# =====================================================
# Lead Time Score
# Lower lead time = better
# =====================================================

min_lead = df["LeadTimeDays"].min()
max_lead = df["LeadTimeDays"].max()

if max_lead == min_lead:
    df["LeadTimeScore"] = 100
else:
    df["LeadTimeScore"] = (
        (max_lead - df["LeadTimeDays"])
        / (max_lead - min_lead)
    ) * 100

# =====================================================
# Risk Score
# Lower is better
# =====================================================

df["RiskScore"] = (
    (100 - df["ReliabilityScore"])
    + (100 - df["QualityScore"])
    + (100 - df["OnTimeDelivery"])
)

# =====================================================
# Annual Spend Analysis
# =====================================================

df["AnnualSpend"] = (
    df["UnitCost"]
    * df["AnnualVolume"]
)

lowest_spend = df["AnnualSpend"].min()

df["PremiumVsLowest"] = (
    df["AnnualSpend"]
    - lowest_spend
)

# =====================================================
# Procurement-Focused Weighting
# =====================================================

df["OverallScore"] = (
    (df["PriceScore"] * 0.15)
    + (df["LeadTimeScore"] * 0.25)
    + (df["ReliabilityScore"] * 0.30)
    + (df["QualityScore"] * 0.20)
    + (df["OnTimeDelivery"] * 0.10)
)

# =====================================================
# Supplier Tier Classification
# =====================================================

def supplier_tier(score):

    if score >= 85:
        return "Preferred"

    elif score >= 75:
        return "Approved"

    elif score >= 65:
        return "Conditional"

    else:
        return "High Risk"

df["SupplierTier"] = df["OverallScore"].apply(
    supplier_tier
)

# =====================================================
# Rank Suppliers
# =====================================================

ranked = df.sort_values(
    by="OverallScore",
    ascending=False
)

# =====================================================
# Scorecard Output
# =====================================================

print("\nSTRATEGIC SUPPLIER SCORECARD")
print("=" * 80)

for _, row in ranked.iterrows():

    print("\nSupplier:", row["Supplier"])
    print("Supplier Tier:", row["SupplierTier"])

    print(
        "Unit Cost: ${:.2f}".format(
            row["UnitCost"]
        )
    )

    print(
        "Lead Time: {} Days".format(
            row["LeadTimeDays"]
        )
    )

    print(
        "Reliability: {}%".format(
            row["ReliabilityScore"]
        )
    )

    print(
        "Quality: {}%".format(
            row["QualityScore"]
        )
    )

    print(
        "On-Time Delivery: {}%".format(
            row["OnTimeDelivery"]
        )
    )

    print(
        "Risk Score: {:.2f}".format(
            row["RiskScore"]
        )
    )

    print(
        "Annual Spend: ${:,.2f}".format(
            row["AnnualSpend"]
        )
    )

    print(
        "Cost Premium vs Lowest Supplier: ${:,.2f}".format(
            row["PremiumVsLowest"]
        )
    )

    print(
        "Overall Score: {:.2f}".format(
            row["OverallScore"]
        )
    )

# =====================================================
# Recommended Supplier
# =====================================================

winner = ranked.iloc[0]

print("\n" + "=" * 80)
print("RECOMMENDED SUPPLIER")
print("=" * 80)

print("Supplier:", winner["Supplier"])
print("Supplier Tier:", winner["SupplierTier"])

print(
    "Overall Score: {:.2f}".format(
        winner["OverallScore"]
    )
)

print(
    "Annual Spend: ${:,.2f}".format(
        winner["AnnualSpend"]
    )
)

# =====================================================
# Procurement Assessment
# =====================================================

print("\nPROCUREMENT ASSESSMENT")
print("-" * 80)

if winner["LeadTimeDays"] <= 15:
    print("- Strong lead-time advantage")

if winner["ReliabilityScore"] >= 95:
    print("- Excellent supplier reliability")

if winner["OnTimeDelivery"] >= 95:
    print("- Strong delivery performance")

if winner["QualityScore"] >= 90:
    print("- High product quality rating")

if winner["PremiumVsLowest"] > 0:

    print(
        "- Additional annual spend of ${:,.2f} versus the "
        "lowest-cost supplier is offset by stronger quality, "
        "delivery, reliability, and lead-time performance."
        .format(winner["PremiumVsLowest"])
    )

# =====================================================
# Executive Summary
# =====================================================

lowest_supplier = df.loc[
    df["AnnualSpend"].idxmin(),
    "Supplier"
]

print("\nEXECUTIVE SUMMARY")
print("-" * 80)

print(
    f"""
Recommended Supplier: {winner['Supplier']}

Lowest Cost Supplier: {lowest_supplier}

The recommendation favors supplier
performance, quality, reliability,
and reduced supply-chain risk rather
than selecting purely on price.

This approach better supports supply
continuity and manufacturing stability.
"""
)
