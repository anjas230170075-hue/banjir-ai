# 🌊 BanjirAI  
### Aplikasi Prediksi Potensi Banjir Berbasis Machine Learning & Cuaca Real-Time

---

## 📌 Deskripsi
**BanjirAI** adalah aplikasi berbasis **Machine Learning** yang digunakan untuk memprediksi
**potensi banjir** berdasarkan **curah hujan** dan **tinggi air**.  
Aplikasi ini mengintegrasikan **OpenWeather API** untuk mengambil data cuaca real-time
(cerah/hujan dan intensitas hujan), kemudian memprosesnya menggunakan
**algoritma Decision Tree** untuk menghasilkan status banjir serta rekomendasi tindakan.

Aplikasi ini dikembangkan sebagai **Projek Akhir / UAS Mata Kuliah Machine Learning**.

---

## 🎯 Tujuan Aplikasi
- Menyediakan informasi cuaca real-time berdasarkan lokasi
- Menampilkan intensitas hujan secara aktual
- Memprediksi potensi banjir menggunakan Machine Learning
- Memberikan rekomendasi tindakan kepada masyarakat
- Menjadi alat bantu mitigasi bencana banjir

---

## 🧠 Metode & Teknologi
### 🔹 Machine Learning
- Algoritma: **Decision Tree Classifier**
- Fitur:
  - Curah hujan (mm)
  - Tinggi air (cm)
- Output:
  - Aman
  - Waspada
  - Bahaya

### 🔹 Sumber Data Cuaca
- **OpenWeather API**
  - Kondisi cuaca saat ini
  - Intensitas hujan (mm/jam)
  - Suhu & kelembapan

---

## 📥 Input Aplikasi
- Lokasi (format: `Kota,ID`)
- Curah hujan (mm)  
  *(otomatis dari OpenWeather, dapat diubah manual)*
- Tinggi air (cm)

---

## 📤 Output Aplikasi
- Kondisi cuaca (cerah/hujan)
- Intensitas hujan (mm/jam)
- Status potensi banjir:
  - 🟢 Aman
  - 🟡 Waspada
  - 🔴 Bahaya
- Tingkat risiko (%)
- Rekomendasi tindakan mitigasi
- Waktu dan lokasi prediksi

---

## 🖥️ Tampilan Aplikasi
- Desain **modern & berwarna**
- Sidebar untuk input
- Dashboard interaktif
- Tampilan status banjir dengan warna kontekstual

---

## 🛠️ Teknologi & Library
- Python 3.x
- Streamlit
- Pandas
- Scikit-learn
- Requests
- Joblib
- OpenWeather API

---

## 🚀 Cara Menjalankan Aplikasi

### 1️⃣ Install library
```bash
pip install streamlit pandas scikit-learn requests joblib
