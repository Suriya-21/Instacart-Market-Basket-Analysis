# ==========================================
# MARKET BASKET ANALYSIS VISUALIZATIONS
# ==========================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    CSV_OUTPUT_DIR,
    IMAGE_OUTPUT_DIR
)

# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

print("=" * 60)
print("MARKET BASKET ANALYSIS VISUALIZATIONS")
print("=" * 60)

frequent_itemsets = pd.read_csv(
    os.path.join(CSV_OUTPUT_DIR, "frequent_itemsets.csv"),
)

association_rules = pd.read_csv(
    os.path.join(CSV_OUTPUT_DIR, "association_rules.csv"),
)

print("\nFrequent Itemsets Shape:", frequent_itemsets.shape)
print("Association Rules Shape:", association_rules.shape)

print("\nData Loaded Successfully!")

# ==========================================
# TOP 10 MOST FREQUENT PRODUCTS
# ==========================================

top_products = (
    frequent_itemsets[
        frequent_itemsets["length"] == 1
    ]
    .sort_values(
        by="support",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(14,7))

plt.bar(
    top_products["itemsets"],
    top_products["support"],
    edgecolor="black"
)

plt.title(
    "Top 10 Most Frequent Products",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Product",
    fontsize=12
)

plt.ylabel(
    "Support",
    fontsize=12
)

plt.xticks(rotation=45, ha="right")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_OUTPUT_DIR, "top_10_products.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("✓ Top 10 Products chart saved.")

# ==========================================
# TOP 10 ASSOCIATION RULES BY LIFT
# ==========================================

top_rules = (
    association_rules
    .sort_values(
        by="lift",
        ascending=False
    )
    .head(10)
)

top_rules["rule"] = (
    top_rules["antecedents"]
    + " → "
    + top_rules["consequents"]
)

plt.figure(figsize=(14,7))

plt.barh(
    top_rules["rule"],
    top_rules["lift"],
    edgecolor="black"
)

plt.title(
    "Top 10 Association Rules by Lift",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Lift",
    fontsize=12
)

plt.ylabel(
    "Association Rule",
    fontsize=12
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_OUTPUT_DIR, "top_10_rules_by_lift.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("✓ Top 10 Association Rules by Lift chart saved.")

# ==========================================
# TOP 10 ASSOCIATION RULES BY CONFIDENCE
# ==========================================

top_confidence = (
    association_rules
    .sort_values(
        by="confidence",
        ascending=False
    )
    .head(10)
)

top_confidence["rule"] = (
    top_confidence["antecedents"]
    + " → "
    + top_confidence["consequents"]
)

plt.figure(figsize=(14,7))

plt.barh(
    top_confidence["rule"],
    top_confidence["confidence"],
    edgecolor="black"
)

plt.title(
    "Top 10 Association Rules by Confidence",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Confidence",
    fontsize=12
)

plt.ylabel(
    "Association Rule",
    fontsize=12
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_OUTPUT_DIR, "top_10_rules_by_confidence.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("✓ Top 10 Association Rules by Confidence chart saved.")

# ==========================================
# SUPPORT VS CONFIDENCE (LIFT AS COLOR)
# ==========================================

plt.figure(figsize=(10, 7))

scatter = plt.scatter(
    association_rules["support"],
    association_rules["confidence"],
    c=association_rules["lift"],
    cmap="viridis",
    s=120,
    edgecolors="black",
    alpha=0.8
)

plt.colorbar(
    scatter,
    label="Lift"
)

plt.title(
    "Support vs Confidence of Association Rules",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Support",
    fontsize=12
)

plt.ylabel(
    "Confidence",
    fontsize=12
)

plt.grid(
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_OUTPUT_DIR, "support_vs_confidence.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("✓ Support vs Confidence Scatter Plot saved.")

# ==========================================
# CORRELATION HEATMAP
# ==========================================

correlation = association_rules[
    [
        "support",
        "confidence",
        "lift"
    ]
].corr()

plt.figure(figsize=(8,6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="YlGnBu",
    linewidths=0.5,
    fmt=".2f"
)

plt.title(
    "Correlation Between Support, Confidence and Lift",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    os.path.join(IMAGE_OUTPUT_DIR, "top_10_correlation.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("✓ Correlation Heatmap saved.")
