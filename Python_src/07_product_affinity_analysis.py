# ============================================================
# Product Affinity Analysis
# ============================================================

import os
import pandas as pd
from config import (CSV_OUTPUT_DIR)
# ============================================================
# Create Output Directory
# ============================================================

os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)

# ============================================================
# Load Association Rules
# ============================================================

association_rules = pd.read_csv(
    os.path.join(CSV_OUTPUT_DIR, "association_rules.csv")
)

print("\nAssociation Rules Loaded Successfully!")
print(f"Total Rules: {len(association_rules)}")

print("\nFirst Five Association Rules:")
print(association_rules.head())

# ============================================================
# Create Product Participation Table
# ============================================================

# Products acting as antecedents
antecedent_df = association_rules.rename(
    columns={
        "antecedents": "Product",
        "consequents": "Related Product"
    }
).copy()

antecedent_df["Role"] = "Antecedent"

# Products acting as consequents
consequent_df = association_rules.rename(
    columns={
        "consequents": "Product",
        "antecedents": "Related Product"
    }
).copy()

consequent_df["Role"] = "Consequent"

# Combine both views
participation_df = pd.concat(
    [antecedent_df, consequent_df],
    ignore_index=True
)

# Reorder columns
participation_df = participation_df[
    [
        "Product",
        "Role",
        "Related Product",
        "support",
        "confidence",
        "lift"
    ]
]

print("\nProduct Participation Table Created Successfully!")
print(f"Total Records: {len(participation_df)}")

print("\nFirst Five Records:")
print(participation_df.head())

print("\nFirst Five Records:")
print(participation_df.head())

# ============================================================
# Save Product Participation Table
# ============================================================

participation_df.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "participation_table.csv")
)

print("\nProduct Participation Table Saved Successfully!")

# ============================================================
# Product Affinity Index (PAI) - Product Metrics
# ============================================================

product_metrics = (
    participation_df
    .groupby("Product")
    .agg(
        Antecedent_Count=("Role", lambda x: (x == "Antecedent").sum()),
        Consequent_Count=("Role", lambda x: (x == "Consequent").sum()),
        Avg_Support=("support", "mean"),
        Avg_Confidence=("confidence", "mean"),
        Avg_Lift=("lift", "mean")
    )
    .reset_index()
)

# ============================================================
# Calculate Total Associations
# ============================================================

product_metrics["Total_Associations"] = (
    product_metrics["Antecedent_Count"] +
    product_metrics["Consequent_Count"]
)

# ============================================================
# Normalize Product Metrics
# ============================================================

# Normalize Total Associations
product_metrics["Norm_Associations"] = (
    (
        product_metrics["Total_Associations"]
        - product_metrics["Total_Associations"].min()
    ) /
    (
        product_metrics["Total_Associations"].max()
        - product_metrics["Total_Associations"].min()
    )
)

# Normalize Average Support
product_metrics["Norm_Support"] = (
    (
        product_metrics["Avg_Support"]
        - product_metrics["Avg_Support"].min()
    ) /
    (
        product_metrics["Avg_Support"].max()
        - product_metrics["Avg_Support"].min()
    )
)

# Normalize Average Confidence
product_metrics["Norm_Confidence"] = (
    (
        product_metrics["Avg_Confidence"]
        - product_metrics["Avg_Confidence"].min()
    ) /
    (
        product_metrics["Avg_Confidence"].max()
        - product_metrics["Avg_Confidence"].min()
    )
)

# Normalize Average Lift
product_metrics["Norm_Lift"] = (
    (
        product_metrics["Avg_Lift"]
        - product_metrics["Avg_Lift"].min()
    ) /
    (
        product_metrics["Avg_Lift"].max()
        - product_metrics["Avg_Lift"].min()
    )
)

# ============================================================
# Calculate Product Affinity Index (PAI)
# ============================================================

product_metrics["Product_Affinity_Index"] = (
    0.40 * product_metrics["Norm_Associations"] +
    0.35 * product_metrics["Norm_Lift"] +
    0.20 * product_metrics["Norm_Confidence"] +
    0.05 * product_metrics["Norm_Support"]
)

product_metrics["Product_Affinity_Index"] = (
    product_metrics["Product_Affinity_Index"].round(4)
)

# ============================================================
# Rank Products by Product Affinity Index
# ============================================================

product_metrics = (
    product_metrics
    .sort_values(
        by="Product_Affinity_Index",
        ascending=False
    )
    .reset_index(drop=True)
)

# ============================================================
# Assign Business Role
# ============================================================

