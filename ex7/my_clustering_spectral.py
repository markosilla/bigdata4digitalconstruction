import argparse
import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler

# --- Command-line argument parsing ---
parser = argparse.ArgumentParser(description="Spectral clustering for building data")
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

# --- Spectral Clustering ---
spectral_clust = SpectralClustering(n_clusters=args.k, affinity='nearest_neighbors', random_state=42, assign_labels='kmeans')
data['Cluster'] = spectral_clust.fit_predict(features_scaled)

# --- Cluster Summary Output ---
for cluster in range(args.k):
    cluster_data = data[data['Cluster'] == cluster]
    print(f'Cluster {cluster + 1}')
    buildings = cluster_data['EHRkood'].tolist()
    print('Buildings:', buildings)

    print('Average Values:')
    for column in features:
        print(f'{column}: {cluster_data[column].mean():.2f}')

    if 'linn' in cluster_data.columns:
        city_mode = cluster_data['linn'].mode().iloc[0]
        print(f'Most frequent City: {city_mode}')
    
    print('')
