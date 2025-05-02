import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans  # <-- Täpselt nii nagu küsisid!
import os

# --- Load and clean data ---
# Define file names
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '706d79f84d75abd81744048179.csv')  # Output name

# 1. Laeme andmed, kasutades semikoolonit ja hüpates üle metaandmete
data = pd.read_csv(file_path, sep=';', skiprows=4)

# 2. Parandame andmed: koma -> punkt ja muudame numbriks
data['Tarbitud energia (võrgust) / kWh'] = (
    data['Tarbitud energia (võrgust) / kWh']
    .str.replace(',', '.')
    .astype(float)
)

# 3. Kuupäeva ja kellaaja töötlemine
data['Periood'] = pd.to_datetime(data['Periood'], format='%d.%m.%Y %H:%M')
data['Kuupäev'] = data['Periood'].dt.date
data['Tund'] = data['Periood'].dt.hour

# 4. Filtreerime välja päevad, millel pole täpselt 24 mõõtmist
measurement_counts = data.groupby('Kuupäev').size()
valid_days = measurement_counts[measurement_counts == 24].index
data_clean = data[data['Kuupäev'].isin(valid_days)]


# 5. Teeme pivot-tabeli: read = kuupäevad, veerud = tunnid
pivot_data = data_clean.pivot(index='Kuupäev', columns='Tund', values='Tarbitud energia (võrgust) / kWh')

# 6. Standardiseerime andmed
scaler = StandardScaler()
X_scaled = scaler.fit_transform(pivot_data)

# 7. Klasterdame KMeans abil kolmeks
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
pivot_data['Cluster'] = labels

# 8. Joonistame klastrite tsentroidid
plt.figure(figsize=(12, 6))
colors = ['blue', 'green', 'red']

for i in range(3):
    centroid_scaled = kmeans.cluster_centers_[i]
    centroid_unscaled = scaler.inverse_transform([centroid_scaled])[0]
    
    plt.plot(range(24), centroid_unscaled, label=f'Klaster {i+1} tsentroid', color=colors[i])

plt.xlabel('Tund')
plt.ylabel('Tarbitud energia (kWh)')
plt.title('Klastrite tsentroidid (keskväärtused)')
plt.legend()
plt.grid(True)
plt.show()

# 9. Kuvame mitu päeva igas klastris
cluster_counts = pivot_data['Cluster'].value_counts().sort_index()
for cluster_id, count in cluster_counts.items():
    print(f"Klaster {cluster_id}: {count} päeva")
