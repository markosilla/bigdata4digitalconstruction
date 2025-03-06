import pandas as pd
import numpy as np
import os

print(os.getcwd())

################################################################################
# USER SETTINGS
################################################################################
CSV_FILE = 'ex5/bank-data.csv'             # Input CSV file
OUTPUT_FIMI_FILE = 'ex5/input2.txt'   # Output file for FIMI format

# Columns to remove entirely (e.g., unique IDs)
COLUMNS_TO_REMOVE = ['id']

# Numeric columns to discretize
NUMERIC_TO_DISCRETIZE = ['age', 'income']

# Number of bins for discretization (equi-width)
N_BINS = 5

################################################################################
# 1. LOAD DATA
################################################################################
df = pd.read_csv(CSV_FILE)
print("Original data (head):")
#display(df.head())

################################################################################
# 2. REMOVE UNWANTED COLUMNS
################################################################################
df.drop(columns=COLUMNS_TO_REMOVE, inplace=True, errors='ignore')
print(f"\nDropped columns: {COLUMNS_TO_REMOVE}")

################################################################################
# 3. DISCRETIZE SELECTED NUMERIC COLUMNS
#    - Replaces numeric values with a label like "age_10.0_20.0"
################################################################################
def discretize_numeric(df, col, nbins=5):
    """
    Discretize column 'col' into 'nbins' equi-width bins.
    Each value is replaced with a label of the form: "col_left_right".
    """
    if col not in df.columns:
        return
    col_min = df[col].min()
    col_max = df[col].max()
    # If the column is empty or has NaNs only, skip
    if pd.isna(col_min) or pd.isna(col_max):
        return

    # Create equi-width bin edges
    edges = np.linspace(col_min, col_max, nbins + 1)

    # Use pd.cut to bin the values
    binned = pd.cut(df[col], bins=edges, include_lowest=True, right=False)

    # Convert each bin Interval to a string label
    labels = []
    for iv in binned:
        if pd.isna(iv):
            labels.append(np.nan)
        else:
            left = f"{iv.left:.1f}"
            right = f"{iv.right:.1f}"
            labels.append(f"{col}_{left}_{right}")

    df[col] = labels

# Apply discretization to each specified numeric column
for col in NUMERIC_TO_DISCRETIZE:
    discretize_numeric(df, col, nbins=N_BINS)

print("\nData after discretization (head):")
#display(df.head())

################################################################################
# 4. BUILD FIMI TRANSACTIONS
#    - Each row becomes a list of items
#    - Numeric columns are now bin labels, e.g. "age_10.0_20.0"
#    - Other columns become "col_val"
################################################################################
transactions = []
for _, row in df.iterrows():
    items = []
    for col in df.columns:
        val = row[col]
        if pd.notna(val):
            # If this column was discretized, it's already something like "age_10.0_20.0"
            # Otherwise, for categorical columns, do "col_val"
            if col in NUMERIC_TO_DISCRETIZE:
                items.append(str(val))
            else:
                items.append(f"{col}_{val}")
    transactions.append(items)

################################################################################
# 5. WRITE OUT FIMI FILE
#    - One line per transaction, space-separated items
################################################################################
with open(OUTPUT_FIMI_FILE, 'w') as f:
    for trans in transactions:
        line = ' '.join(trans)
        f.write(line + '\n')

print(f"\nFIMI transactions saved to '{OUTPUT_FIMI_FILE}'.")

# OPTIONAL: download the output file from Google Colab
# files.download(OUTPUT_FIMI_FILE)