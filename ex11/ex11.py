import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import os
import numpy as np

# --- Load and clean data ---
# Define file names
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '706d79f84d75abd81744048179.csv')  # Output name

# Read CSV
raw = pd.read_csv(file_path, sep=';', skiprows=4)
raw.columns = ['timestamp', 'energy']
raw = raw.dropna()
raw['energy'] = raw['energy'].str.replace(',', '.').astype(float)
raw['timestamp'] = pd.to_datetime(raw['timestamp'], format='%d.%m.%Y %H:%M')

# --- Prepare daily data ---
raw['date'] = raw['timestamp'].dt.date
raw['hour'] = raw['timestamp'].dt.hour

# Pivot table: each row = a day, each column = an hour
pivot = raw.pivot_table(index='date', columns='hour', values='energy')

# Drop days with missing hours
pivot = pivot.dropna()

# --- Find 3 most similar days ---
# Compute pairwise distances
distances = euclidean_distances(pivot)

# Mask the diagonal (distance to itself)
np.fill_diagonal(distances, np.inf)

# Find the closest pair
i, j = np.unravel_index(np.argmin(distances), distances.shape)

# Get these two days
similar_days = [pivot.index[i], pivot.index[j]]

# Find the third most similar day to these two
remaining = [k for k in range(len(pivot)) if k not in (i, j)]
third_idx = min(remaining, key=lambda k: distances[i, k] + distances[j, k])
similar_days.append(pivot.index[third_idx])

# --- Print out distances between the selected days ---
print("Distances between selected days:")
day1, day2, day3 = similar_days

print(f"{day1} ↔ {day2}: {distances[i, j]:.6f}")
print(f"{day1} ↔ {day3}: {distances[i, third_idx]:.6f}")
print(f"{day2} ↔ {day3}: {distances[j, third_idx]:.6f}")
print(f"Total distance: {(distances[i, j] + distances[i, third_idx] + distances[j, third_idx]):.6f}")

# --- Plotting ---
plt.figure(figsize=(10,6))

for day in similar_days:
    plt.plot(pivot.columns, pivot.loc[day], label=str(day))

plt.xlabel('Hour of Day')
plt.ylabel('Energy Consumption (kWh)')
plt.title('3 Most Similar Days')
plt.legend()
plt.grid(True)
plt.show()
