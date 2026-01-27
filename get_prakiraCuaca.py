import requests
import pandas as pd
import time

def ambil_cuaca_bmkg():
    print("Mulai ambil data Prakiraan cuaca BMKG Jawa Barat...")
    
    # baca file excel data kode wilayah jawa barat
    try:
        data_wilayah = pd.read_csv("kode_wilayah_jabar.csv")
    except:
        print("File excel tidak ditemukan!!!")
        return
        
    hasil_cuaca = [] # menyimpan data
    total = len(data_wilayah) # untuk melacak progres
    
    # loop setiap kelurahan
    for i, wilayah in data_wilayah.iterrows():
        url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={wilayah['Kode']}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                json_data = response.json()
                
                if json_data["data"]:
                    lokasi = json_data["data"][0]["lokasi"]
                    cuaca = json_data["data"][0]["cuaca"][0][0]
                    
                    hasil_cuaca.append({
                        "Kota": wilayah["Kabupaten/Kota"],
                        "Kecamatan": wilayah["Kecamatan"],
                        "Kelurahan": wilayah["Kelurahan"],
                        "Waktu Prakiraan": cuaca["local_datetime"],
                        "Suhu (°C)": cuaca["t"],
                        "Kelembapan (%)": cuaca["hu"],
                        "Kondisi Cuaca": cuaca["weather_desc"],
                        "Kecepatan Angin (km/jam)": cuaca["ws"],
                        "Latitude": lokasi["lat"],
                        "Longitude": lokasi["lon"]
                    })
                    print(f"[{i+1}/{total}] ✅ done {wilayah['Kelurahan']}")
            
            time.sleep(1.5)
            
        except:
            print(f"[{i+1}/{total}] ❌ skip {wilayah['Kelurahan']}")
            continue
        
    df = pd.DataFrame(hasil_cuaca)
    df.to_csv("Prakiraan_cuaca_jabar.csv", index=False)
    
    print(f"\n Selesai, total data: {len(df)}")

if __name__ == "__main__":
    ambil_cuaca_bmkg()