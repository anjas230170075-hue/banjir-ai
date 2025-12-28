import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# 1) Load dataset
df = pd.read_csv("dataset_banjir.csv")

# 2) Pisahkan fitur (X) dan label (y)
X = df[["curah_hujan", "tinggi_air"]]
y = df["status"]

# 3) Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4) Train model Decision Tree
model = DecisionTreeClassifier(random_state=42, max_depth=4)
model.fit(X_train, y_train)

# 5) Evaluasi
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
print("✅ Akurasi:", acc)
print("\n📌 Classification Report:\n", classification_report(y_test, pred))
print("\n📌 Confusion Matrix:\n", confusion_matrix(y_test, pred))

# 6) Simpan model
joblib.dump(model, "model.pkl")
print("\n✅ Model disimpan: model.pkl")
