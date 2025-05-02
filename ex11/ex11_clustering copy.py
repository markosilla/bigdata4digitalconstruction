import pandas as pd
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import os

# Define file names
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '706d79f84d75abd81744048179.csv')  # Output name

# 1. Laeme andmed (semikooloniga ja vahelejätame esimesed read)
data = pd.read_csv(file_path, sep=';', skiprows=4)

# 2. Muudame energia veeru õigeks numbriks
data['Tarbitud energia (võrgust) / kWh'] = (
    data['Tarbitud energia (võrgust) / kWh']
    .str.replace(',', '.')
    .astype(float)
)

# 3. Muudame kuupäeva ja kellaaja datetime'ks
data['Periood'] = pd.to_datetime(data['Periood'], format='%d.%m.%Y %H:%M')
data['Kuupäev'] = data['Periood'].dt.date
data['Tund'] = data['Periood'].dt.hour

# 4. Filtreerime ainult need päevad, millel on täpselt 24 mõõtmist
measurement_counts = data.groupby('Kuupäev').size()
valid_days = measurement_counts[measurement_counts == 24].index
data_clean = data[data['Kuupäev'].isin(valid_days)]

# 5. Pivot: read = kuupäevad, veerud = tunnid (0-23)
pivot_data = data_clean.pivot(index='Kuupäev', columns='Tund', values='Tarbitud energia (võrgust) / kWh')

# 6. Skaleerime kõik päevad null keskmise ja ühikvariatsiooniga
scaler = TimeSeriesScalerMeanVariance()
X_scaled = scaler.fit_transform(pivot_data.values[:, :, None])  # kuju: (päevade arv, 24, 1)

# 7. Klasterdame DTW põhjal
model = TimeSeriesKMeans(n_clusters=3, metric="dtw", random_state=42)
labels = model.fit_predict(X_scaled)

# 8. Lisame klastrisildid pivot-tabelisse
pivot_data['Cluster'] = labels

# 9. Joonistame klastrite tsentroidid
plt.figure(figsize=(12, 6))
colors = ['blue', 'green', 'red']

for i in range(3):
    centroid = model.cluster_centers_[i].ravel()
    plt.plot(range(24), centroid, label=f'Klaster {i+1} tsentroid (DTW)', color=colors[i])

plt.xlabel('Tund')
plt.ylabel('Tarbitud energia (kWh)')
plt.title('Klastrite tsentroidid (kasutades Dynamic Time Warping)')
plt.legend()
plt.grid(True)
plt.show()

# 10. Kuvame mitu päeva igas klastris
cluster_counts = pivot_data['Cluster'].value_counts().sort_index()
for cluster_id, count in cluster_counts.items():
    print(f"Klaster {cluster_id}: {count} päeva")
