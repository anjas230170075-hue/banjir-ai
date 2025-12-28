import requests
API_KEY = "a52c78ddcc6b54a4451d7eec3ec7328d"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(kota):
    params = {
        "q": kota,
        "appid": API_KEY,
        "units": "metric",
        "lang": "id"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("❌ Gagal mengambil data cuaca")
        print(response.json())
        return

    data = response.json()

    cuaca = data["weather"][0]["description"]
    suhu = data["main"]["temp"]
    kelembapan = data["main"]["humidity"]

    hujan = 0
    if "rain" in data:
        hujan = data["rain"].get("1h", 0)

    print("📍 Lokasi :", data["name"])
    print("🌤️ Cuaca :", cuaca)
    print("🌡️ Suhu :", suhu, "°C")
    print("💧 Kelembapan :", kelembapan, "%")
    print("🌧️ Intensitas Hujan :", hujan, "mm/jam")

if __name__ == "__main__":
    kota = input("Masukkan kota (contoh: Lhokseumawe,ID): ")
    get_weather(kota)
