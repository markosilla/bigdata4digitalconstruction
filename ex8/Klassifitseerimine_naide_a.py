import pandas as pd  # Imporditakse pandas teek nimega pd andmete töötlemiseks
from sklearn.preprocessing import LabelEncoder  # Imporditakse LabelEncoder kategooriliste muutujate numbriliseks kodeerimiseks
from sklearn.tree import DecisionTreeClassifier  # Imporditakse DecisionTreeClassifier otsustuspuu klassifitseerija loomiseks
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'weather-nominal-weka.csv')

# Loetakse andmestik failist
#file_path = 'weather-nominal-weka.csv'  # Määratakse muutuja file_path väärtuseks faili asukoht

df = pd.read_csv(file_path)  # Loetakse CSV fail pandas DataFrame'iks df

# Kodeeritakse kategoorilised muutujad numbriliseks kasutades LabelEncoder'it
label_encoder = LabelEncoder()  # Loome LabelEncoder objekti
for col in df.columns:  # Käiakse tsükliga läbi kõik veerud DataFrame'is df
    df[col] = label_encoder.fit_transform(df[col])  # Kodeeritakse veeru väärtused numbriliseks

# Eraldatakse sisend- ja väljundandmed
X = df.drop('play', axis=1)  # Eraldatakse sisendandmed muutujasse X, eemaldades veeru 'play'
y = df['play']  # Eraldatakse sihtmärgi (väljundi) veerg y

# Treenitakse otsustuspuu klassifitseerimisemudel
clf = DecisionTreeClassifier(random_state=42)  # Loome DecisionTreeClassifier objekti nimega clf
clf.fit(X, y)  # Treenime klassifitseerimismudeli clf kasutades X ja y

# Tehakse ennustused treeningandmete peal (lihtsustus õpetamisel, tegelikult peaks eraldi testandmed olema)
predictions = clf.predict(X)  # Tehakse ennustused

# Ennustatud numbrilised väärtused teisendatakse tagasi algseteks siltideks
predicted_labels = label_encoder.inverse_transform(predictions)  # Teisendatakse ennustatud väärtused tagasi siltideks

# Lisatakse ennustatud sildid DataFrame'ile
df['predicted_play'] = predicted_labels  # Lisatakse df-le veerg ennustatud väärtustega

# Tegelikud 'play' sildid teisendatakse tagasi algseteks vormideks, kui need olid kodeeritud
df['actual_play'] = label_encoder.inverse_transform(df['play'])  # Lisatakse df-le veerg tegelike väärtustega

# Valitakse kuvamiseks ainult asjakohased veerud
comparison_df = df[['predicted_play', 'actual_play']]  # Luuakse uus DataFrame võrdluseks

# Kuvatakse võrdluse DataFrame
print(comparison_df)  # Prinditakse võrdlus, näitamaks ennustatud ja tegelikke väärtusi