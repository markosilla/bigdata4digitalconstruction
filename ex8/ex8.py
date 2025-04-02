import pandas as pd
import os
import pandas as pd  # Impordib pandas teeki lühendatud nimetusega "pd".
from sklearn.model_selection import train_test_split  # Impordib funktsiooni andmekogumi jagamiseks treening- ja testandmeteks.
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Impordib klassi muutujate ümberskaleerimiseks.
from sklearn.metrics import accuracy_score  # Impordib funktsiooni mudeli ennustuste täpsuse hindamiseks.
from sklearn.linear_model import LogisticRegression  # Impordib LogisticRegression klassifikaatori.
from sklearn.neighbors import KNeighborsClassifier  # Impordib KNeighborsClassifier klassifikaatori.
from sklearn.svm import SVC  # Impordib SVC (Support Vector Machine) klassifikaatori.
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier  # Impordib RandomForest ja GradientBoosting klassifikaatorid.
from sklearn.tree import DecisionTreeClassifier  # Impordib DecisionTreeClassifier klassifikaatori.
from sklearn.naive_bayes import BernoulliNB # Proovi NaiveBayes
import os

# Define file names
current_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_file = os.path.join(current_dir, 'Apartment_Building_Dataset.xlsx')  # ← Replace with your filename
csv_file = os.path.join(current_dir, 'Apartment_Building_Dataset.csv')    # Output name

# Read Excel
df = pd.read_excel(xlsx_file)

# Write CSV
df.to_csv(csv_file, index=False)

print(f"Converted {xlsx_file} → {csv_file}")

data = pd.read_csv(csv_file)  # Loeb CSV-faili pandas DataFrame'i.


# Set prediction target
target_column = 'Energy_Certificate_Class'

# Drop columns you don’t need or that leak the target
data.drop(columns=['ID', 'EHR_kood', 'TaisAadress', 'Maakond', 'KOV', 'KOV_voi_LinnaOsa', 'Tänav_Hoone_Nr'], inplace=True, errors='ignore')

# Drop rows where target is missing
data.dropna(subset=[target_column], inplace=True)

# Encode target labels
label_encoder = LabelEncoder()
data[target_column] = label_encoder.fit_transform(data[target_column])

# Separate features and target
X = data.drop(columns=[target_column])
y = data[target_column]

# Optional: Fill missing values
X = X.fillna(0)

# Teisendab kategoorilised tunnused one-hot kodeeringuks.
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Jagab andmed.

# Skaalib funktsioonid.
scaler = StandardScaler()  # Loob ümberskaleerimise objekti.
X_train = scaler.fit_transform(X_train)  # skaleerib treeningandmed ümber
X_test = scaler.transform(X_test)  # skaleerib testandmed ümber

# Klassifikaatorite valik (ise kommenteeri välja ja sisse, mida soovid!)
#clf = DecisionTreeClassifier(random_state=42) # Kasutab DecisionTree (otsustuspuu) klassifikaatorit.
#clf = KNeighborsClassifier()
#clf = LogisticRegression(random_state=42)
#clf = SVC(random_state=42)
#clf = RandomForestClassifier(random_state=42)
clf = GradientBoostingClassifier(random_state=42)
#clf = BernoulliNB()  # ← Naive Bayes klassifikaator

# Koolitab valitud klassifikaatori.
clf.fit(X_train, y_train)

# Teeb ennustused testandmete kohta.
y_pred = clf.predict(X_test)

# Hindab mudeli ennustuste täpsust.
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy of {clf.__class__.__name__}: {accuracy:.2f}')  # Prindib välja klassifikaatori nime ja täpsuse.






##########
print("\n--- Sample Predictions (Energy Certificate Class) ---")
shown = 0
max_examples = 10

X_test_df = pd.DataFrame(X_test, columns=X.columns)
X_test_df = X_test_df.reset_index(drop=True)
y_test_reset = y_test.reset_index(drop=True)
y_pred_reset = pd.Series(y_pred).reset_index(drop=True)

for i in range(len(y_test_reset)):
    actual = label_encoder.inverse_transform([y_test_reset[i]])[0]
    predicted = label_encoder.inverse_transform([y_pred_reset[i]])[0]
    print(f"\nNäide {shown + 1}:")
    # print(X_test_df.iloc[i])  # optionally uncomment this if you want to see input features
    print(f"Tegelik energiamärgis: {actual}")
    print(f"Ennustatud energiamärgis: {predicted}")
    shown += 1
    if shown >= max_examples:
        break
##########











print("\nActual outcomes (y_test):")
print(y_test.to_numpy())  # Teisendab y_test pandas seeria numpy massiiviks parema loetavuse jaoks ja prindib selle välja.
print("\nPredicted outcomes (y_pred):")
print(y_pred)  # Prindib välja mudeli poolt ennustatud tulemused (y_pred).

# Milline tunnus omab tugevat ennustusväärtust? Kas antud klassifikaator toetab feature_importances_?
feature_names = X.columns
if hasattr(clf, 'feature_importances_'):
    # Print the feature importances
    print("Feature Importances:")
    for name, importance in zip(feature_names, clf.feature_importances_):
        print(f"{name}: {importance:.4f}")
else:
    print(f"{clf.__class__.__name__} does not support feature importance directly.")