total_products = len(product_metrics)

top_20 = max(1, round(total_products * 0.20))
next_30 = max(1, round(total_products * 0.30))


def assign_role(rank):

    if rank < top_20:
        return "Primary Anchor"

    elif rank < top_20 + next_30:
        return "Secondary Anchor"

    return "Supporting Product"


product_metrics["Business_Role"] = [
    assign_role(i)
    for i in range(total_products)
]

# ============================================================
# Format Numerical Columns
# ============================================================

product_metrics["Avg_Support"] = (
    product_metrics["Avg_Support"].round(4)
)

product_metrics["Avg_Confidence"] = (
    product_metrics["Avg_Confidence"].round(4)
)

product_metrics["Avg_Lift"] = (
    product_metrics["Avg_Lift"].round(2)
)

product_metrics["Product_Affinity_Index"] = (
    product_metrics["Product_Affinity_Index"].round(4)
)

# ============================================================
# Reorder Columns
# ============================================================

product_metrics = product_metrics[
    [
        "Product",
        "Antecedent_Count",
        "Consequent_Count",
        "Total_Associations",
        "Avg_Support",
        "Avg_Confidence",
        "Avg_Lift",
        "Product_Affinity_Index",
        "Business_Role"
    ]
]

# ============================================================
# Save Product Affinity Index
# ============================================================

product_metrics.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "product_affinity_index.csv")
)

print("\nProduct Affinity Index Generated Successfully!")

print("\nTop Products by Product Affinity Index:")
print(product_metrics.head(10))

# ============================================================
# Cross-Sell Recommendation Engine
# ============================================================

# ============================================================
# Prepare Cross-Sell Recommendations
# ============================================================

cross_sell = association_rules[
    [
        "antecedents",
        "consequents",
        "confidence",
        "lift",
        "support"
    ]
].copy()

cross_sell.rename(
    columns={
        "antecedents": "Purchased_Product",
        "consequents": "Recommended_Product",
        "confidence": "Confidence",
        "lift": "Lift",
        "support": "Support"
    },
    inplace=True
)

# ============================================================
# Recommendation Strength
# ============================================================

def recommendation_strength(lift):

    if lift >= 3:
        return "Very Strong"

    elif lift >= 2:
        return "Strong"

    elif lift >= 1.5:
        return "Moderate"

    return "Weak"


cross_sell["Recommendation_Strength"] = (
    cross_sell["Lift"]
    .apply(recommendation_strength)
)

cross_sell = (
    cross_sell
    .sort_values(
        by=[
            "Lift",
            "Confidence"
        ],
        ascending=False
    )
    .reset_index(drop=True)
)

cross_sell["Support"] = (
    cross_sell["Support"].round(4)
)

cross_sell["Confidence"] = (
    cross_sell["Confidence"].round(4)
)

cross_sell["Lift"] = (
    cross_sell["Lift"].round(2)
)

cross_sell.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "cross_sell_recommendations.csv")
)

print("\nCross-Sell Recommendation Engine Completed Successfully!")

print("\nTop Cross-Sell Recommendations:")
print(cross_sell.head(10))

# ============================================================
# Bundle Recommendation Engine
# ============================================================

# ============================================================
# Prepare Bundle Recommendations
# ============================================================

bundle_df = association_rules[
    [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]
].copy()

bundle_df.rename(
    columns={
        "antecedents": "Bundle_Product_1",
        "consequents": "Bundle_Product_2",
        "support": "Support",
        "confidence": "Confidence",
        "lift": "Lift"
    },
    inplace=True
)

# ============================================================
# Bundle Quality
# ============================================================

def bundle_quality(row):

    if row["Lift"] >= 3 and row["Confidence"] >= 0.25:
        return "Premium Bundle"

    elif row["Lift"] >= 2 and row["Confidence"] >= 0.20:
        return "High-Potential Bundle"

    elif row["Lift"] >= 1.5:
        return "Standard Bundle"

    return "Low-Priority Bundle"


bundle_df["Bundle_Quality"] = (
    bundle_df.apply(bundle_quality, axis=1)
)

bundle_df = (
    bundle_df
    .sort_values(
        by=[
            "Lift",
            "Confidence",
            "Support"
        ],
        ascending=False
    )
    .reset_index(drop=True)
)

bundle_df["Support"] = (
    bundle_df["Support"].round(4)
)

bundle_df["Confidence"] = (
    bundle_df["Confidence"].round(4)
)

bundle_df["Lift"] = (
    bundle_df["Lift"].round(2)
)

