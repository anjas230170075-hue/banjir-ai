import numpy as np
import pandas as pd

np.random.seed(42)

N = 300  # jumlah data

curah_hujan = np.random.randint(0, 401, size=N)   # mm
tinggi_air  = np.random.randint(50, 261, size=N)  # cm

def label_banjir(hujan, air):
    if hujan > 250 or air > 180:
        return "Bahaya"
    elif hujan >= 150 or air >= 120:
        return "Waspada"
    else:
        return "Aman"

status = [label_banjir(h, a) for h, a in zip(curah_hujan, tinggi_air)]

df = pd.DataFrame({
    "curah_hujan": curah_hujan,
    "tinggi_air": tinggi_air,
    "status": status
})

df.to_csv("dataset_banjir.csv", index=False)

print("✅ dataset_banjir.csv berhasil dibuat")
print(df.head())
