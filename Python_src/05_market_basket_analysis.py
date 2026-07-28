# ==========================================
# MARKET BASKET ANALYSIS USING APRIORI
# ==========================================
import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from config import CSV_OUTPUT_DIR

# ==========================================
# PARAMETERS
# ==========================================

MIN_SUPPORT = 0.01
MIN_CONFIDENCE = 0.20

# ==========================================
# STEP 1: LOAD CLEANED DATASET
# ==========================================

print("=" * 60)
print("MARKET BASKET ANALYSIS")
print("=" * 60)

df = pd.read_csv(
    os.path.join(CSV_OUTPUT_DIR, "cleaned_transactions.csv")
)

print("\nFIRST FIVE ROWS OF CLEANED DATASET")
print("-" * 60)
print(df.head())

print("\nDataset Shape:", df.shape)

# ==========================================
# STEP 2: CREATE TRANSACTION MATRIX
# ==========================================

print("\n" + "=" * 60)
print("CREATING TRANSACTION MATRIX")
print("=" * 60)

transaction_matrix = df.pivot_table(
    index="order_id",
    columns="product_name",
    aggfunc=len,
    fill_value=0
).astype(bool)

print("\nTransaction Matrix Shape:")
print(transaction_matrix.shape)

print("\nFirst Five Rows of Transaction Matrix")
print("-" * 60)
print(transaction_matrix.head())

# ==========================================
# STEP 3: GENERATE FREQUENT ITEMSETS
# ==========================================

print("\n" + "=" * 60)
print("GENERATING FREQUENT ITEMSETS")
print("=" * 60)

frequent_itemsets = apriori(
    transaction_matrix,
    min_support=MIN_SUPPORT,
    use_colnames=True
)

print(f"\nTotal Frequent Itemsets Found: {len(frequent_itemsets)}")

# Calculate itemset length
frequent_itemsets["length"] = frequent_itemsets["itemsets"].apply(len)

print("\nItemset Length Distribution")
print("-" * 60)
print(frequent_itemsets["length"].value_counts())

print("\nFrequent 1-Itemsets")
print("-" * 60)
print(
    frequent_itemsets[
        frequent_itemsets["length"] == 1
    ]
)

print("\nFrequent 2-Itemsets")
print("-" * 60)
print(
    frequent_itemsets[
        frequent_itemsets["length"] == 2
    ]
)

# ==========================================
# STEP 4: GENERATE ASSOCIATION RULES
# ==========================================

print("\n" + "=" * 60)
print("GENERATING ASSOCIATION RULES")
print("=" * 60)

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=MIN_CONFIDENCE
)

# ==========================================
# STEP 5: FORMAT OUTPUT
# ==========================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

rules = rules.sort_values(
    by="lift",
    ascending=False
)

# Keep only useful columns
rules = rules[
    [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]
]

# Convert frozensets to readable strings
rules["antecedents"] = rules["antecedents"].apply(
    lambda x: ", ".join(sorted(list(x)))
)

rules["consequents"] = rules["consequents"].apply(
    lambda x: ", ".join(sorted(list(x)))
)

# Round numerical values
rules["support"] = rules["support"].round(4)
rules["confidence"] = rules["confidence"].round(4)
rules["lift"] = rules["lift"].round(4)

print("\nTop 10 Association Rules")
print("-" * 60)
print(rules.head(10))

# ==========================================
# STEP 6: FORMAT FREQUENT ITEMSETS
# ==========================================

frequent_itemsets["itemsets"] = frequent_itemsets["itemsets"].apply(
    lambda x: ", ".join(sorted(list(x)))
)

frequent_itemsets["support"] = frequent_itemsets["support"].round(4)

# ==========================================
# STEP 7: SAVE RESULTS
# ==========================================

frequent_itemsets.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "frequent_itemsets.csv"),
)

rules.to_csv(
    os.path.join(CSV_OUTPUT_DIR, "association_rules.csv"),
)

# ==========================================
# COMPLETION MESSAGE
# ==========================================

print("\n" + "=" * 60)
print("MARKET BASKET ANALYSIS COMPLETED")
print("=" * 60)

print("✓ Frequent Itemsets Generated")
print("✓ Association Rules Generated")
print("✓ frequent_itemsets.csv Saved")
print("✓ association_rules.csv Saved")

print("\nResults saved successfully!")