bundle_df.to_csv(
   os.path.join(CSV_OUTPUT_DIR, "bundle_recommendations.csv")
   )

print("\nBundle Recommendation Engine Completed Successfully!")

print("\nTop Bundle Recommendations:")
print(bundle_df.head(10))

# ============================================================
# Store Layout Optimization
# ============================================================

# ============================================================
# Prepare Store Layout Recommendations
# ============================================================

layout_df = association_rules[
    [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]
].copy()

layout_df.rename(
    columns={
        "antecedents": "Primary_Product",
        "consequents": "Nearby_Product",
        "support": "Support",
        "confidence": "Confidence",
        "lift": "Lift"
    },
    inplace=True
)

# ============================================================
# Placement Recommendation
# ============================================================

def placement_recommendation(lift):

    if lift >= 3:
        return "Adjacent Shelf"

    elif lift >= 2:
        return "Same Display"

    elif lift >= 1.5:
        return "Same Aisle"

    return "Nearby Section"


layout_df["Placement_Recommendation"] = (
    layout_df["Lift"]
    .apply(placement_recommendation)
)

layout_df = (
    layout_df
    .sort_values(
        by=[
            "Lift",
            "Confidence",
            "Support"
        ],
        ascending=False
    )
    .reset_index(drop=True)
)

layout_df["Support"] = (
    layout_df["Support"].round(4)
)

layout_df["Confidence"] = (
    layout_df["Confidence"].round(4)
)

layout_df["Lift"] = (
    layout_df["Lift"].round(2)
)

layout_df = layout_df[
    [
        "Primary_Product",
        "Nearby_Product",
        "Support",
        "Confidence",
        "Lift",
        "Placement_Recommendation"
    ]
]

layout_df.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "store_layout_recommendations.csv")
)

print("\nStore Layout Optimization Completed Successfully!")

print("\nTop Store Layout Recommendations:")
print(layout_df.head(10))

# ============================================================
# Product Pair Affinity Score
# ============================================================

# ============================================================
# Prepare Product Pair Affinity Data
# ============================================================

pair_df = association_rules[
    [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]
].copy()

pair_df.rename(
    columns={
        "antecedents": "Product_1",
        "consequents": "Product_2",
        "support": "Support",
        "confidence": "Confidence",
        "lift": "Lift"
    },
    inplace=True
)

# ============================================================
# Normalize Metrics
# ============================================================

pair_df["Norm_Support"] = (
    (pair_df["Support"] - pair_df["Support"].min()) /
    (pair_df["Support"].max() - pair_df["Support"].min())
)

pair_df["Norm_Confidence"] = (
    (pair_df["Confidence"] - pair_df["Confidence"].min()) /
    (pair_df["Confidence"].max() - pair_df["Confidence"].min())
)

pair_df["Norm_Lift"] = (
    (pair_df["Lift"] - pair_df["Lift"].min()) /
    (pair_df["Lift"].max() - pair_df["Lift"].min())
)

# ============================================================
# Calculate Product Pair Affinity Score
# ============================================================

pair_df["Product_Pair_Affinity_Score"] = (
    0.50 * pair_df["Norm_Lift"] +
    0.30 * pair_df["Norm_Confidence"] +
    0.20 * pair_df["Norm_Support"]
)

pair_df["Product_Pair_Affinity_Score"] = (
    pair_df["Product_Pair_Affinity_Score"].round(4)
)

pair_df = (
    pair_df
    .sort_values(
        by="Product_Pair_Affinity_Score",
        ascending=False
    )
    .reset_index(drop=True)
)

# ============================================================
# Affinity Level
# ============================================================

def affinity_level(score):

    if score >= 0.80:
        return "Excellent"

    elif score >= 0.60:
        return "High"

    elif score >= 0.40:
        return "Moderate"

    return "Low"


pair_df["Affinity_Level"] = (
    pair_df["Product_Pair_Affinity_Score"]
    .apply(affinity_level)
)

pair_df["Support"] = pair_df["Support"].round(4)
pair_df["Confidence"] = pair_df["Confidence"].round(4)
pair_df["Lift"] = pair_df["Lift"].round(2)

pair_df = pair_df[
    [
        "Product_1",
        "Product_2",
        "Support",
        "Confidence",
        "Lift",
        "Product_Pair_Affinity_Score",
        "Affinity_Level"
    ]
]

pair_df.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "product_pair_affinity_scores.csv")
)

print("\nProduct Pair Affinity Score Completed Successfully!")

print("\nTop Product Pairs:")
print(pair_df.head(10))
