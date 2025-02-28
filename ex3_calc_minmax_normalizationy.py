import pandas as pd
import numpy as np

# Define mapping to iterate in order
buildings_map = {
    "121363179": ("222", "Pärnu Rääma tn 9"),
    "121363182": ("222", "Pärnu Rääma tn 9a"),
    "121363185": ("222", "Pärnu Rääma tn 11"),
    "103014811": ("223", "Pärnu Mai 39"),
    "103015648": ("223", "Pärnu Mai 45"),
    "103015786": ("223", "Pärnu Mai 43"),
    "104018086": ("224", "Tartu Mõisavahe 35"),
    "104018376": ("224", "Tartu Mõisavahe 38"),
    "104023804": ("224", "Tartu Mõisavahe 42"),
    "104018213": ("225", "Tartu Mõisavahe 43"),
    "104019313": ("225", "Tartu Mõisavahe 47"),
    "104036004": ("225", "Tartu Mõisavahe 39")
}

# Load data from CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    df["energiaKlass"] = df["energiaKlass"].map({"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}).fillna(0)
    filenames = df["filename"].astype(str).str.replace(".ehr.json", "", regex=False).tolist()
    data = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0).values  # Convert numeric columns
    return filenames, data

# Normalize data using Min-Max Scaling
def normalize_minmax(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    return (data - min_vals) / (max_vals - min_vals + 1e-8)  # Avoid division by zero

# Compute Euclidean Distance Matrix
def calculate_euclidean_distances(matrix):
    size = len(matrix)
    dist_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dist_matrix[i, j] = np.sqrt(np.sum((matrix[i] - matrix[j])**2))
    return dist_matrix

# Load and process data
file_path = "ehr_files/output.csv"
filenames, data = load_data(file_path)

if len(data) == 0:
    print("No valid data found.")
    exit()

# Normalize data
normalized_data = normalize_minmax(data)

# Compute Euclidean Distance Matrix
distance_matrix = calculate_euclidean_distances(normalized_data)

# Reorder results based on buildings_map
ehr_codes = [code for code in buildings_map.keys() if code in filenames]
distance_df = pd.DataFrame(distance_matrix, index=filenames, columns=filenames)
distance_df = distance_df.loc[ehr_codes, ehr_codes]
distance_df = distance_df.reindex(index=ehr_codes, columns=ehr_codes)

# Print Euclidean Distance Matrix to console
print("\nEuclidean Distance Matrix:")
print(distance_df.to_csv(index=True))
