import pandas as pd
import os
from config import CSV_OUTPUT_DIR

# ==========================================
# TRANSACTION MATRIX CREATION
# ==========================================

print("=" * 50)
print("TRANSACTION MATRIX")
print("=" * 50)

# ------------------------------------------
# Step 1: Load the cleaned transaction data
# ------------------------------------------
df = pd.read_csv(
    os.path.join(CSV_OUTPUT_DIR, "cleaned_transactions.csv")
)

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nFirst Five Rows:")
print(df.head())

# ------------------------------------------
# Step 2: Create Transaction Matrix
# ------------------------------------------
# Each row represents an order (transaction)
# Each column represents a unique product
# Values indicate whether the product appears
# in the order.

transaction_matrix = df.pivot_table(
    index="order_id",
    columns="product_name",
    aggfunc=len,
    fill_value=0
)

# ------------------------------------------
# Step 3: Display Matrix Information
# ------------------------------------------
print("\nTransaction Matrix Shape:")
print(transaction_matrix.shape)

print("\nFirst Five Rows of Transaction Matrix:")
print(transaction_matrix.head())

# --------------------------------------------------
# Step 4: Convert to Boolean Matrix
# --------------------------------------------------

transaction_matrix = transaction_matrix.astype(bool)

print("\nData Type After Conversion:")
print(transaction_matrix.dtypes.head())

# --------------------------------------------------
# Step 5: Memory Usage
# --------------------------------------------------

memory_usage = transaction_matrix.memory_usage(deep=True).sum() / (1024 ** 2)

print("\nMemory Usage:")
print(f"{memory_usage:.2f} MB")

# --------------------------------------------------
# Step 6: Save Transaction Matrix (Optional)
# --------------------------------------------------

save_matrix = False

if save_matrix:
    transaction_matrix.to_csv(
       os.path.join(CSV_OUTPUT_DIR, "transaction_matrix.csv"),
    )
    print("\nTransaction Matrix saved successfully!")
else:
    print("\nTransaction Matrix not saved (using in-memory DataFrame).")

