import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Lae oma andmed
df = pd.read_csv("buildings.csv")

# Muuda kategooriad numbrilisteks (nt 'linn', 'energiaKlass')
energia_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
df['energiaKlass'] = df['energiaKlass'].map(energia_map)
df = df.fillna(df.mean(numeric_only=True))

categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
for col in categorical_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# --- Elbow meetodi testimine ---
X = df.drop(columns=["EHRkood"])  # kasuta ainult numbrilisi tunnuseid

inertia_values = []
k_values = range(1, 10)

for k in k_values:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    inertia_values.append(model.inertia_)

# --- Joonista graafik ---
plt.figure(figsize=(8, 4))
plt.plot(k_values, inertia_values, marker='o')
plt.title("Elbow Method for Optimal k")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia (sum of squared distances)")
plt.grid(True)
plt.tight_layout()
plt.show()
