import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import requests

# =========================
# CONFIG
# =========================
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

if not API_KEY:
    st.error("OPENWEATHER_API_KEY belum diset di Streamlit Secrets")
    st.stop()


st.set_page_config(
    page_title="BanjirAI",
    page_icon="🌊",
    layout="wide"
)

# =========================
# STYLE (Modern UI)
# =========================
st.markdown(
    """
    <style>
      .app-title {font-size: 2.0rem; font-weight: 800; margin-bottom: 0.25rem;}
      .app-subtitle {opacity: 0.85; margin-top: 0;}
      .card {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px 18px;
        background: rgba(255,255,255,0.03);
      }
      .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        font-size: 0.85rem;
        margin-right: 6px;
      }
      .muted {opacity: 0.8;}
      .small {font-size: 0.9rem;}
      .divider {height: 1px; background: rgba(255,255,255,0.08); margin: 14px 0;}
      /* Make buttons look nicer */
      div.stButton > button {
        border-radius: 12px;
        padding: 0.65rem 1rem;
        font-weight: 600;
      }
      /* Sidebar styling */
      section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,0.08);
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HELPERS
# =========================
@st.cache_data(show_spinner=False, ttl=60)  # cache 60 detik biar hemat request
def get_weather(lokasi: str):
    params = {"q": lokasi, "appid": API_KEY, "units": "metric", "lang": "id"}
    r = requests.get(BASE_URL, params=params, timeout=15)
    data = r.json()

    if r.status_code != 200:
        msg = data.get("message", "Gagal mengambil data cuaca.")
        raise ValueError(f"OpenWeather error {r.status_code}: {msg}")

    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rain_1h = 0.0
    if "rain" in data:
        rain_1h = float(data["rain"].get("1h", 0.0))

    return {
        "name": data.get("name", lokasi),
        "desc": desc,
        "temp": temp,
        "humidity": humidity,
        "rain_1h": rain_1h
    }

def format_time_now():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def status_rekomendasi(status: str):
    if status == "Aman":
        return (
            "🟢 **Rekomendasi Aksi:**\n"
            "- Tetap pantau informasi cuaca\n"
            "- Pastikan saluran air tidak tersumbat\n"
            "- Aktivitas dapat dilakukan seperti biasa"
        )
    if status == "Waspada":
        return (
            "🟡 **Rekomendasi Aksi:**\n"
            "- Siapkan perlengkapan darurat\n"
            "- Pantau kenaikan debit air\n"
            "- Koordinasi dengan aparat setempat"
        )
    return (
        "🔴 **Rekomendasi Aksi:**\n"
        "- Segera lakukan evakuasi\n"
        "- Jauhi area sungai dan dataran rendah\n"
        "- Ikuti arahan BPBD/petugas"
    )

def badge(text: str):
    st.markdown(f'<span class="pill">{text}</span>', unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
try:
    model = joblib.load("model.pkl")
except:
    st.error("❌ Model tidak ditemukan. Jalankan dulu: python train_model.py")
    st.stop()

# =========================
# HEADER
# =========================
st.markdown('<div class="app-title">🌊 BanjirAI</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle muted">Cuaca real-time (OpenWeather) + Prediksi Risiko Banjir (Decision Tree) — tampilkan status, risiko, dan rekomendasi aksi.</p>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR INPUTS (Modern)
# =========================
with st.sidebar:
    st.header("⚙️ Input")
    lokasi = st.text_input("Lokasi (format aman: Kota,ID)", value="Lhokseumawe,ID")
    st.caption("Contoh: Banda Aceh,ID • Medan,ID • Jakarta,ID")

    ambil_cuaca = st.button("☁️ Ambil Cuaca", use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.subheader("🌧️ Input Banjir")

    # default curah hujan dari cuaca (akan diisi setelah ambil_cuaca)
    if "weather" not in st.session_state:
        st.session_state.weather = None

    default_curah = 0
    if st.session_state.weather:
        default_curah = int(round(st.session_state.weather.get("rain_1h", 0)))

    curah_hujan = st.number_input(
        "Curah hujan (mm)",
        min_value=0,
        max_value=500,
        value=default_curah,
        step=1,
        help="Default diisi otomatis dari hujan 1 jam terakhir (OpenWeather). Kamu bisa ubah manual."
    )

    tinggi_air = st.number_input(
        "Tinggi air (cm)",
        min_value=0,
        max_value=300,
        value=100,
        step=1
    )

    prediksi_btn = st.button("🔍 Prediksi Risiko", type="primary", use_container_width=True)

# =========================
# WEATHER FETCH
# =========================
if ambil_cuaca:
    if not lokasi.strip():
        st.sidebar.error("Mohon isi lokasi dulu.")
    else:
        try:
            st.session_state.weather = get_weather(lokasi.strip())
            st.sidebar.success("Cuaca berhasil diambil ✅")
        except Exception as e:
            st.session_state.weather = None
            st.sidebar.error(f"Gagal ambil cuaca: {e}")

# =========================
# MAIN LAYOUT (2 columns)
# =========================
left, right = st.columns([1.15, 1.0], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌦️ Cuaca Saat Ini")
    waktu = format_time_now()
    badge(f"📍 {lokasi}")
    badge(f"🕒 {waktu}")

    if st.session_state.weather:
        w = st.session_state.weather
        st.write(f"**Lokasi terdeteksi:** {w['name']}")
        st.write(f"**Kondisi:** {w['desc']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Suhu (°C)", f"{w['temp']}")
        c2.metric("Kelembapan (%)", f"{w['humidity']}")
        c3.metric("Hujan 1 jam (mm)", f"{w['rain_1h']}")
        st.caption("Sumber: OpenWeather")
    else:
        st.info("Klik **☁️ Ambil Cuaca** di sidebar untuk menampilkan cuaca dan mengisi default curah hujan otomatis.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧾 Ringkasan Input")
    st.write(f"- **Lokasi:** {lokasi}")
    st.write(f"- **Curah hujan:** {curah_hujan} mm")
    st.write(f"- **Tinggi air:** {tinggi_air} cm")
    st.caption("Catatan: curah hujan default diambil dari ‘rain_1h’ (hujan 1 jam terakhir). Kamu boleh set manual untuk simulasi.")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Hasil Prediksi")
    st.caption("Klik tombol **Prediksi Risiko** di sidebar untuk menjalankan model.")

    if prediksi_btn:
        if not lokasi.strip():
            st.error("Mohon isi lokasi (Kota,ID) terlebih dahulu.")
        else:
            X = pd.DataFrame([{"curah_hujan": curah_hujan, "tinggi_air": tinggi_air}])

            hasil = model.predict(X)[0]
            prob = model.predict_proba(X)
            confidence = max(prob[0]) * 100

            # Header hasil
            badge(f"Status: {hasil}")
            badge(f"Risiko: {confidence:.2f}%")

            # Tampilkan dengan styling Streamlit bawaan (modern)
            if hasil == "Aman":
                st.success(f"✅ **{hasil}**")
            elif hasil == "Waspada":
                st.warning(f"⚠️ **{hasil}**")
            else:
                st.error(f"🚨 **{hasil}**")

            st.markdown(status_rekomendasi(hasil))

            # Tambahan info cuaca singkat
            if st.session_state.weather:
                w = st.session_state.weather
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.write("**Cuaca (ringkas):**")
                st.write(f"- {w['desc']} | Hujan: {w['rain_1h']} mm/jam")

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("© 2025 | BanjirAI — Machine Learning + OpenWeather")

