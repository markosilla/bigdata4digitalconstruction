import argparse
import pandas as pd
import numpy as np
from sklearn.cluster import (
    KMeans, MiniBatchKMeans, AgglomerativeClustering, SpectralClustering,
    DBSCAN, OPTICS, MeanShift, Birch
)
from sklearn.preprocessing import LabelEncoder

# --- Command-line arguments ---
parser = argparse.ArgumentParser(description="Universal clustering for building data")
parser.add_argument('--k', type=int, default=4, help='Number of clusters (default: 4). Ignored by DBSCAN, OPTICS, MeanShift.')
parser.add_argument('--csv', type=str, default='buildings.csv', help='Path to input CSV file')
parser.add_argument('--method', type=str, default='KMeans',
                    choices=["KMeans", "MiniBatchKMeans", "AgglomerativeClustering", "SpectralClustering",
                             "DBSCAN", "OPTICS", "MeanShift", "Birch"],
                    help='Clustering method to use')
args = parser.parse_args()

# --- Load and prepare data ---
df = pd.read_csv(args.csv)
clustering_method = args.method
k = args.k

if "id" in df.columns:
    df = df.drop(columns=["id"])

# Map energiaKlass (ordinal)
energia_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
df['energiaKlass'] = df['energiaKlass'].map(energia_map)

# Handle missing values
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].mean())

# Identify numeric and categorical columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

# Label encode categorical columns
df_for_cluster = df.copy()
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_for_cluster[col] = le.fit_transform(df_for_cluster[col])
    label_encoders[col] = le

# --- Select and fit clustering model ---
if clustering_method == "KMeans":
    model = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
elif clustering_method == "MiniBatchKMeans":
    model = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=100)
elif clustering_method == "AgglomerativeClustering":
    model = AgglomerativeClustering(n_clusters=k)
elif clustering_method == "SpectralClustering":
    model = SpectralClustering(n_clusters=k, affinity='nearest_neighbors', random_state=42, assign_labels='kmeans')
elif clustering_method == "DBSCAN":
    model = DBSCAN(eps=0.5, min_samples=5)  # You can tune these
elif clustering_method == "OPTICS":
    model = OPTICS(min_samples=5, xi=0.05, min_cluster_size=0.1)  # Good defaults
elif clustering_method == "MeanShift":
    model = MeanShift()
elif clustering_method == "Birch":
    model = Birch(n_clusters=k)
else:
    raise ValueError("Invalid clustering method selected.")

# --- Fit and assign cluster labels ---
df_for_cluster["Cluster"] = model.fit_predict(df_for_cluster)
df["Cluster"] = df_for_cluster["Cluster"]

# --- Print cluster sizes ---
print("Cluster sizes:")
cluster_sizes = df["Cluster"].value_counts().sort_index()
for cluster, count in cluster_sizes.items():
    print(f"Cluster {cluster}: {count}")

# --- Compute and print centroids (exclude EHRkood) ---
categorical_cols_cleaned = [col for col in categorical_cols if col != "EHRkood"]
centroids_numeric = df.groupby("Cluster")[numeric_cols].mean()
centroids_categorical = df.groupby("Cluster")[categorical_cols_cleaned].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "N/A")
centroids_df = pd.concat([centroids_numeric, centroids_categorical], axis=1)
ordered_cols = numeric_cols + categorical_cols_cleaned
centroids_df = centroids_df[ordered_cols]

# --- Display output neatly ---
pd.set_option("display.width", 1000)
pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)

print("\nCluster Centroids (features as rows, clusters as columns):")
print(centroids_df.transpose())

# --- Show buildings per cluster ---
if "EHRkood" in df.columns:
    print("\nBuildings per cluster:")
    for cluster in sorted(df["Cluster"].unique()):
        buildings_in_cluster = df[df["Cluster"] == cluster]["EHRkood"].tolist()
        print(f"\nCluster {cluster} ({len(buildings_in_cluster)} buildings):")
        print(buildings_in_cluster)
