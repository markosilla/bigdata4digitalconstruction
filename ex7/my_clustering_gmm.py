import argparse
import pandas as pd
from sklearn.mixture import GaussianMixture

# --- Command-line arguments ---
parser = argparse.ArgumentParser(description="K-Means clustering for building data")
parser.add_argument('--k', type=int, default=4, help='Number of clusters (default: 4)')
parser.add_argument('--csv', type=str, default='buildings.csv', help='Path to input CSV file (default: buildings.csv)')
args = parser.parse_args()

# --- Load data ---
data = pd.read_csv(args.csv)

# --- Ordinal mapping for energiaKlass ---
energia_map = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
}

if 'energiaKlass' in data.columns:
    data['energiaKlass_mapped'] = data['energiaKlass'].map(energia_map)
    # If any unmapped values exist (e.g., NaN), they'll be dropped below

# --- Select features for clustering ---
features = [
    'esmane_kasutus',
    'suletud_netopind',
    'ehitiseMaht',
    'maxKorrusteArv',
    'ehitisalunePind',
    'mahtBruto',
    #'yldkasut_pind'
]

if 'energiaKlass_mapped' in data.columns:
    features.append('energiaKlass_mapped')

# --- Drop rows with missing values in selected columns ---
data = data.dropna(subset=features)

# --- GMM Clustering ---
gmm = GaussianMixture(n_components=args.k, random_state=42)
data['Cluster'] = gmm.fit_predict(data[features])

# --- Print out cluster summaries ---
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
