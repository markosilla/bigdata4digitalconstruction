import argparse
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# --- Command-line argument parsing ---
parser = argparse.ArgumentParser(description="Agglomerative clustering for building data")
parser.add_argument('--k', type=int, default=3, help='Number of clusters (default: 3)')
parser.add_argument('--csv', type=str, default='buildings.csv', help='Path to input CSV file (default: buildings.csv)')
args = parser.parse_args()

# --- Read CSV data ---
data = pd.read_csv(args.csv)

# --- Ordinal mapping for energiaKlass ---
energia_map = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
}
data['energiaKlass_num'] = data['energiaKlass'].map(energia_map)

# --- Features for clustering ---
features = [
    'ehitisePindala',
    'ehitiseMaht',
    'ehitisalunePind',
    'suletud_netopind',
    'mahtBruto',
    'maxKorrusteArv',
    #'yldkasut_pind',
    'esmane_kasutus',
    'energiaKlass_num'
]

# --- Drop rows with missing values ---
data = data.dropna(subset=features)

# --- Standardize features ---
scaler = StandardScaler()
features_scaled = scaler.fit_transform(data[features])

# --- Agglomerative Clustering ---
agg_clust = AgglomerativeClustering(n_clusters=args.k, linkage='ward')
data['Cluster'] = agg_clust.fit_predict(features_scaled)

# --- Dendrogram ---
linked = linkage(features_scaled, method='ward')
plt.figure(figsize=(12, 7))
dendrogram(
    linked,
    orientation='top',
    labels=data['EHRkood'].astype(str).values,
    distance_sort='descending',
    show_leaf_counts=True,
    leaf_rotation=90
)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('EHRkood')
plt.ylabel('Distance')
plt.tight_layout()
plt.show()

# --- Print cluster summaries ---
for cluster in range(args.k):
    cluster_data = data[data['Cluster'] == cluster]
    print(f'\nCluster {cluster + 1}')
    ehrkood_list = cluster_data['EHRkood'].tolist()
    print('EHRkood:', ehrkood_list)

    print('Average Values:')
    for column in features:
        if column == 'energiaKlass_num':
            # Convert numeric back to label for readability
            inv_map = {v: k for k, v in energia_map.items()}
            numeric_mode = cluster_data[column].mode().iloc[0]
            print(f'energiaKlass (mode): {inv_map.get(numeric_mode, "Unknown")}')
        else:
            print(f'{column}: {cluster_data[column].mean():.2f}')

    # Most frequent city
    if not cluster_data['linn'].mode().empty:
        city_mode = cluster_data['linn'].mode().iloc[0]
    else:
        city_mode = 'N/A'
    print(f'Most frequent City: {city_mode}')
