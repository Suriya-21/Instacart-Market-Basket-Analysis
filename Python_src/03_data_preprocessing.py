import os
from config import CSV_OUTPUT_DIR
from utils.database import load_transactions

# Load transaction data
df = load_transactions(500000)

print("=" * 50)
print("DATA PREPROCESSING")
print("=" * 50)

# -----------------------------
# Dataset Overview
# -----------------------------
print("\nDataset Shape:")
print(df.shape)

# -----------------------------
# Missing Values
# -----------------------------
print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------------
# Duplicate Rows
# -----------------------------
duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)

# -----------------------------
# Duplicate Products in Same Order
# -----------------------------
duplicate_products = df.duplicated(
    subset=["order_id", "product_name"]
).sum()

print("\nDuplicate Products Within Same Order:")
print(duplicate_products)

print("\nDataset Shape After Cleaning:")
print(df.shape)

# Save cleaned data
df.to_csv(
   os.path.join(CSV_OUTPUT_DIR, "cleaned_transactions.csv"),
)

print("\nCleaned dataset saved successfully!")